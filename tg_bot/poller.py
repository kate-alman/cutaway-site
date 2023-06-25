import asyncio
import logging
from asyncio import Task, Future
from typing import Optional

from config import Config

from tg_bot.dataclass import UpdateObject
from tg_bot.client import TgClient
from tg_bot.rabbitMQ import RabbitMQ


class Poller:
    """A class that (if running) constantly checks for new messages from the bot."""
    def __init__(self, cfg: Config, timeout: int = 20):
        self.logger = logging.getLogger("tg_poller")
        logging.basicConfig(level=logging.INFO)
        self._task: Optional[Task] = None
        self.tg_client: TgClient = TgClient(cfg=cfg)
        self.rabbitMQ = RabbitMQ(
            host=cfg.rabbitmq.host,
            port=cfg.rabbitmq.port,
            user=cfg.rabbitmq.user,
            password=cfg.rabbitmq.password,
        )
        self.is_running = False
        self.timeout = timeout

    def _done_callback(self, future: Future) -> None:
        if future.exception():
            self.logger.exception("polling failed", exc_info=future.exception())

    async def start(self):
        task_poll = asyncio.create_task(self._poll())
        task_poll.add_done_callback(self._done_callback)
        self.is_running = True
        self._task = task_poll
        await self.rabbitMQ.connect()

    async def stop(self):
        self.is_running = False
        await self.rabbitMQ.disconnect()
        if self._task:
            await asyncio.wait([self._task], timeout=self.timeout)
            self._task.cancel()
        self._task = None

    async def _poll(self):
        offset = 0
        while self.is_running:
            self.logger.info("Polling...")
            update_res = await self.tg_client.get_update_objects(
                offset=offset, timeout=self.timeout
            )
            if update_res:
                for upd in update_res.result:
                    offset = upd.update_id + 1
                    update = UpdateObject.Schema().dump(upd)
                    await self.rabbitMQ.send_event(
                        message=update, routing_key="tg_poller"
                    )
                    await asyncio.sleep(1)
