import uvicorn
from fastapi import FastAPI

from api.router import api_router
from db import get_unit_of_work
from services.unit_of_work import AbstractUnitOfWork
from settings import get_settings


def create_app() -> FastAPI:
    """Fastapi factory"""
    fastapi_app = FastAPI()
    fastapi_app.include_router(api_router)
    fastapi_app.dependency_overrides[AbstractUnitOfWork] = get_unit_of_work
    return fastapi_app


app = create_app()

if __name__ == "__main__":
    _settings = get_settings()
    _host = _settings.listen_host
    _port = _settings.listen_port
    uvicorn.run("web:app", host=_host, port=_port, reload=True)
