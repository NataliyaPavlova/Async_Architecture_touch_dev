from aio_pika import DeliveryMode, Message, connect
from aio_pika.exceptions import PublishError, DeliveryError
from aiormq.abc import Basic

from src.core.queue.models import BEvent, StreamEvent, Event
from src.core.settings import settings
from schema_registry.validators.user.v1.event_validator import UserEventValidator


class QueuePublisher:

    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_be = None
        self.queue_stream = None
        self.event_validator = UserEventValidator()

    async def connect(self) -> None:
        print(f'Trying to connect to MB: {settings.rabbit_url}')
        u = settings.rabbit_url
        self.connection = await connect(url=u)
        async with self.connection:
            channel = await self.connection.channel(on_return_raises=True)
            self.queue_stream = await channel.declare_queue(
                name=settings.rabbitmq_queue_stream,
                durable=True
            )
            self.queue_be = await channel.declare_queue(
                name=settings.rabbitmq_queue_be,
                durable=True
            )

    async def publish_be(self, event: Event) -> None:
        print(f'Got a business event to send: {event}')
        if not self.event_validator.validate_be_event_added(event):
            print(f'Validation error: event {event} is not match its schema')
            return
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
        print(f'Got a stream event to send: {event}')
        if not self.event_validator.validate_stream_event_created(event):
            print(f'Validation error: event {event} is not match its schema')
            return
        self.connection = await connect(settings.rabbit_url)
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


message_broker = QueuePublisher()
