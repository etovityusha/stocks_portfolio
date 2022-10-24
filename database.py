from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from environs import Env

env = Env()
env.read_env()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{env.str('API_POSTGRES_USER')}:"
    f"{env.str('API_POSTGRES_PASSWORD')}@"
    f"{env.str('API_POSTGRES_HOST')}:"
    f"{env.str('API_POSTGRES_PORT')}/"
    f"{env.str('API_POSTGRES_DB')}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()
