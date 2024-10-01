from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from .settings import DEBUG, db_config


def get_database_url() -> str:
    # if DEBUG:
    #     return "postgresql+psycopg://postgres:postgres@localhost/dreamer"
    # else:
    return (
        f"postgresql+psycopg://{db_config['username']}:"
        f"{db_config['password']}@{db_config['host']}/"
        f"{db_config['db_name']}"
    )


SQLALCHEMY_DATABASE_URL = get_database_url()

# Create the async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    # echo=True,  # Uncomment this if you want SQLAlchemy to log SQL queries
)

# Async session factory
AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


# Dependency for FastAPI routes
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
