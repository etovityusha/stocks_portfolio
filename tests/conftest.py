import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, drop_database
from starlette.testclient import TestClient

from models.base import meta
from services.unit_of_work import AbstractUnitOfWork, FakeUnitOfWork
from web import create_app


TESTING_DATABASE_URL = f"postgresql://postgres:postgres@localhost:5432/stocks_portfolio_test_{uuid.uuid4()}"


@pytest.fixture()
def test_session_maker() -> sessionmaker:
    create_database(TESTING_DATABASE_URL)
    try:
        engine = create_engine(TESTING_DATABASE_URL)
        testing_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        meta.create_all(bind=engine)
        yield testing_session_maker
    finally:
        drop_database(TESTING_DATABASE_URL)


@pytest.fixture()
def session(test_session_maker) -> Session:
    session = test_session_maker()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def test_client() -> TestClient:
    fastapi_app = create_app()
    fastapi_app.dependency_overrides[AbstractUnitOfWork] = lambda: FakeUnitOfWork()
    with TestClient(fastapi_app) as client:
        yield client
