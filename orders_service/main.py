#!/usr/bin/env python
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from core.config import setting
from core.model import helper_db
from api.routers import all_router
from core.authorization.middleware_auth import MiddlewareAuth
from utils.exception_middleware import ExceptionHandlingMiddleware
from utils.middleware_prometheus import PrometheusMiddleware

logging.basicConfig(
    level=logging.INFO,
    format=setting.log.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await helper_db.dispose()


app_orders_main = FastAPI(lifespan=lifespan)
app_orders_main.include_router(router=all_router)

app_orders_main.add_middleware(ExceptionHandlingMiddleware)
app_orders_main.add_middleware(MiddlewareAuth)
app_orders_main.add_middleware(PrometheusMiddleware)


@app_orders_main.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app_orders_main.get("/protected_order/")
async def protected_endpoint(request: Request):
    return {"message": f"Привет {request.state.user}. Доступ разрешен."}


@app_orders_main.get("/")
async def get_hello():
    return {"message": "Hello, this is the order container."}


if __name__ == "__main__":
    uvicorn.run(
        "main:app_orders_main",
        host=setting.run.host,
        port=setting.run.port,
    )
