from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from learn_fastapi.config.settings import (
    ASYNC_DATABASE_URL,
    DATABASE_ECHO,
    DATABASE_MAX_OVERFLOW,
    DATABASE_POOL_SIZE,
)
from learn_fastapi.models import Base

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=DATABASE_ECHO,
    pool_size=DATABASE_POOL_SIZE,
    max_overflow=DATABASE_MAX_OVERFLOW,
)
AsyncSessionLocal = async_sessionmaker(bind=engine)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise