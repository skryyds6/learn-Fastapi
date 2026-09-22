from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI
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
        onupdate=func.now,
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

AsyncSessionLocal = async_sessionmaker(
    bind=engine
)
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

@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book