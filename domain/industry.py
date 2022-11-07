from domain.base import BaseEntity
from domain.sector import Sector


class Industry(BaseEntity):
    title_en: str
    title_ru: str
    sector: Sector
    logo_url: str | None = None
