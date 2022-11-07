"""stocks

Revision ID: 7318582dfea1
Revises: cf6734a2f551
Create Date: 2022-11-06 15:22:04.878298

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7318582dfea1"
down_revision = "cf6734a2f551"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "exchange",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("suffix", sa.String(), nullable=False),
        sa.Column("utc_offset", sa.Integer(), nullable=True),
        sa.Column("working_start", sa.Time(), nullable=True),
        sa.Column("working_end", sa.Time(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "industry",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title_en", sa.String(), nullable=False),
        sa.Column("title_ru", sa.String(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sector",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title_en", sa.String(), nullable=False),
        sa.Column("title_ru", sa.String(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "country",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(length=3), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currency.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "city",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("population", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["country.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stock",
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("exchange_id", sa.Integer(), nullable=False),
        sa.Column("isin", sa.String(length=12), nullable=False),
        sa.Column("ticker", sa.String(length=8), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("sector_id", sa.Integer(), nullable=False),
        sa.Column("industry_id", sa.Integer(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("full_time_employees", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["city.id"],
        ),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["exchange_id"],
            ["exchange.id"],
        ),
        sa.ForeignKeyConstraint(
            ["industry_id"],
            ["industry.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sector_id"],
            ["sector.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("isin"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stock")
    op.drop_table("city")
    op.drop_table("country")
    op.drop_table("sector")
    op.drop_table("industry")
    op.drop_table("exchange")
    # ### end Alembic commands ###
