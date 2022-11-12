import sqlalchemy as sa

from models.base import BaseModelORM


class StockTypeORM(BaseModelORM):
    __tablename__ = "stock_type"

    title_en = sa.Column(sa.String, nullable=False)
    title_ru = sa.Column(sa.String, nullable=False)
