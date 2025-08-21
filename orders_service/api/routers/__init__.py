from fastapi import APIRouter
from .router_order import router as router_order

all_router = APIRouter()

all_router.include_router(router=router_order)
