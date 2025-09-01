#!/usr/bin/env python
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from core.config import setting
from core.model import helper_db
from api.routers import all_router
from core.authoriztion.middleware_auth import AuthMiddleware

logging.basicConfig(
    level=logging.INFO,
    format=setting.log.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await helper_db.dispose()


app_catalog_main = FastAPI(lifespan=lifespan)
app_catalog_main.include_router(router=all_router)

app_catalog_main.add_middleware(AuthMiddleware)


@app_catalog_main.get("/protected")
async def protected_endpoint(request: Request):
    return {"message": f"Привет, {request.state.user}. Доступ разрешен."}


@app_catalog_main.get("/")
async def get_hello():
    return {"message": "Hello, this is the catalog container."}


if __name__ == "__main__":
    uvicorn.run(
        "main:app_catalog_main",
        host=setting.run.host,
        port=setting.run.port,
    )
