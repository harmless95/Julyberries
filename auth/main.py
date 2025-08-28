#!/usr/bin/env python
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis import asyncio as aioredis

from api.routers import all_routers
from core.config import setting
from core.model import helper_db
from api.dependecies.redis_client import redis

logging.basicConfig(
    level=logging.INFO,
    format=setting.log.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    redis = aioredis.from_url(setting.redis.url)
    try:
        yield
    finally:
        await redis.close()
        await helper_db.dispose()


app_main = FastAPI(lifespan=lifespan)
app_main.include_router(router=all_routers)


@app_main.get("/")
async def get_hello():
    return {"message": "Hello, this is the authorization container."}


if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=setting.run.host,
        port=setting.run.port,
    )
