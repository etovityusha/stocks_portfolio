from enum import Enum

from cachetools.func import lru_cache
from pydantic import BaseSettings, validator

from db import get_db
from services.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork, FakeUnitOfWork


class LoggerLevelEnum(Enum):
    debug = "debug"
    info = "info"
    warning = "warning"


class UnitOfWorkEnum(Enum):
    postgres = "postgres"
    fake = "fake"
    mongodb = "mongodb"


class Settings(BaseSettings):
    app_name: str = "stocks portfolio"
    listen_host: str
    listen_port: int
    logger_level: LoggerLevelEnum
    unit_of_work: UnitOfWorkEnum

    postgres_host: str | None = None
    postgres_port: int | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_db: str | None = None

    @validator("is_postgres_enabled", check_fields=False)
    def validate_postgres_settings(cls, v, values):
        if values["unit_of_work"] == UnitOfWorkEnum.postgres:
            if not all(
                [
                    values["postgres_host"],
                    values["postgres_port"],
                    values["postgres_user"],
                    values["postgres_password"],
                    values["postgres_db"],
                ]
            ):
                raise ValueError("Postgres settings are not set")

    @property
    def postgres_dsn(self):
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_prefix = "API_"
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


def get_unit_of_work(_settings: Settings) -> AbstractUnitOfWork:
    _val: UnitOfWorkEnum = _settings.unit_of_work
    if _val == UnitOfWorkEnum.postgres:
        return SqlAlchemyUnitOfWork(session_factory=get_db)
    if _val == UnitOfWorkEnum.fake:
        return FakeUnitOfWork()
    if _val == UnitOfWorkEnum.mongodb:
        raise NotImplementedError
    else:
        raise ValueError("Unknown unit of work")
