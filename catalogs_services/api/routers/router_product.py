from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from api.CRUD.crud_products import (
    get_all,
    get_product_id,
    create_product,
    update_product,
)
from core.model import helper_db
from core.schemas.schema_product import ProductRead, ProductCreate, ProductUpdate
from core.model import Product

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


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_product(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_product: ProductCreate,
) -> Product:
    product = await create_product(session=session, data_product=data_product)
    return product


@router.put(
    "/{product_id}/",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def update_product_by_id(
    data_update: ProductUpdate,
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    product: Product = Depends(get_product_by_id),
) -> Product:
    product_update = await update_product(
        session=session,
        data_update=data_update,
        product=product,
    )
    return product_update


@router.patch(
    "/{product_id}/",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def update_product_by_id_partial(
    data_update: ProductUpdate,
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    product: Product = Depends(get_product_by_id),
) -> Product:
    product_update = await update_product(
        session=session, data_update=data_update, product=product, partial=True
    )
    return product_update


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product_by_id(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    product: Product = Depends(get_product_by_id),
) -> None:
    await session.delete(product)
    await session.commit()
