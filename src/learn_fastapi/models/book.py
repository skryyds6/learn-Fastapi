from pydantic import BaseModel
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from learn_fastapi.models.Base import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")


class BookBase(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str