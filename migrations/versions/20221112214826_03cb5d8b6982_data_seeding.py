"""data seeding

Revision ID: d9c812c73c36
Revises: 824f7e2574d1
Create Date: 2022-11-12 19:29:33.232228

"""
import datetime

from alembic import op

# revision identifiers, used by Alembic.
revision = "d9c812c73c36"
down_revision = "06fa114f15cc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    currencies: list[tuple] = [
        ("USD", "US dollar"),
        ("EUR", "Euro"),
        ("RUB", "Russian Ruble"),
    ]
    cur = op.get_bind().connection.cursor()
    cur.execute(
        f"""
    INSERT INTO currency (code, name)
    VALUES {", ".join([f"('{code}', '{name}')" for code, name in currencies])}
    RETURNING id;
    """
    )
    _currency_ids: list[int] = [x[0] for x in cur.fetchall()]
    counties: list[tuple] = [
        ("USA", "USA", _currency_ids[0]),
        ("Russia", "RUS", _currency_ids[2]),
        ("Germany", "GER", _currency_ids[1]),
        ("France", "FRA", _currency_ids[1]),
        ("Italy", "ITA", _currency_ids[1]),
        ("Spain", "SPA", _currency_ids[1]),
    ]
    cur.execute(
        f"""
    INSERT INTO country (name, code, currency_id)
    VALUES {", ".join([f"('{name}', '{code}', {currency_id})" for name, code, currency_id in counties])}
    returning id;
    """
    )
    _countries_ids = [x[0] for x in cur.fetchall()]
    cities: list[tuple] = [
        ("New York", _countries_ids[0]),
        ("Moscow", _countries_ids[1]),
        ("Berlin", _countries_ids[2]),
        ("Paris", _countries_ids[3]),
        ("Rome", _countries_ids[4]),
        ("Madrid", _countries_ids[5]),
    ]
    cur.execute(
        f"""
    INSERT INTO city (name, country_id)
    VALUES {", ".join([f"('{name}', {country_id})" for name, country_id in cities])}
    returning id;
    """
    )
    _cities_ids = [x[0] for x in cur.fetchall()]

    stock_sectors: list[tuple] = [
        ("Technology", "Технологии"),
        ("Communication Services", "Связь"),
        ("Financial Services", "Финансы"),
        ("Healthcare", "Здравоохранение"),
        ("Basic Materials", "Базовые материалы"),
        ("Consumer Cyclical", "Потребительский циклический"),
        ("Consumer Defensive", "Потребительский защитный"),
        ("Energy", "Энергетика"),
        ("Industrials", "Промышленность"),
        ("Real Estate", "Недвижимость"),
        ("Utilities", "Коммунальные услуги"),
    ]
    cur.execute(
        f"""
    INSERT INTO sector (title_en, title_ru)
    VALUES {", ".join([f"('{name}', '{name_ru}')" for name, name_ru in stock_sectors])}
    returning id;
        """
    )
    _stock_sectors_ids = [x[0] for x in cur.fetchall()]
    exchanges: list[tuple] = [
        ("NASDAQ", "", -5, datetime.time(9, 30), datetime.time(16, 0)),
        ("NYSE", "", -5, datetime.time(9, 30), datetime.time(16, 0)),
        ("MOEX", ".ME", 3, datetime.time(10, 0), datetime.time(18, 30)),
    ]
    cur.execute(
        f"""
    INSERT INTO exchange (title, suffix, utc_offset, open_time, close_time)
    VALUES {", ".join([f"('{name}', '{suffix}', {timezone}, '{open_time}', '{close_time}')"
                       for name, suffix, timezone, open_time, close_time in exchanges])}
    returning id;
        """
    )
    _exchanges_ids = [x[0] for x in cur.fetchall()]
    stock_types: list[tuple] = [
        ("Common Stock", "Обыкновенные акции"),
        ("Preferred Stock", "Предпочтительные акции"),
        ("Warrant", "Варанты"),
        ("Unit", "Единицы"),
        ("Right", "Права"),
        ("ADR", "ADR"),
        ("ETF", "ETF"),
        ("REIT", "REIT"),
        ("Closed-End Fund", "Закрытые фонды"),
        ("Open-End Fund", "Открытые фонды"),
        ("Unit Investment Trust", "Единицы инвестиционных доверительных"),
        ("Limited Partnership", "Ограниченное партнерство"),
        ("Exchange Traded Fund", "ETF"),
        ("Real Estate Investment Trust", "REIT"),
    ]
    cur.execute(
        f"""
    INSERT INTO stock_type (title_en, title_ru)
    VALUES {", ".join([f"('{name}', '{name_ru}')" for name, name_ru in stock_types])}
    returning id;
        """
    )
    _stock_types_ids = [x[0] for x in cur.fetchall()]
    cur.close()


def downgrade() -> None:
    tables = (
        "stock",
        "stock_type",
        "exchange",
        "sector",
        "city",
        "country",
        "currency",
    )
    cur = op.get_bind().connection.cursor()
    for table in tables:
        cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
    cur.close()
