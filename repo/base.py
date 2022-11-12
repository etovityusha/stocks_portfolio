import abc
from abc import abstractmethod
from typing import Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.base import BaseEntity
from models.base import BaseModelORM


class AbstractRepo(abc.ABC):
    entity: Type[BaseEntity] = None

    @abstractmethod
    def __init__(self, entity: Type[entity]):
        self.entity = entity

    @abstractmethod
    def get_by_id(self, _id: int) -> entity:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[entity]:
        raise NotImplementedError

    @abstractmethod
    def find_by(self, **kwargs) -> list[entity]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, _id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def update(self, _id: int, **kwargs) -> int:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def exists(self, _id: int) -> bool:
        raise NotImplementedError


class SqlAlchemyRepo(AbstractRepo):
    _orm_model: Type[BaseModelORM]
    entity: Type[BaseEntity]

    def __init__(self, session: Session, orm_model: Type[BaseModelORM], entity: Type[BaseEntity]):
        self.session = session
        self._orm_model = orm_model
        super().__init__(entity)

    def get_by_id(self, _id: int) -> BaseEntity | None:
        statement = select(self._orm_model).where(self._orm_model.id == _id)
        if orm_obj := self.session.execute(statement).scalar_one_or_none():
            return self.entity.from_orm(orm_obj)
        return None

    def find_all(self) -> list[BaseEntity]:
        objects = self.session.execute(select(self._orm_model)).scalars().all()
        return [self.entity.from_orm(x) for x in objects]

    def find_by(self, **kwargs) -> list[BaseEntity]:
        return [
            self.entity.from_orm(x)
            for x in self.session.execute(select(self._orm_model).where_by(**kwargs)).scalars().all()
        ]

    def delete_by_id(self, _id: int) -> int:
        return int(self._orm_model.query.filter_by(id=_id).delete())

    def update(self, _id: int, **kwargs) -> int:
        return int(self._orm_model.query.filter_by(id=_id).update(kwargs))

    def count(self) -> int:
        return self._orm_model.query.count()

    def exists(self, _id: int) -> bool:
        return self._orm_model.query.filter_by(id=_id).count() > 0


class FakeRepo(AbstractRepo):
    entity = BaseEntity

    def __init__(self, objects: list[BaseEntity] = None):
        self.objects = [] if objects is None else objects
        super().__init__(self.entity)

    def get_by_id(self, _id: int) -> BaseEntity | None:
        return next((obj for obj in self.objects if obj.id == _id), None)

    def find_all(self) -> list[BaseModel]:
        return list(self.objects)

    def find_by(self, **kwargs) -> list[BaseModel]:
        return [obj for obj in self.objects if all(getattr(obj, k) == v for k, v in kwargs.items())]

    def delete_by_id(self, _id: int) -> int:
        length = len(self.objects)
        self.objects = [obj for obj in self.objects if obj.id != _id]
        return length - len(self.objects)

    def update(self, _id: int, **kwargs) -> int:
        for_update = [obj for obj in self.objects if obj.id == _id]
        for obj in for_update:
            if obj.id == _id:
                for k, v in kwargs.items():
                    setattr(obj, k, v)
        return len(for_update)

    def count(self) -> int:
        return len(self.objects)

    def exists(self, _id: int) -> bool:
        return any(obj.id == _id for obj in self.objects)

    def _get_next_id(self) -> int:
        return max((obj.id for obj in self.objects), default=0) + 1
