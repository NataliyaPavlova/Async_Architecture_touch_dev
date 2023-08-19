from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    SECRET_KEY: str = "ea3dc753ae38919e81362d39cf6d6d03b6a82d2168e97d3f50a72a132c98a7cf"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    auth_secret: str = 'sejhjkbfhhv'

    rabbitmq_host: str = 'rabbitmq'
    rabbitmq_port: str = '5672'
    rabbitmq_default_user: str = 'guest'
    rabbitmq_default_pass: str = 'guest'
    rabbitmq_queue_be: str = 'user_lifecycle.be'
    rabbitmq_queue_stream: str = 'user_lifecycle.stream'

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
