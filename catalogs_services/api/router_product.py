from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from catalogs_services.api.CRUD.crud_products import get_all
from catalogs_services.core.model import helper_db
from catalogs_services.core.schemas.schema_product import ProductRead

router = APIRouter(prefix="/products", tags=["Product"])


@router.get(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
) -> ProductRead:
    products = await get_all(session=session)
    return ProductRead.model_validate(products)
