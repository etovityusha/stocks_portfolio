import abc

from models.currency import CurrencyORM
from repo.currency import CurrencySqlalchemyRepo, CurrencyAbstractRepo, CurrencyObj, CurrencyFakeRepo


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
        self.session = self.session_factory()
        self.currency_repo = CurrencySqlalchemyRepo(self.session, CurrencyORM, CurrencyObj)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.currency_repo = CurrencyFakeRepo()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
