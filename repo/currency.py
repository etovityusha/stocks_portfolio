import abc

from pydantic import BaseModel
from sqlalchemy import select, update

from models.currency import CurrencyORM
from repo.base import SqlAlchemyRepo, FakeRepo


class CurrencyObj(BaseModel):
    id: int | None
    code: str
    name: str

    class Config:
        orm_mode = True

class CurrencyAbstractRepo(abc.ABC):
    @abc.abstractmethod
    def update(self, _id: int, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def create_new(self, code: str, name: str) -> CurrencyObj:
        raise NotImplementedError


class CurrencySqlalchemyRepo(SqlAlchemyRepo):
    _orm_model = CurrencyORM
    entity = CurrencyObj

    def update(self, _id: int, code: str | None = None, name: str | None = None) -> bool:
        qry = update(self._orm_model).where(self._orm_model.id == _id)
        if code is not None:
            qry = qry.values(code=code)
        if name is not None:
            qry = qry.values(name=name)
        self.session.execute(qry)
        return True

    def create_new(self, code: str, name: str) -> CurrencyObj:
        currency = CurrencyORM(code=code, name=name)
        self.session.add(currency)
        return self.entity.from_orm(currency)

class CurrencyFakeRepo(FakeRepo):
    def create_new(self, code: str, name: str):
        self.objects.add(
            CurrencyObj(

        )

