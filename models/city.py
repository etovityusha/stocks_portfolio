import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base import BaseModelORM


class CityORM(BaseModelORM):
    __tablename__ = "city"

    name = sa.Column(sa.String, nullable=False)
    country_id = sa.Column(sa.Integer, sa.ForeignKey("country.id"), nullable=False)
    country = relationship("CountryORM", back_populates="cities")
    population = sa.Column(sa.Integer, nullable=True)
