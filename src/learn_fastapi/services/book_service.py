from sqlalchemy.ext.asyncio import AsyncSession

from learn_fastapi.models import Book, BookBase
from learn_fastapi.repositories import book_repository


async def get_by_id(session: AsyncSession, book_id: int) -> list[Book]:
    return await book_repository.get_by_id(session, book_id)


async def get_average_price(session: AsyncSession) -> list[float | None]:
    return await book_repository.get_average_price(session)


async def get_page(
    session: AsyncSession, page: int, page_size: int
) -> list[Book]:
    return await book_repository.get_page(session, page, page_size)


async def add(session: AsyncSession, book: BookBase) -> BookBase:
    await book_repository.add(session, book)
    return book