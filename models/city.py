import sqlalchemy as sa

from models.base import BaseModelORM


class CityORM(BaseModelORM):
    __tablename__ = "city"

    name = sa.Column(sa.String, nullable=False)
    country_id = sa.Column(sa.Integer, sa.ForeignKey("country.id"), nullable=False)
    population = sa.Column(sa.Integer, nullable=True)
