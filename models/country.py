import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.base import BaseModelORM


class CountryORM(BaseModelORM):
    __tablename__ = "country"

    name = sa.Column(sa.String, nullable=False)
    code = sa.Column(sa.String(3), nullable=False, unique=True)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey("currency.id"), nullable=False)
    currency = relationship("CurrencyORM")
    logo_url = sa.Column(sa.String, nullable=True)

    def __repr__(self):
        return f"CountryORM(name={self.name}, code={self.code}, currency_id={self.currency_id})"
