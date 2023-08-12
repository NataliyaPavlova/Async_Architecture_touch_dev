from celery.utils.log import get_task_logger
from admin_api.src.core.queue.models import Event
from admin_api.src.core.settings import get_settings
from pika import BlockingConnection, BasicProperties, spec, URLParameters

settings = get_settings()


class QueuePublisher:

    def __init__(self):
        self._url = settings.rabbit_url
        self.connection = None
        self.channel = None
        self.queue = None
        self.logger = get_task_logger(settings.log_filename)

    def connect(self) -> None:
        self.connection = BlockingConnection(
            URLParameters(self._url))
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(
            queue=settings.rabbitmq_queue,
            durable=True
        )

    def publish(self, event: Event) -> None:
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=settings.rabbitmq_queue,
                body=event.json(),
                properties=BasicProperties(
                    delivery_mode=spec.PERSISTENT_DELIVERY_MODE
                )
            )
        except Exception as err:
            self.logger.error("ERROR: error publishing " + str(err))
            raise err

    def stop(self):
        self.channel.close()
        self.connection.close()
