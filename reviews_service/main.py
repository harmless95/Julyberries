import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from aiokafka import AIOKafkaProducer

from core.config import setting
from api.routers.reviews import router
from core.models.reviews import Reviews
from core.authorization.middleware_auth import MiddlewareAuth


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient("mongodb://mongo_db:27017")
    db = client["testing_mmm"]
    await init_beanie(database=db, document_models=[Reviews])
    app.state.client = client

    producer = AIOKafkaProducer(
        bootstrap_servers=["kafka1:9090"],
        client_id="product-app",
    )
    await producer.start()
    app.state.producer = producer
    yield
    client.close()
    await producer.stop()


app_reviews = FastAPI(lifespan=lifespan)
app_reviews.include_router(router=router)
app_reviews.add_middleware(MiddlewareAuth)


@app_reviews.get("/protected_reviews/")
async def protected_endpoint(request: Request):
    return {"message": f"Привет {request.state.user}. Доступ разрешен."}


if __name__ == "__main__":
    uvicorn.run("main:app_reviews", host=setting.run.host, port=setting.run.port)
