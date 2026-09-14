from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/html", response_class=HTMLResponse)
async def read_html():
    return "<h1>Hello, HTML!</h1>"