import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base import BaseModelORM


class Industry(BaseModelORM):
    __tablename__ = "industry"

    title_en = sa.Column(sa.String, nullable=False)
    title_ru = sa.Column(sa.String, nullable=False)
    sector = relationship("Sector", back_populates="industries")
    stocks = relationship("StockORM", back_populates="industry")
    logo_url = sa.Column(sa.String, nullable=True)
