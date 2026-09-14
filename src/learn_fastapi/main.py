from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

class Book(BaseModel):
    title: str
    author: str
    price: float


@app.post("/add_books")
async def add_books(book: Book):
    return {"title": book.title, "author": book.author, "price": book.price}
