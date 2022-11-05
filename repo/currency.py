import abc

from sqlalchemy import update

from models.currency import CurrencyORM
from repo.base import SqlAlchemyRepo, FakeRepo, BaseEntity, AbstractRepo


class CurrencyObj(BaseEntity):
    code: str
    name: str


class CurrencyAbstractRepo(AbstractRepo):
    entity = CurrencyObj

    @abc.abstractmethod
    def update(self, _id: int, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def create_new(self, code: str, name: str) -> CurrencyObj:
        raise NotImplementedError


class CurrencySqlalchemyRepo(SqlAlchemyRepo, CurrencyAbstractRepo):
    _orm_model = CurrencyORM

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
    entity = CurrencyObj

    def create_new(self, code: str, name: str) -> CurrencyObj:
        obj = CurrencyObj(code=code, name=name, id=None)
        self.objects.append(obj)
        return obj
