from src.core.settings import settings
from src.core.services.event_service import TaskTrackerEventService


class TaskTrackerQueueConsumer:
    def __init__(self):
        super().__init__()
        self.queue_be_title = settings.tasktracker_queue_consume_be
        self.queue_stream_title = settings.tasktracker_queue_consume_stream
        self.event_service = TaskTrackerEventService()


tasktracker_consumer = TaskTrackerQueueConsumer()
