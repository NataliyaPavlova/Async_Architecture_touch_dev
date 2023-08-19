import logging

import asyncio
from aio_pika import DeliveryMode, Message, connect, AbstractIncomingMessage

from src.core.queue.models import BEvent, StreamEvent, Event
from src.core.settings import settings
from src.core.services.event_service import EventService


class QueueConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_be = None
        self.queue_stream = None
        self.event_service = EventService()

    async def connect(self) -> None:
        self.connection = await connect(settings.rabbit_url)

        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        self.queue_be = await self.channel.queue_declare(
            queue=settings.rabbitmq_queue_consume_be,
            durable=True
        )
        self.queue_stream = await self.channel.queue_declare(
            queue=settings.rabbitmq_queue_consume_stream,
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


events_consumer = QueueConsumer()
