from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

class News(BaseModel):
    title: str
    content: str
    published: bool

@app.get("/news",response_model=News)
async def get_news():
    return News(
        title="Sample News Title",
        content="This is the content of the news article.",
        published=True
    )