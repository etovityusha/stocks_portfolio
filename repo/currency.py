import abc

from sqlalchemy import update

from domain.base import BaseEntity
from domain.currency import Currency
from models.currency import CurrencyORM
from repo.base import SqlAlchemyRepo, FakeRepo, AbstractRepo


class CurrencyAbstractRepo(AbstractRepo):
    entity = Currency

    @abc.abstractmethod
    def update(self, _id: int, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def create_new(self, code: str, name: str) -> Currency:
        raise NotImplementedError


class CurrencySqlalchemyRepo(SqlAlchemyRepo, CurrencyAbstractRepo):
    _orm_model = CurrencyORM

    def update(self, _id: int, code: str | None = None, name: str | None = None) -> bool:
        qry = update(self._orm_model).where(self._orm_model.id == _id)
        if code is not None:
            qry = qry.values(code=code)
        if name is not None:
            qry = qry.values(name=name)
        self.session.execute(qry)
        return True

    def create_new(self, code: str, name: str) -> BaseEntity:
        currency = CurrencyORM(code=code, name=name)
        self.session.add(currency)
        return self.entity.from_orm(currency)


class CurrencyFakeRepo(FakeRepo, CurrencyAbstractRepo):
    entity = Currency

    def create_new(self, code: str, name: str) -> Currency:
        obj = Currency(code=code, name=name, id=self._get_next_id())
        self.objects.append(obj)
        return obj
