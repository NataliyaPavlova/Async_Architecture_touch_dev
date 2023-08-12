from http.client import HTTPSConnection
import json
import random

from src.core.settings import settings
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

    def get_popug_tasks(self, popug_id: int) -> list[Task] | None:
        tasks = self.task_repository.get_popug_tasks(popug_id)
        if tasks:
            return tasks
        return None

    def get_undone_tasks(self) -> list[Task] | None:
        tasks = self.task_repository.get_undone_tasks()
        if tasks:
            return tasks
        return None

    def shuffle(self):
        undone_tasks = self.get_undone_tasks()
        # get all popugs-workers
        with HTTPSConnection(settings.auth_host) as connection:
            headers = {'Content-type': 'application/json'}
            connection.request('GET', settings.get_workers_url, headers)
            response = connection.getresponse()
            workers = response.read().decode()
        if not workers:
            return None
        # randomly shuffle among workers
        for task in undone_tasks:
            assignee = random.choice(workers)
            self.task_repository.update_assignee(task.task_id, assignee)
        return self.get_undone_tasks()

    def update_status(self, task_id: int) -> Task:
        self.task_repository.update_status(task_id)
        return self.task_repository.get(task_id)

