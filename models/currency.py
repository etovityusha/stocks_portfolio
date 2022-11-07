import sqlalchemy as sa

from models.base import BaseModelORM


class CurrencyORM(BaseModelORM):
    __tablename__ = "currency"

    name = sa.Column(sa.String, nullable=False)
    code = sa.Column(sa.String(3), nullable=False)
