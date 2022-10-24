from pydantic import BaseModel
from sqlalchemy import select, update

from models.currency import CurrencyORM
from repo.base import BaseRepo


class CurrencyObj(BaseModel):
    id: int | None
    code: str
    name: str

    class Config:
        orm_mode = True


class CurrencyRepo(BaseRepo):
    _orm_model = CurrencyORM

    def get_by_id(self, _id: int) -> CurrencyObj:
        statement = select(self._orm_model).where(self._orm_model.id == _id)
        result = self.session.scalars(statement).first()
        return CurrencyObj.from_orm(result)

    def find(self) -> list[CurrencyObj]:
        qs = self.session.scalars(select(self._orm_model)).all()
        return [CurrencyObj.from_orm(x) for x in qs]

    def update(
        self, _id: int, code: str | None = None, name: str | None = None
    ) -> bool:
        qry = update(self._orm_model).where(self._orm_model.id == _id)
        if code is not None:
            qry = qry.values(code=code)
        if name is not None:
            qry = qry.values(name=name)
        self.session.execute(qry)
        self.session.commit()
        return True
