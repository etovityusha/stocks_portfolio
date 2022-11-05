import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base import BaseModelORM


class Sector(BaseModelORM):
    __tablename__ = "sector"

    title_en = sa.Column(sa.String, nullable=False)
    title_ru = sa.Column(sa.String, nullable=False)
    industries = relationship("Industry", back_populates="sector")
    stocks = relationship("StockORM", back_populates="sector")
    logo_url = sa.Column(sa.String, nullable=True)
