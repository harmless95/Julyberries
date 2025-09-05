import json
from decimal import Decimal
from typing import Annotated, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from aiokafka import AIOKafkaProducer

from api.CRUD.crud_products import (
    get_all,
    get_product_id,
    create_product,
    update_product,
)

from api.dependencies.kafka_state import get_producer
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
    producer: Annotated[AIOKafkaProducer, Depends(get_producer)],
    product: Product = Depends(get_product_by_id),
) -> ProductRead:
    product_update = await update_product(
        session=session,
        data_update=data_update,
        product=product,
    )
    if data_update.price != product.price:
        message_bytes = json.dumps(
            data_update.model_dump(),
            default=lambda v: float(v) if isinstance(v, Decimal) else v,
        ).encode("utf-8")
        await producer.send_and_wait("PRODUCT_UPDATED", message_bytes)
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
    product_update = await update_product(
        session=session, data_update=data_update, product=product, partial=True
    )
    if product_update is not None and product_update.price != product.price:
        message_bytes = json.dumps(
            data_update.model_dump(),
            default=lambda v: float(v) if isinstance(v, Decimal) else v,
        ).encode("utf-8")
        await producer.send_and_wait("PRODUCT_UPDATED", message_bytes)
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
