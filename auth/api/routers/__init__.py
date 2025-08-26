from fastapi import APIRouter
from .user_router import router as user_router

all_routers = APIRouter()
all_routers.include_router(router=user_router)
