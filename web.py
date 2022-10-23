import uvicorn
from fastapi import FastAPI

from config import get_settings


def create_app() -> FastAPI:
    """Fastapi factory"""
    fastapi_app = FastAPI()
    return fastapi_app


app = create_app()
settings = get_settings()

if __name__ == "__main__":
    _host = settings.listen_host
    _port = settings.listen_port
    uvicorn.run("web:app", host=_host, port=_port, reload=True)
