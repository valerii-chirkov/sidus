from fastapi import FastAPI
from model import Base
from config import engine
from router import router


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def hello():
    return "This is a sidus test task"


app.include_router(router, prefix="/user", tags=["user"])

