import logging

from src.core.queue.models import BEvent, CUDEvent, Event
from src.core.settings import settings
from pika import BlockingConnection, BasicProperties, spec, URLParameters


class QueuePublisher:

    def __init__(self):
        self._url = settings.rabbit_url
        self.connection = None
        self.channel = None
        self.queue_be = None
        self.queue_cud = None

    def connect(self) -> None:
        self.connection = BlockingConnection(
            URLParameters(self._url))
        self.channel = self.connection.channel()
        self.queue_be = self.channel.queue_declare(
            queue=settings.rabbitmq_queue_be,
            durable=True
        )
        self.queue_cud = self.channel.queue_declare(
            queue=settings.rabbitmq_queue_cud,
            durable=True
        )

    def publish_be(self, event: Event) -> None:
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=settings.rabbitmq_queue_be,
                body=event.json(),
                properties=BasicProperties(
                    delivery_mode=spec.PERSISTENT_DELIVERY_MODE
                )
            )
        except Exception as err:
            logging.error("ERROR: error publishing BE" + str(err))
            raise err

    def publish_cud(self, event: Event) -> None:
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=settings.rabbitmq_queue_cud,
                body=event.json(),
                properties=BasicProperties(
                    delivery_mode=spec.PERSISTENT_DELIVERY_MODE
                )
            )
        except Exception as err:
            logging.error("ERROR: error publishing CUD" + str(err))
            raise err

    def stop(self):
        self.channel.close()
        self.connection.close()
