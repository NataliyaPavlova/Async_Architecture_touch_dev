from http.client import HTTPSConnection

from src.core.settings import settings
from src.core.services.models import User


class AuthService:

    def get_user(self) -> User:
        with HTTPSConnection(settings.auth_host) as connection:
            headers = {'Content-type': 'application/json'}
            connection.request('GET', settings.popug_url, headers)
            response = connection.getresponse()
            popug = response.read().decode()
        return User(
            username=popug['username'],
            role=popug['role'],
            email=popug['email'],
        )

    def get_workers_auth(self, headers: dict) -> dict:
        with HTTPSConnection(settings.auth_host) as connection:
            headers['Content-type'] = 'application/json'
            connection.request('GET', settings.get_workers_url, headers)
            response = connection.getresponse()
            workers = response.read().decode()
        return workers

