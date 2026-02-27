from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import PGSettings, get_settings


def pg_engine(pg_settings: PGSettings, log_level: str) -> AsyncEngine:
    return create_async_engine(
        pg_settings.db_url,
        pool_size=pg_settings.POOL_MINSIZE,
        max_overflow=pg_settings.POOL_MAX_OVERFLOW,
        pool_timeout=pg_settings.POOL_TIMEOUT,
        pool_recycle=pg_settings.POOL_RECYCLE,
        pool_pre_ping=True,
        echo=log_level == "debug",
    )


@lru_cache
def get_pg_engine() -> AsyncEngine:
    settings = get_settings()
    return pg_engine(pg_settings=settings.PG, log_level=settings.LOG_LEVEL)


@lru_cache
def get_session_factory() -> sessionmaker:
    return sessionmaker(get_pg_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
