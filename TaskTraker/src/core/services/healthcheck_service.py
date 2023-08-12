from pika.exceptions import AMQPConnectionError

from TaskTraker.src.core.settings import get_settings
from TaskTraker.src.core.queue.connection import get_rabbitmq_connection

settings = get_settings()


class HealthcheckService:

    @staticmethod
    async def check_queue_connect() -> bool:
        try:
            connection = get_rabbitmq_connection()
            if connection.is_open is True:
                return True
            return False
        except AMQPConnectionError:
            return False
