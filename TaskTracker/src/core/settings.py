from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename: str = 'popug.log'
    log_level: str = 'INFO'

    SECRET_KEY: str = "ea3dc753ae38919e81362d39cf6d6d03b6a82d2168e97d3f50a72a132c98a7cf"
    ALGORITHM: str = "HS256"

    auth_host: str = 'auth'
    workers_url: str = '/workers'
    popug_url: str = '/popug'
    internal_url: str = '/popug/internal/{public_id}'
    auth_secret: str = 'sejhjkbfhhv'
    auth_login_url: str = '/token'

    @property
    def get_auth_login(self):
        return f'{self.auth_host}{self.auth_login_url}'

    rabbitmq_host: str = 'rabbitmq'
    rabbitmq_port: str = '5672'
    rabbitmq_default_user: str = 'user'
    rabbitmq_default_pass: str = 'pass'
    rabbitmq_queue_be: str = 'task_lifecycle.be'
    rabbitmq_queue_stream: str = 'task_lifecycle.stream'
    rabbitmq_queue_consume_be: str = 'user_lifecycle.be'
    rabbitmq_queue_consume_stream: str = 'user_lifecycle.stream'

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
