import random

from src.core.services.abstract_service import AbstractService
from src.core.db.models import Task
from src.core.services.models import TaskInService
from src.api.request_models import TaskRequest


class TaskService(AbstractService):

    def create(self, task: TaskRequest) -> Task:
        task_to_create = TaskInService(
            description=task.description,
        )
        created_id = self.task_repository.add(task_to_create)
        return self.task_repository.get(created_id)

    # def get_popug_tasks(self, popug_public_id: str) -> list[Task] | None:
    #     tasks = self.task_repository.get_popug_tasks(popug_public_id)
    #     return tasks or None

    def get_task(self, public_id: str) -> Task | None:
        task = self.task_repository.get_task(public_id)
        return task or None

    def update(self, task: TaskInService) -> None:
        self.task_repository.update(task)
