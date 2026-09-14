from fastapi import FastAPI, Path, Query

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

@app.get("/news/new_list")
async def read_news_list(skip: int = Query(0, min_length=0,max_length=100, description="Number of items to skip"),
                          limit: int = Query(10, description="Maximum number of items to return")):
    return {"skip": skip, "limit": limit, "message": "This endpoint returns a list of news articles with pagination."}