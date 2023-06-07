import asyncio
import json
import logging
from typing import Optional

import aio_pika
import aiormq
import bson
from aio_pika import (
    Connection,
    RobustChannel,
    ExchangeType,
    IncomingMessage,
    RobustExchange,
)

from config import config


class RabbitMQ:
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.host = host if host else config.rabbitmq.host
        self.port = port if port else config.rabbitmq.port
        self.user = user if user else config.rabbitmq.user
        self.password = password if password else config.rabbitmq.password
        self.url = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"

        self.exchange: Optional[ExchangeType] = None
        self.connection_: Optional[Connection] = None
        self.listener: Optional[asyncio.Task] = None
        self.logger = logging.getLogger(__name__)
        self.channel: Optional[RobustChannel] = None

    async def connect(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            connection = await aio_pika.connect_robust(self.url, loop=loop)

        except (ConnectionError, aiormq.exceptions.IncompatibleProtocolError) as e:
            self.logger.error(f"action=setup_rabbitmq, status=fail, retry=10s, {e}")
            await asyncio.sleep(10)
            await self.connect()
            return None

        channel = await connection.channel(publisher_confirms=True)
        auth_exchange = await channel.declare_exchange(
            name="my-auth-delayed",
            type=ExchangeType.X_DELAYED_MESSAGE,
            durable=True,
            arguments={"x-delayed-type": "direct"},
        )
        self.channel = channel
        self.connection_ = connection
        self.exchange = auth_exchange
        self.logger.info("action=setup_rabbitmq, status=success")

    async def disconnect(self) -> None:
        if self.channel:
            await self.channel.close()
            self.channel = None
        if self.connection_:
            await self.connection_.close()
            self.connection_ = None
        self.logger.info("action=close_rabbitmq, status=success")

    async def send_event(
        self,
        message: dict,
        routing_key: str,
        delay: int = 10,
    ) -> None:
        """
        Отправка сообщения
        :param message: словарь с сообщением
        :param routing_key: роутинг ключ
        :param delay: время жизни сообщения
        """
        self.logger.info(f"action=send_event, status=success, message={message}")
        await self.exchange.publish(
            aio_pika.Message(
                body=bson.dumps(message),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={"x-delay": delay},
            ),
            routing_key=routing_key,
            mandatory=False,
        )

    async def listen_events(
        self, routing_key: list[str], queue_name: str, on_message_func=None
    ) -> None:
        """
        Прослушивание событий
        :param routing_key: роутинг ключ
        :param queue_name: имя очереди
        :param on_message_func: функция, которая будет вызвана при получении сообщения
        """
        self.logger.info(
            f"action=listen_events, status=success, routing_key={routing_key}, queue_name={queue_name}"
        )
        try:
            channel = await self.connection_.channel()
            await channel.set_qos(prefetch_count=1)

            auth_exchange = await channel.declare_exchange(
                name="my-auth-delayed",
                type=aio_pika.ExchangeType.X_DELAYED_MESSAGE,
                durable=True,
                arguments={"x-delayed-type": "direct"},
            )
            queue = await channel.declare_queue(
                name=queue_name,
                durable=True,
            )
            for key in routing_key:
                await queue.bind(auth_exchange, routing_key=key)
            await queue.consume(on_message_func if on_message_func else self.on_message)
            self.logger.info(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future()
        except asyncio.CancelledError:
            pass

    async def on_message(self, message: IncomingMessage) -> None:
        """
        Функция, которая будет вызвана при получении сообщения
        :param message: сообщение
        """
        self.logger.info("Message body is: %r" % bson.loads(message.body))
