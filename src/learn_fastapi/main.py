from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/file")
async def get_file():
    path = "./src/test.txt"  # Replace with the actual file path
    return FileResponse(path)