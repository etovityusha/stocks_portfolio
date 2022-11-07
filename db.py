from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


def _get_engine(_dsn: str):
    return create_engine(_dsn)


@lru_cache()
def get_session_maker(_dsn: str) -> sessionmaker:
    engine = _get_engine(_dsn)
    return sessionmaker(engine, expire_on_commit=False)


def get_db():
    db = get_session_maker()()
    try:
        yield db
    finally:
        db.close()
