from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from learn_fastapi.models import Book, BookBase


async def get_by_id(session: AsyncSession, book_id: int) -> list[Book]:
    result = await session.execute(select(Book).where(Book.id == book_id))
    return list(result.scalars().all())


async def get_average_price(session: AsyncSession) -> list[float | None]:
    result = await session.execute(select(func.avg(Book.price)))
    return list(result.scalars().all())


async def get_page(
    session: AsyncSession, page: int, page_size: int
) -> list[Book]:
    skip = (page - 1) * page_size
    result = await session.execute(select(Book).offset(skip).limit(page_size))
    return list(result.scalars().all())


async def add(session: AsyncSession, book: BookBase) -> None:
    session.add(Book(**book.model_dump()))