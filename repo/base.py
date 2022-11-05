import abc
from abc import abstractmethod
from typing import Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.base import BaseModelORM


class BaseEntity(BaseModel):
    id: int | None


class AbstractRepo(abc.ABC):
    entity: Type[BaseEntity] = None

    @abstractmethod
    def __init__(self, entity: Type[BaseEntity]):
        self.entity = entity

    @abstractmethod
    def get_by_id(self, _id: int) -> BaseEntity:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[BaseEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by(self, **kwargs) -> list[BaseEntity]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, _id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, _id: int, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def exists(self, _id: int) -> bool:
        raise NotImplementedError


class SqlAlchemyRepo(AbstractRepo):
    _orm_model: Type[BaseModelORM] = None
    entity: Type[BaseEntity]

    def __init__(self, session: Session, orm_model: Type[BaseModelORM], entity: Type[BaseEntity]):
        self.session = session
        self._orm_model = orm_model
        super().__init__(entity)

    def get_by_id(self, _id: int):
        statement = select(self._orm_model).where(self._orm_model.id == _id)
        return self.entity.from_orm(self.session.execute(statement).scalar_one())

    def find_all(self):
        return [self.entity.from_orm(x) for x in self._orm_model.query.all()]

    def find_by(self, **kwargs):
        return [self.entity.from_orm(x) for x in self._orm_model.query.filter_by(**kwargs).all()]

    def delete_by_id(self, _id: int):
        self._orm_model.query.filter_by(id=_id).delete()

    def update(self, _id: int, **kwargs):
        self._orm_model.query.filter_by(id=_id).update(kwargs)

    def count(self) -> int:
        return self._orm_model.query.count()

    def exists(self, _id: int) -> bool:
        return self._orm_model.query.filter_by(id=_id).count() > 0


class FakeRepo(AbstractRepo):
    def __init__(self, entity: Type[BaseModel], objects: list[BaseModel] = None):
        if objects is None:
            self.objects = []
        else:
            self.objects = objects
        super().__init__(entity)

    def get_by_id(self, _id: int) -> BaseModel:
        for obj in self.objects:
            if obj.id == _id:
                return obj

    def find_all(self) -> list[BaseModel]:
        return list(self.objects)

    def find_by(self, **kwargs) -> list[BaseModel]:
        return [obj for obj in self.objects if all(getattr(obj, k) == v for k, v in kwargs.items())]

    def delete_by_id(self, _id: int):
        for obj in self.objects:
            if obj.id == _id:
                self.objects.remove(obj)

    def update(self, _id: int, **kwargs):
        for obj in self.objects:
            if obj.id == _id:
                for k, v in kwargs.items():
                    setattr(obj, k, v)

    def count(self) -> int:
        return len(self.objects)

    def exists(self, _id: int) -> bool:
        return any(obj.id == _id for obj in self.objects)
