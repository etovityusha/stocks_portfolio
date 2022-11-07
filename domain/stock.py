from pydantic import Field

from domain.currency import Currency
from domain.base import BaseEntity
from domain.city import City
from domain.exchange import Exchange
from domain.industry import Industry


class Stock(BaseEntity):
    exchange: Exchange
    isin: str = Field(min_length=12, max_length=12)
    ticker: str
    name: str
    currency: Currency
    city: City
    address: str | None = None
    industry: Industry

    logo_url: str | None = None
    website: str | None = None
    full_time_employees: int | None = None
