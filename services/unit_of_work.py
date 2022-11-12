import abc
from functools import lru_cache

from sqlalchemy.orm import Session

from domain.currency import Currency
from models.currency import CurrencyORM
from repo.currency import CurrencySqlalchemyRepo, CurrencyAbstractRepo, CurrencyFakeRepo


class AbstractUnitOfWork(abc.ABC):
    currency_repo: CurrencyAbstractRepo

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def currency_repo(self):
        return CurrencySqlalchemyRepo(self.session, CurrencyORM, Currency)


@lru_cache()
def get_fake_currency_repo():
    return CurrencyFakeRepo()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.committed = False
        self.currency_repo = get_fake_currency_repo()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
