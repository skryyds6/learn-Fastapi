from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None):
    return {"item_id": item_id, "q": q}

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(..., description="The ID of the book to get", gt= 0, lt=1000)):
    return {"book_id": book_id, "message": "Book ID must be greater than 0 and less than 1000"}