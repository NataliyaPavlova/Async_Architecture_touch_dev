import abc
import datetime

from src.core.queue.models import BEvent, StreamEvent
from src.core.services.abstract_service import AbstractService
from src.core.services.auth_service import AuthService
from src.core.services.models import User, TaskInService, AccountRowInService


class AuthEventService(AbstractService):

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()

    async def process_business_event(self, event: BEvent):
        ...

    async def process_stream_event(self, event: StreamEvent):
        if event.name == 'UserCreated':
            popug = self.auth_service.get_popug(event.public_id)
            if popug:
                self.user_repository.add(User(
                    role=popug.role, email=popug.email, public_id=event.public_id)
                )


class TaskTrackerEventService(AbstractService):

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()

    async def process_business_event(self, event: BEvent):
        match event.name:
            case 'TaskAssigned':
                # to do: assuming it is already updated in our db
                task = self.task_repository.get_task(event.public_id)
                popug = self.user_repository.get_popug_info(task.popug_public_id)
                # update current account
                current_account = popug.current_account - task.assigning_cost
                self.user_repository.update_account(popug.public_id, current_account)
                # insert a row into the account_log
                self.account_service.add(
                    AccountRowInService(
                        popug_public_id=popug.public_id,
                        task_public_id=task.public_id,
                        payment=(-1)*task.assigning_cost
                    )
                )
            case 'TaskDone':
                # to do: assuming it is already updated in our db
                task = self.task_repository.get_task(event.public_id)
                popug = self.user_repository.get_popug_info(task.popug_public_id)
                # update current account
                current_account = popug.current_account + task.price
                self.user_repository.update_account(popug.public_id, current_account)
                # insert a row into the account_log
                self.account_service.add(
                    AccountRowInService(
                        popug_public_id=popug.public_id,
                        task_public_id=task.public_id,
                        payment=task.price
                    )
                )
            case _:
                pass

    async def process_stream_event(self, event: StreamEvent):
        match event.name:
            case 'TaskCreated':
                task = self.auth_service.get_task(event.public_id)
                if task:
                    self.task_repository.add(TaskInService(
                            description=task.description,
                            status=task.status,
                            popug_public_id=task.popug_public_id,
                            public_id=task.public_id,
                        )
                    )
            case 'TaskUpdated':
                task = self.auth_service.get_task(event.public_id)
                if task:
                    self.task_repository.update(TaskInService(
                            description=task.description,
                            status=task.status,
                            popug_public_id=task.popug_public_id,
                            public_id=task.public_id,
                        )
                    )
            case _:
                pass

