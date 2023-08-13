from abc import ABC
from src.core.db.repository import TaskRepository
from src.core.queue.rabbit_sender import QueuePublisher


class AbstractService(ABC):
    def __init__(self) -> None:
        self.task_repository = TaskRepository()
        self.queue_publisher = QueuePublisher()
