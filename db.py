from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.unit_of_work import (
    AbstractUnitOfWork,
    SqlAlchemyUnitOfWork,
    FakeUnitOfWork,
)
from settings import get_settings, UnitOfWorkEnum


def _get_engine(_dsn: str):
    return create_engine(_dsn)


@lru_cache()
def get_session_maker(_dsn: str) -> sessionmaker:
    engine = _get_engine(_dsn)
    return sessionmaker(engine, expire_on_commit=False)


def get_db():
    settings = get_settings()
    session = get_session_maker(settings.postgres_dsn)()
    try:
        yield session
    finally:
        session.close()


def get_unit_of_work() -> AbstractUnitOfWork:
    _value = get_settings().unit_of_work
    settings = get_settings()
    if _value == UnitOfWorkEnum.postgres:
        return SqlAlchemyUnitOfWork(session_factory=get_session_maker(settings.postgres_dsn))
    if _value == UnitOfWorkEnum.fake:
        return FakeUnitOfWork()
    else:
        raise ValueError("Unknown unit of work")
