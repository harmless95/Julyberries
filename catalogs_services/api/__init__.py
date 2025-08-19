from fastapi import APIRouter

from api.router_product import router as router_product

all_router = APIRouter()

all_router.include_router(router=router_product)
