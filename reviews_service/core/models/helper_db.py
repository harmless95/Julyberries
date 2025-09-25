from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from core.models.reviews import Reviews


async def connect_mongo_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["reviews-db"]
    await init_beanie(database=db, document_models=[Reviews])
