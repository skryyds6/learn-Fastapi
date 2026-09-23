from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, String, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
# 创建异步数据库引擎
ASYNC_DATABASE_URL = (
    "mysql+aiomysql://root:123456@localhost:3306/FastAPI_test?charset=utf8mb4"
)
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 可选的，输出SQL日志
    pool_size=10,  # 可选的，连接池大小
    max_overflow=20,  # 可选的，连接池最大溢出数
)


# 定义模型类：基类 + 表对应的模型类
# 基类： 创建时间、更新时间
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


AsyncSessionLocal = async_sessionmaker(bind=engine)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 查询--select()-->db.execute()-->从orm获取数据-->响应结果
# 条件查询，where
@app.get("/book/books/{book_id}")
async def get_book_list(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().all()
    return book


# 聚合查询，func.方法名（类属性名）
@app.get("/book/get_book/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):

    # result = await db.execute(select(func.count(Book.id)))
    # result = await db.execute(select(func.max(Book.price)))
    # result = await db.execute(select(func.min(Book.price)))
    # result = await db.execute(select(func.sum(Book.price)))
    result = await db.execute(select(func.avg(Book.price)))
    book = result.scalars().all()
    return book


# 分页查询 offset()跳过的记录数，limit()每页显示的记录数
@app.get("/book/get_book_list")
async def get_book_list_limit(
    db: AsyncSession = Depends(get_db), page: int = 1, page_size=10
):
    skip: int = (page - 1) * page_size

    result = await db.execute(select(Book).offset(skip).limit(page_size))

    book = result.scalars().all()
    return book

class book_base(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str

class new_book(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

# 新增数据
@app.post("/book/add_book")
async def add_book(book: book_base, db: AsyncSession = Depends(get_db)):
    # ORM对象--> add-->commit
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    await db.refresh(book_obj)

    return book

# 修改数据
@app.put("/book/book_update/{book_id}")
async def book_update(book_id:int, data_update:new_book,db:AsyncSession = Depends(get_db)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404,detail="没有这本书")
    db_book.bookname = data_update.bookname
    db_book.author = data_update.author
    db_book.price = data_update.price
    db_book.publisher = data_update.publisher
    await db.commit()
    await db.refresh(db_book)
    return db_book
