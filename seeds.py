from db import get_session_maker
from domain.currency import Currency
from domain.city import City
from domain.country import Country
from domain.sector import Sector

from models.currency import CurrencyORM
from models.city import CityORM
from models.country import CountryORM
from models.sector import SectorORM

usd = Currency(name="US Dollar", code="USD")
eur = Currency(name="Euro", code="EUR")
gbp = Currency(name="British Pound", code="GBP")
chf = Currency(name="Swiss Franc", code="CHF")
rub = Currency(name="Russian Ruble", code="RUB")

currencies = [usd, eur, gbp, chf, rub]


counties = [
    Country(name="United States", code="USA", currency=currencies[0]),
    Country(name="United Kingdom", code="GBR", currency=currencies[2]),
    Country(name="Switzerland", code="CHE", currency=currencies[3]),
    Country(name="Germany", code="DEU", currency=currencies[1]),
    Country(name="France", code="FRA", currency=currencies[1]),
    Country(name="Italy", code="ITA", currency=currencies[1]),
    Country(name="Spain", code="ESP", currency=currencies[1]),
    Country(name="Netherlands", code="NLD", currency=currencies[1]),
    Country(name="Russia", code="RUS", currency=currencies[4]),
]

cities = [
    City(name="New York", country=counties[0]),
    City(name="London", country=counties[1]),
    City(name="Zurich", country=counties[2]),
    City(name="Frankfurt", country=counties[3]),
    City(name="Paris", country=counties[4]),
    City(name="Milan", country=counties[5]),
    City(name="Madrid", country=counties[6]),
    City(name="Amsterdam", country=counties[7]),
    City(name="Moscow", country=counties[8]),
]

sectors = [
    Sector(title_en="Basic Materials", title_ru="Базовые материалы"),
    Sector(title_en="Communication Services", title_ru="Связь"),
    Sector(title_en="Consumer Cyclical", title_ru="Потребительский циклический"),
    Sector(title_en="Consumer Defensive", title_ru="Потребительский защитный"),
    Sector(title_en="Energy", title_ru="Энергетика"),
    Sector(title_en="Financial Services", title_ru="Финансовые услуги"),
    Sector(title_en="Healthcare", title_ru="Здравоохранение"),
    Sector(title_en="Industrials", title_ru="Промышленность"),
    Sector(title_en="Real Estate", title_ru="Недвижимость"),
    Sector(title_en="Technology", title_ru="Технологии"),
    Sector(title_en="Utilities", title_ru="Утилиты"),
]

session = get_session_maker("postgresql://postgres:postgres@127.0.0.1:8001/postgres")()
for cc in currencies:
    session.add(CurrencyORM(name=cc.name, code=cc.code))
session.commit()
for c in counties:
    session.add(CountryORM(name=c.name, code=c.code, currency=c.currency))
session.commit()
for c in cities:
    session.add(CityORM(name=c.name, country_id=c.country.id))
session.commit()
for s in sectors:
    session.add(SectorORM(name=s.name))
session.commit()
