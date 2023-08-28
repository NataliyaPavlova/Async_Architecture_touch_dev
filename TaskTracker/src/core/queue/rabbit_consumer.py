import logging
import json
import asyncio
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import logger


from src.core.queue.models import BEvent, StreamEvent, Event
from src.core.settings import settings
from src.core.services.event_service import EventService

logger.setLevel(logging.INFO)


class QueueConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_be = None
        self.queue_stream = None
        self.event_service = EventService()


    async def consume_be(self):
        self.connection = await connect(settings.rabbit_url)
        async with self.connection:
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)
            self.queue_be = await self.channel.declare_queue(
                name=settings.rabbitmq_queue_consume_be,
                durable=True
            )
            await self.queue_be.consume(self.on_message_be)
            self.queue_stream = await self.channel.declare_queue(
                name=settings.rabbitmq_queue_consume_stream,
                durable=True
            )
            await self.queue_stream.consume(self.on_message_stream)
            await asyncio.Future()

    async def consume_stream(self):
        self.connection = await connect(settings.rabbit_url)
        async with self.connection:
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)
            self.queue_stream = await self.channel.declare_queue(
                name=settings.rabbitmq_queue_consume_stream,
                durable=True
            )
            await self.queue_stream.consume(self.on_message_stream)
            await asyncio.Future()

    async def on_message_be(self, message: AbstractIncomingMessage) -> None:
        print(f'Got a be message: {message.body}')
        async with message.process():
            event_json = json.loads(message.body.decode())
            event = BEvent(**event_json)
            await self.event_service.process_business_event(event)

    async def on_message_stream(self, message: AbstractIncomingMessage) -> None:
        print(f'Got a stream message: {message.body}')
        async with message.process():
            event_json = json.loads(message.body.decode())
            event = StreamEvent(**event_json)
            await self.event_service.process_stream_event(event)

    def stop(self):
        self.channel.close()
        self.connection.close()


event_consumer = QueueConsumer()
