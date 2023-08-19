from abc import ABC
from src.core.db.repository import TaskRepository, UserRepository
# from src.core.queue.rabbit_sender import event_publisher


class AbstractService(ABC):
    def __init__(self) -> None:
        self.task_repository = TaskRepository()
        self.user_repository = UserRepository()
        # self.event_publisher = QueuePublisher()
