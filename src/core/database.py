"""Setup the Database and support functions."""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings

settings = get_settings()

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)


async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)



async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """Return the database connection as a Generator."""
    async with async_session_factory() as session:
        yield session