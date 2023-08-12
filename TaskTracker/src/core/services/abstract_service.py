from abc import ABC
from src.core.db.repository import TaskRepository


class AbstractService(ABC):
    def __init__(self) -> None:
        self.task_repository = TaskRepository()
