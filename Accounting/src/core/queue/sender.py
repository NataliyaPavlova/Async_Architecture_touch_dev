import logging

from aio_pika import DeliveryMode, Message, connect

from src.core.queue.models import Event
from src.core.settings import settings


class QueuePublisher:

    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_be = None
        self.queue_stream = None

    async def connect(self) -> None:
        self.connection = await connect(settings.rabbit_url)

        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        self.queue_be = await self.channel.queue_declare(
            queue=settings.rabbitmq_queue_be,
            durable=True
        )
        self.queue_stream = await self.channel.queue_declare(
            queue=settings.rabbitmq_queue_stream,
            durable=True
        )

    async def publish_be(self, event: Event) -> None:
        channel = await self.connection.channel()
        message = Message(body=event.json().encode(), delivery_mode=DeliveryMode.PERSISTENT)
        await channel.default_exchange.publish(
            message, routing_key=settings.rabbitmq_queue_be,
        )

    async def publish_stream(self, event: Event) -> None:
        message = Message(body=event.json().encode(), delivery_mode=DeliveryMode.PERSISTENT)
        await self.channel.default_exchange.publish(
            message, routing_key=settings.rabbitmq_queue_stream,
        )

    def stop(self):
        self.channel.close()
        self.connection.close()


event_publisher = QueuePublisher()
