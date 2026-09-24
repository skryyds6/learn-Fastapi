from contextlib import asynccontextmanager

from fastapi import FastAPI

from learn_fastapi.handlers.book_handler import router as book_router
from learn_fastapi.infra.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(book_router)
