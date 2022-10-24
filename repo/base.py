from typing import Type

from sqlalchemy.orm import Session

from models.base import BaseModelORM


class BaseRepo:
    _orm_model: Type[BaseModelORM] = None

    def __init__(self, session: Session):
        self.session = session
