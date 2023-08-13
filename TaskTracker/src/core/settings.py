from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename: str = 'popug.log'

    log_level: str = 'INFO'

    auth_host: str = 'https://0.0.0.0:8888/api'
    workers_url: str = '/workers'
    popug_url: str = '/popug'
    auth_login_url: str = '/token'

    @property
    def get_auth_login(self):
        return f'{self.auth_host}{self.auth_login_url}'

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_queue: str

    @property
    def rabbit_url(self):
        return (
            f'amqp://{self.rabbitmq_default_user}:'
            f'{self.rabbitmq_default_pass}@{self.rabbitmq_host}:'
            f'{self.rabbitmq_port}/'
        )

    class Config:
        env_file = ENV_FILE


settings = Settings()
