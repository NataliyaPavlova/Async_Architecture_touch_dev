import logging

import asyncio
from aio_pika import DeliveryMode, Message, connect
from aio_pika.abc import AbstractIncomingMessage


from src.core.queue.models import BEvent, StreamEvent, Event
from src.core.settings import settings


class BaseQueueConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_be = None
        self.queue_stream = None
        self.event_service = None
        self.queue_be_title = None
        self.queue_stream_title = None

    async def connect(self) -> None:
        self.connection = await connect(settings.rabbit_url)

        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        self.queue_be = await self.channel.queue_declare(
            queue=self.queue_be_title,
            durable=True
        )
        self.queue_stream = await self.channel.queue_declare(
            queue=self.queue_stream_title,
            durable=True
        )

    async def consume_be(self):
        await self.queue_be.consume(self.on_message_be)
        await asyncio.Future()

    async def consume_stream(self):
        await self.queue_stream.consume(self.on_message_stream)
        await asyncio.Future()

    async def on_message_be(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            event = BEvent(**message.body().decode())
            self.event_service.process_business_event(event)

    async def on_message_stream(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            event = StreamEvent(**message.body().decode())
            self.event_service.process_stream_event(event)

    def stop(self):
        self.channel.close()
        self.connection.close()

