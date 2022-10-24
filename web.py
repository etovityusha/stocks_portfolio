from enum import Enum

import uvicorn
from cachetools.func import lru_cache
from fastapi import FastAPI
from pydantic import BaseSettings

from api.router import api_router


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


def create_app() -> FastAPI:
    """Fastapi factory"""
    fastapi_app = FastAPI()
    fastapi_app.include_router(api_router)
    return fastapi_app


app = create_app()
settings = get_settings()

if __name__ == "__main__":
    _host = settings.listen_host
    _port = settings.listen_port
    uvicorn.run("web:app", host=_host, port=_port, reload=True)
