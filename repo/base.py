from abc import abstractmethod
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.base import BaseModelORM


class BaseRepo:
    _orm_model: Type[BaseModelORM] = None

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def create_new(self, **kwargs):
        pass

    @abstractmethod
    def find(self, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, _id: int):
        pass

    def _get_by_id(self, _id: int):
        statement = select(self._orm_model).where(self._orm_model.id == _id)
        return self.session.scalars(statement).first()
