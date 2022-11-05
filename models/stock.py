import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base import BaseModelORM


class StockORM(BaseModelORM):
    __tablename__ = "stock"

    exchange = relationship("ExchangeORM", back_populates="stocks")
    exchange_id = sa.Column(sa.Integer, sa.ForeignKey("exchange.id"), nullable=False)

    isin = sa.Column(sa.String(12), nullable=False, unique=True)
    ticker = sa.Column(sa.String(8), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey("currency.id"), nullable=False)
    currency = relationship("CurrencyORM", back_populates="stocks")
    city = relationship("CityORM", back_populates="stocks")
    city_id = sa.Column(sa.Integer, sa.ForeignKey("city.id"), nullable=False)
    address = sa.Column(sa.String, nullable=False)
    sector_id = sa.Column(sa.Integer, sa.ForeignKey("sector.id"), nullable=False)
    sector = relationship("Sector", back_populates="stocks")
    industry_id = sa.Column(sa.Integer, sa.ForeignKey("industry.id"), nullable=False)
    industry = relationship("Industry", back_populates="stocks")

    logo_url = sa.Column(sa.String, nullable=True)
    website = sa.Column(sa.String, nullable=True)
    full_time_employees = sa.Column(sa.Integer, nullable=True)
