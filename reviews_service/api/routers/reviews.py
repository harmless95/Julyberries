from fastapi import APIRouter, status, Request

from api.CRUD.reviews_crud import create_reviews
from core.config import setting
from core.schema.reviews_schema import ReviewsCreate, ReviewsRead

router = APIRouter(prefix=setting.api.prefix, tags=[setting.api.tags])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_reviews(
    data_reviews: ReviewsCreate,
    request: Request,
):
    result = await create_reviews(data_reviews=data_reviews, request=request)
    return result
