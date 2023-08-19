from http.client import HTTPSConnection

from src.core.settings import settings
from src.core.services.models import User


class AuthService:

    def get_user(self, auth_header: str) -> User:
        with HTTPSConnection(settings.auth_host) as connection:
            headers = {'Content-type': 'application/json', 'Authorization': f'Bearer {auth_header}'}
            connection.request('GET', settings.popug_url, headers)
            response = connection.getresponse()
            popug = response.read().decode()
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


