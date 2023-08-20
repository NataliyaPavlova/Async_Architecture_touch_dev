from src.core.queue.base_consumer import BaseQueueConsumer
from src.core.settings import settings
from src.core.services.event_service import AuthEventService


class AuthQueueConsumer(BaseQueueConsumer):
    def __init__(self):
        super().__init__()
        self.event_service = AuthEventService()
        self.queue_be_title = settings.auth_queue_consume_be
        self.queue_stream_title = settings.auth_queue_consume_stream


auth_consumer = AuthQueueConsumer()
