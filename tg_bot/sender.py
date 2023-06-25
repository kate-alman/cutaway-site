import asyncio
import logging
from asyncio import Task

import bson
from aio_pika import IncomingMessage

from config import Config
from tg_bot.consts import MORE_POST
from tg_bot.keyboards import START_KEYBOARD, POST_AMOUNT_KEYBOARD
from tg_bot.rabbitMQ import RabbitMQ
from tg_bot.client import TgClient


class TgSender:
    """A class that (if running) sends messages processed by the worker to the user in the chat."""
    def __init__(self, cfg: Config):
        self.workers = 10
        self.tg_client = TgClient(cfg=cfg)
        self.rabbitMQ = RabbitMQ(
            host=cfg.rabbitmq.host,
            port=cfg.rabbitmq.port,
            user=cfg.rabbitmq.user,
            password=cfg.rabbitmq.password,
        )
        self.routing_key_worker = "tg_worker"
        self.routing_key_sender = "tg_sender"
        self.queue_name = "tg_sender"
        self._tasks: list[Task] = []

        self.logger = logging.getLogger("sender")

    async def on_message(self, message: IncomingMessage) -> None:
        """Passes messages for processing."""
        update = bson.loads(message.body)
        await self.handle_update(update)
        await message.ack()

    async def start(self) -> None:
        await self.rabbitMQ.connect()
        self._tasks = [
            asyncio.create_task(self._worker_rabbit()) for _ in range(self.workers)
        ]

    async def stop(self) -> None:
        for task in self._tasks:
            task.cancel()
        await self.rabbitMQ.disconnect()

    async def _worker_rabbit(self) -> None:
        """Receives messages from the queue."""
        await self.rabbitMQ.listen_events(
            on_message_func=self.on_message,
            queue_name=self.queue_name,
            routing_key=[self.routing_key_sender],
        )

    async def handle_update(self, update: dict) -> None:
        """Depending on the type of update, sends a message to the user and the keyboard if necessary."""
        match update["type_"]:
            case "message":
                await self.tg_client.send_message(
                    chat_id=update["chat_id"],
                    text=update["text"],
                )
            case "start_message":
                await self.tg_client.send_keyboard(
                    chat_id=update["chat_id"],
                    text=update["text"],
                    keyboard=START_KEYBOARD,
                )
            case "get_posts":
                await self.tg_client.send_keyboard(
                    chat_id=update["chat_id"],
                    text=update.get("text", None),
                    keyboard=POST_AMOUNT_KEYBOARD,
                )
            case "show_posts":
                await self.tg_client.send_message(
                    chat_id=update["chat_id"],
                    text=update.get("text", None),
                )
                await asyncio.sleep(1)
                await self.tg_client.send_message(
                    chat_id=update["chat_id"],
                    text=MORE_POST,
                )
                await self.tg_client.remove_inline_keyboard(
                    message_id=update["message_id"], chat_id=update["chat_id"]
                )

        await asyncio.sleep(1)
