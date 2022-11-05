from domain.base import BaseEntity


class Currency(BaseEntity):
    code: str
    name: str
