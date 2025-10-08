#!/usr/bin/env python
import asyncio
import time

import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from aiokafka import AIOKafkaProducer
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from core.config import setting
from core.model import helper_db
from api.routers import all_router
from core.authoriztion.middleware_auth import AuthMiddleware
from utils.middleware_prometheus import PrometheusMiddleware
from utils.exception_middleware import ExceptionHandlingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format=setting.log.log_format,
)

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(setting.redis_conf.url)
    FastAPICache.init(RedisBackend(redis=redis), prefix="fastapi-cache")

    producer = AIOKafkaProducer(
        bootstrap_servers=["kafka1:9090"],
        client_id="product-app",
    )
    await producer.start()
    app.state.producer = producer
    yield
    await helper_db.dispose()
    await producer.stop()


app_catalog_main = FastAPI(lifespan=lifespan)
app_catalog_main.include_router(router=all_router)

app_catalog_main.add_middleware(ExceptionHandlingMiddleware)
app_catalog_main.add_middleware(AuthMiddleware)
app_catalog_main.add_middleware(PrometheusMiddleware)


@app_catalog_main.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app_catalog_main.get("/protected_catalog/")
@cache(expire=setting.redis_conf.expire_second)
async def protected_endpoint(request: Request):
    start = time.time()
    await asyncio.sleep(5)
    elapsed = time.time() - start
    log.warning("Время работы: %s", elapsed)
    return {
        "message": f"Привет, {request.state.user}. Доступ разрешен.",
        "Время работы": elapsed,
    }


@app_catalog_main.get("/")
async def get_hello():
    return {"message": "Hello, this is the catalog container."}


if __name__ == "__main__":
    uvicorn.run(
        "main:app_catalog_main",
        host=setting.run.host,
        port=setting.run.port,
    )
