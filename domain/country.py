from pydantic import Field

from domain.currency import Currency
from domain.base import BaseEntity


class Country(BaseEntity):
    name: str
    code: str = Field(min_length=3, max_length=3)
    currency: Currency
    logo_url: str | None = None
