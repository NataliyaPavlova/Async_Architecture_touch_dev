from pathlib import Path

from pydantic import BaseSettings
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename = 'popug.log'

    log_level: str = 'INFO'

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

    db_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    db_port: int

    @property
    def database_url(self):
        """Получить ссылку для подключения к DB."""
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ENV_FILE


@lru_cache()
def get_settings():
    return Settings()
