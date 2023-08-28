import logging

from aio_pika import DeliveryMode, Message, connect
from aio_pika.exceptions import PublishError, DeliveryError
from aiormq.abc import Basic

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

        async with self.connection:
            self.channel = await self.connection.channel(on_return_raises=True)
            await self.channel.set_qos(prefetch_count=1)

            self.queue_be = await self.channel.declare_queue(
                name=settings.rabbitmq_queue_be,
                durable=True
            )
            self.queue_stream = await self.channel.declare_queue(
                name=settings.rabbitmq_queue_stream,
                durable=True
            )

    async def publish_be(self, event: Event) -> None:
        print(f'Got a business event to send: {event}')
        self.connection = await connect(url=settings.rabbit_url)
        async with self.connection:
            channel = await self.connection.channel(on_return_raises=True)
            message = Message(body=event.json().encode(), delivery_mode=DeliveryMode.PERSISTENT)
            try:
                confirmation = await channel.default_exchange.publish(
                    message, routing_key=settings.rabbitmq_queue_be,
                )
            except (PublishError, DeliveryError) as e:
                print(e)
            else:
                if not isinstance(confirmation, Basic.Ack):
                    print(f"Message {event} was not acknowledged by broker!")

    async def publish_stream(self, event: Event) -> None:
        print(f'Got a business event to send: {event}')
        self.connection = await connect(url=settings.rabbit_url)
        async with self.connection:
            channel = await self.connection.channel(on_return_raises=True)
            message = Message(body=event.json().encode(), delivery_mode=DeliveryMode.PERSISTENT)
            try:
                confirmation = await channel.default_exchange.publish(
                    message, routing_key=settings.rabbitmq_queue_stream,
                )
            except (PublishError, DeliveryError) as e:
                print(e)
            else:
                if not isinstance(confirmation, Basic.Ack):
                    print(f"Message {event} was not acknowledged by broker!")


event_publisher = QueuePublisher()
