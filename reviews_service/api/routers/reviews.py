from typing import Annotated

from fastapi import APIRouter, status, Request, Depends
from aiokafka import AIOKafkaProducer
from uuid import UUID

from api.CRUD.reviews_crud import (
    create_reviews,
    get_review_by_id,
    update_review_by_product_id,
    get_reviews_by_id,
)

from api.Dependencies.kafka_state import get_producer

from api.Dependencies.reviews_kafka import validate_price_decimal
from core.config import setting
from core.schema.reviews_schema import ReviewsCreate, ReviewsRead, ReviewsUpdate

from core.models.reviews import Reviews

router = APIRouter(prefix=setting.api.prefix, tags=[setting.api.tags])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_reviews(
    data_reviews: ReviewsCreate,
    producer: Annotated[AIOKafkaProducer, Depends(get_producer)],
    request: Request,
):
    result = await create_reviews(data_reviews=data_reviews, request=request)
    await validate_price_decimal(
        review_data=result,
        producer=producer,
    )
    return result


@router.get("/{product_id}/")
async def get_reviews(
    product_id: UUID,
):
    result = await get_reviews_by_id(product_id=product_id)
    return result


@router.patch("/{product_id}/")
async def update_review(
    data_update: ReviewsUpdate,
    data_review: Reviews = Depends(get_review_by_id),
):
    result = await update_review_by_product_id(
        data_update=data_update,
        data_review=data_review,
        partial=True,
    )
    return result
