from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from learn_fastapi.infra.database import get_db
from learn_fastapi.models import BookBase
from learn_fastapi.services import book_service

router = APIRouter()


@router.get("/book/books/{book_id}")
async def get_book_list(book_id: int, db: AsyncSession = Depends(get_db)):
    return await book_service.get_by_id(db, book_id)


@router.get("/book/get_book/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await book_service.get_average_price(db)


@router.get("/book/get_book_list")
async def get_book_list_limit(
    db: AsyncSession = Depends(get_db), page: int = 1, page_size: int = 10
):
    return await book_service.get_page(db, page, page_size)


@router.post("/book/add_book")
async def add_book(book: BookBase, db: AsyncSession = Depends(get_db)) -> BookBase:
    return await book_service.add(db, book)