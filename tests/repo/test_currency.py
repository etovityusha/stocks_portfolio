import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from domain.currency import Currency
from models.currency import CurrencyORM
from repo.currency import CurrencySqlalchemyRepo


@pytest.fixture()
def repo(session: Session):
    yield CurrencySqlalchemyRepo(session=session, orm_model=CurrencyORM, entity=Currency)


def test_repo_get_by_id(session: Session, repo: CurrencySqlalchemyRepo) -> None:
    repo.session.execute(text("INSERT INTO currency (name, code) VALUES ('ruble', 'RUB')"))
    repo.session.commit()
    assert repo.get_by_id(1) == Currency(id=1, name="ruble", code="RUB")


def test_repo_update(session: Session, repo: CurrencySqlalchemyRepo) -> None:
    repo.session.execute(text("INSERT INTO currency (name, code) VALUES ('ruble', 'RUB')"))
    repo.session.commit()

    repo.update(_id=1, name="US DOLLAR")
    assert repo.get_by_id(1) == Currency(id=1, name="US DOLLAR", code="RUB")

    repo.update(_id=1, code="USD")
    assert repo.get_by_id(1) == Currency(id=1, name="US DOLLAR", code="USD")

    repo.update(_id=1, code="EUR", name="euro")
    assert repo.get_by_id(1) == Currency(id=1, name="euro", code="EUR")


def test_repo_obj_create(session: Session, repo: CurrencySqlalchemyRepo) -> None:
    obj = repo.create_new(code="EUR", name="Euro")
    assert obj == Currency(id=None, name="Euro", code="EUR")
