import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from core.config import setting
from api.routers.reviews import router
from core.models.reviews import Reviews


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient("mongodb://mongo_db:27017")
    db = client["testing_mmm"]
    await init_beanie(database=db, document_models=[Reviews])
    app.state.client = client
    yield
    client.close()


app_reviews = FastAPI(lifespan=lifespan)
app_reviews.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app_reviews", host=setting.run.host, port=setting.run.port)
