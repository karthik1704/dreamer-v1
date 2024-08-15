from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from .settings import DEBUG, db_config


def get_database_url():
    if DEBUG:
        return f"postgresql+psycopg://postgres:postgres@localhost/dreamer"
    else:

        return f"postgresql+psycopg://{db_config['username']}:{db_config['password']}@{db_config['host']}/{db_config['db_name']}"


SQLALCHEMY_DATABASE_URL = get_database_url()


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    # echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

# Async engine and session creation
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
AsyncSessionFactory = async_sessionmaker(
    async_engine, autoflush=False, expire_on_commit=False
)


async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
