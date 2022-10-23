from enum import Enum

from cachetools.func import lru_cache
from pydantic import BaseSettings


class LoggerLevel(Enum):
    debug = "debug"
    info = "info"
    warning = "warning"


class Settings(BaseSettings):
    app_name: str = "stocks portfolio"
    listen_host: str
    listen_port: int
    logger_level: LoggerLevel

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_prefix = "API_"
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
