import json
from decimal import Decimal
from typing import Annotated, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Request, HTTPException
from aiokafka import AIOKafkaProducer

from api.CRUD.crud_products import (
    get_all,
    get_product_id,
    create_product,
    update_product,
)

from api.dependencies.kafka_state import get_producer
from api.dependencies.service_httpx import permission_product
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
    product_id: UUID,
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
    request: Request,
) -> Product:
    permission_codes = request.state.user.get("permission")
    if "product.create" not in permission_codes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access for this operation",
        )

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
    producer: Annotated[AIOKafkaProducer, Depends(get_producer)],
    product: Product = Depends(get_product_by_id),
) -> ProductRead:

    permission_codes = request.state.user.get("permission")
    await check_permission(
        permission_codes=permission_codes,
        product_code="product.update",
    )

    await validate_price_decimal(
        data_update=data_update,
        product=product,
        producer=producer,
    )

    product_update = await update_product(
        session=session,
        data_update=data_update,
        product=product,
    )
    return ProductRead.model_validate(product_update)


@router.patch(
    "/{product_id}/",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def update_product_by_id_partial(
    data_update: ProductUpdate,
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    producer: Annotated[AIOKafkaProducer, Depends(get_producer)],
    product: Product = Depends(get_product_by_id),
) -> ProductRead:

    permission_codes = request.state.user.get("permission")
    await check_permission(
        permission_codes=permission_codes,
        product_code="product.update",
    )

    await validate_price_decimal(
        data_update=data_update,
        product=product,
        producer=producer,
    )

    product_update = await update_product(
        session=session, data_update=data_update, product=product, partial=True
    )
    return ProductRead.model_validate(product_update)


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
