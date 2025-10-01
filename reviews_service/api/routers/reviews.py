from typing import Annotated
from fastapi import APIRouter, status, Request, Depends
from aiokafka import AIOKafkaProducer

from api.CRUD.reviews_crud import create_reviews

from api.Dependencies.kafka_state import get_producer

from api.Dependencies.reviews_kafka import validate_price_decimal
from core.config import setting
from core.schema.reviews_schema import ReviewsCreate, ReviewsRead

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
