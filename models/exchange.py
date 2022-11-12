import sqlalchemy as sa

from models.base import BaseModelORM


class ExchangeORM(BaseModelORM):
    __tablename__ = "exchange"

    title = sa.Column(sa.String, nullable=False)
    suffix = sa.Column(sa.String, nullable=False)

    utc_offset = sa.Column(sa.Integer, nullable=True)
    open_time = sa.Column(sa.Time, nullable=True)
    close_time = sa.Column(sa.Time, nullable=True)
