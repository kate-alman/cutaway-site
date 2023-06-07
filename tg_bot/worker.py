import asyncio
import json
import logging
import random
from asyncio import Task

import bson
import requests
from aio_pika import IncomingMessage

from config import Config
from tg_bot.consts import GREETINGS, REDIRECT_SITE, NO_MATCHES, POST_AMOUNT, GIFT, ERROR
from tg_bot.dataclass import UpdateObject, PostSchema
from tg_bot.rabbitMQ import RabbitMQ


class BotWorker:
    def __init__(self, cfg: Config):
        self.rabbitMQ = RabbitMQ(
            host=cfg.rabbitmq.host,
            port=cfg.rabbitmq.port,
            user=cfg.rabbitmq.user,
            password=cfg.rabbitmq.password,
        )
        self._tasks: list[Task] = []
        self.workers = 10
        self.routing_key_worker = "tg_worker"
        self.routing_key_sender = "tg_sender"
        self.routing_key_poller = "tg_poller"
        self.queue_name = "tg_bot"
        self.logger = logging.getLogger("worker")
        self.is_running = False

    async def start(self) -> None:
        await self.rabbitMQ.connect()
        self._tasks = [
            asyncio.create_task(self._worker_rabbit()) for _ in range(self.workers)
        ]
        self.is_running = True

    async def stop(self) -> None:
        self.is_running = False
        for task in self._tasks:
            task.cancel()
        await self.rabbitMQ.disconnect()

    async def _worker_rabbit(self) -> None:
        """
        Метод для прослушивания событий RabbitMQ.
        """
        await self.rabbitMQ.listen_events(
            on_message_func=self.on_message,
            routing_key=[self.routing_key_worker, self.routing_key_poller],
            queue_name=self.queue_name,
        )

    async def on_message(self, message: IncomingMessage) -> None:
        if message.routing_key == "tg_poller":
            update: UpdateObject = UpdateObject.Schema().load(bson.loads(message.body))
            if update.message:
                await self._handler(message)
            elif update.callback_query:
                await self.handle_callback_query(update)
        elif message.routing_key == self.routing_key_worker:
            text = bson.loads(message.body)
            match text["type_"]:
                case "wanna_post":
                    await self.rabbitMQ.send_event(
                        message={
                            "type_": "get_posts",
                            "chat_id": text["chat_id"],
                            "text": POST_AMOUNT,
                        },
                        routing_key=self.routing_key_sender,
                    )
                case "amount":
                    try:
                        count = int(text["text"][1:])
                        posts = await self.get_posts(count=count)
                        await self.rabbitMQ.send_event(
                            message={
                                "type_": "show_posts",
                                "message_id": text["message_id"],
                                "chat_id": text["chat_id"],
                                "text": posts,
                            },
                            routing_key=self.routing_key_sender,
                        )
                    except ValueError:
                        await self.rabbitMQ.send_event(
                            message={
                                "type_": "message",
                                "message_id": text["message_id"],
                                "chat_id": text["chat_id"],
                                "text": ERROR,
                            },
                            routing_key=self.routing_key_sender,
                        )
        await message.ack()

    async def _handler(self, upd: IncomingMessage) -> None:
        update: UpdateObject = UpdateObject.Schema().load(bson.loads(upd.body))
        match update.message.text.split()[-1]:
            case "/start":
                await self.rabbitMQ.send_event(
                    message={
                        "type_": "start_message",
                        "chat_id": update.message.chat.id,
                        "text": GREETINGS,
                    },
                    routing_key=self.routing_key_sender,
                )
            case "посты":
                wanna_post = {
                    "type_": "wanna_post",
                    "chat_id": update.message.chat.id,
                }
                await self.rabbitMQ.send_event(
                    message=wanna_post,
                    routing_key=self.routing_key_worker,
                )
            case "приятность":
                gift = random.choice(GIFT)
                await self.rabbitMQ.send_event(
                    message={
                        "type_": "message",
                        "chat_id": update.message.chat.id,
                        "text": gift,
                    },
                    routing_key=self.routing_key_sender,
                )
            case "сайт":
                await self.rabbitMQ.send_event(
                    message={
                        "type_": "message",
                        "chat_id": update.message.chat.id,
                        "text": REDIRECT_SITE,
                    },
                    routing_key=self.routing_key_sender,
                )
            case _:
                await self.rabbitMQ.send_event(
                    message={
                        "type_": "message",
                        "chat_id": update.message.chat.id,
                        "text": NO_MATCHES,
                    },
                    routing_key=self.routing_key_sender,
                )

    async def handle_callback_query(self, update: UpdateObject) -> None:
        match update.callback_query.data:
            case str() as char if char[1:].isdigit():
                await self.rabbitMQ.send_event(
                    message={
                        "type_": "amount",
                        "message_id": update.callback_query.message.message_id,
                        "chat_id": update.callback_query.message.chat.id,
                        "text": update.callback_query.data,
                    },
                    routing_key=self.routing_key_worker,
                )
            case _:
                await self.rabbitMQ.send_event(
                    message={
                        "type_": "message",
                        "chat_id": update.message.chat.id,
                        "text": NO_MATCHES,
                    },
                    routing_key=self.routing_key_sender,
                )

    @staticmethod
    async def get_posts(count: int) -> str:
        resp = requests.get(
            f"https://alman-project.ru/api/v1/posts/", params={"amount": count}
        )
        resp_to_json = json.loads(resp.content)
        posts = PostSchema().dump(resp_to_json["results"], many=True)
        return "\n -------------- next post -------------- \n".join(
            PostSchema().to_dict(post) for post in posts
        )
