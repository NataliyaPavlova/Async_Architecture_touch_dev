from http.client import HTTPSConnection
import jwt

from src.core.settings import settings
from src.core.services.models import User, TaskInService
from src.core.services.abstract_service import AbstractService


class AuthService(AbstractService):

    def get_user(self, auth_header: str) -> User | None:
        try:
            payload = jwt.decode(auth_header, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            public_id: str = payload.get("sub")
            if public_id is None:
                return None
        except jwt.InvalidTokenError:
            return None
        popug = self.user_repository.get(public_id=public_id)
        return User(
            role=popug['role'],
            email=popug['email'],
            public_id=popug['public_id'],
        )

    def get_popug_info(self) -> User:
        with HTTPSConnection(settings.auth_host) as connection:
            headers = {'Content-type': 'application/json', 'X-Secret': f'Base {settings.auth_secret}'}
            connection.request('GET', settings.internal_url, headers)
            response = connection.getresponse()
            popug = response.read().decode()
        return User(
            role=popug['role'],
            email=popug['email'],
            public_id=popug['public_id'],
        )

    def get_task(self) -> TaskInService:
        with HTTPSConnection(settings.tasktracker_host) as connection:
            headers = {'Content-type': 'application/json', 'X-Secret': f'Base {settings.tasktracker_secret}'}
            connection.request('GET', settings.task_internal_url, headers)
            response = connection.getresponse()
            task = response.read().decode()
        return TaskInService(
            description=task.description,
            status=task.status,
            popug_public_id=task.popug_public_id,
            public_id=task.public_id,
        )



