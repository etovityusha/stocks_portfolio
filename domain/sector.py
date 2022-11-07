from domain.base import BaseEntity


class Sector(BaseEntity):
    title_en: str
    title_ru: str
    logo_url: str | None = None
