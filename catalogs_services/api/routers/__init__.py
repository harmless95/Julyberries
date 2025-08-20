from fastapi import APIRouter

from .router_product import router as router_product
from .router_category import router as router_category

all_router = APIRouter()

all_router.include_router(router=router_product)
all_router.include_router(router=router_category)
