from domain.base import BaseEntity
from domain.country import Country


class City(BaseEntity):
    name: str
    country: Country
    population: int | None = None
