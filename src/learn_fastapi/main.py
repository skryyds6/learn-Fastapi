from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register_user(user: User):
    return {"message": "User registered successfully", "user": user}