import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import setting
from api.routers.reviews import router
from core.models.helper_db import connect_mongo_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await connect_mongo_db()
    yield
    client.close()


app_reviews = FastAPI(lifespan=lifespan)
app_reviews.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app_reviews", host=setting.run.host, port=setting.run.port)
