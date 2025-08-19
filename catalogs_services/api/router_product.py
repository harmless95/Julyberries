from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from catalogs_services.api.CRUD.crud_products import get_all, get_product_id
from catalogs_services.core.model import helper_db
from catalogs_services.core.schemas.schema_product import ProductRead
from catalogs_services.core.model import Product

router = APIRouter(prefix="/products", tags=["Product"])


@router.get(
    "/",
    response_model=list[ProductRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
) -> list[ProductRead]:
    products = await get_all(session=session)
    return [ProductRead.model_validate(product) for product in products]


@router.get(
    "/{product_id}/",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    product_id: int,
) -> ProductRead:
    return await get_product_id(session=session, product_id=product_id)
