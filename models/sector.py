import sqlalchemy as sa

from models.base import BaseModelORM


class SectorORM(BaseModelORM):
    __tablename__ = "sector"

    title_en = sa.Column(sa.String, nullable=False)
    title_ru = sa.Column(sa.String, nullable=False)
    logo_url = sa.Column(sa.String, nullable=True)
