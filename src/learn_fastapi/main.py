from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

class User(BaseModel):
    username: str = Field(default="mike", min_length=2, max_length=10)
    password: str = Field(default="123456", min_length=6, max_length=20)

async def register_user(user: User):
    return {"message": "User registered successfully", "user": user}