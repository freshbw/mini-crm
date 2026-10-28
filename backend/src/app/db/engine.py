from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    url = URL.create(
        drivername="postgresql+asyncpg",
        username=settings.postgres.user,
        password=settings.postgres.password.get_secret_value(),
        host=settings.postgres.host,
        port=settings.postgres.port,
        database=settings.postgres.db,
    )
    return create_async_engine(url, echo=settings.debug, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
