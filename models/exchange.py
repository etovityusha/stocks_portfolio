import sqlalchemy as sa

from models.base import BaseModelORM


class ExchangeORM(BaseModelORM):
    __tablename__ = "exchange"

    title = sa.Column(sa.String, nullable=False)
    suffix = sa.Column(sa.String, nullable=False)

    utc_offset = sa.Column(sa.Integer, nullable=True)
    working_start = sa.Column(sa.Time, nullable=True)
    working_end = sa.Column(sa.Time, nullable=True)
