from sqlalchemy import text
from sqlalchemy.orm import Session

from repo.currency import CurrencyRepo, CurrencyObj


def test_repo_get_by_id(session: Session) -> None:
    session.execute(text("INSERT INTO currency (name, code) VALUES ('ruble', 'RUB')"))
    session.commit()

    repo = CurrencyRepo(session=session)
    assert repo.get_by_id(1) == CurrencyObj(id=1, name="ruble", code="RUB")


def test_repo_update(session: Session) -> None:
    session.execute(text("INSERT INTO currency (name, code) VALUES ('ruble', 'RUB')"))
    session.commit()

    repo = CurrencyRepo(session=session)
    repo.update(_id=1, name="US DOLLAR")

    assert repo.get_by_id(1) == CurrencyObj(id=1, name="US DOLLAR", code="RUB")

    repo.update(_id=1, code="USD")
    assert repo.get_by_id(1) == CurrencyObj(id=1, name="US DOLLAR", code="USD")

    repo.update(_id=1, code="EUR", name="euro")
    assert repo.get_by_id(1) == CurrencyObj(id=1, name="euro", code="EUR")
