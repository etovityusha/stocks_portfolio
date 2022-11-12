import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base import BaseModelORM


class Industry(BaseModelORM):
    __tablename__ = "industry"

    title_en = sa.Column(sa.String, nullable=False)
    title_ru = sa.Column(sa.String, nullable=False)
    logo_url = sa.Column(sa.String, nullable=True)
    sector_id = sa.Column(sa.Integer, sa.ForeignKey("sector.id"), nullable=False)
    sector = relationship("SectorORM")
