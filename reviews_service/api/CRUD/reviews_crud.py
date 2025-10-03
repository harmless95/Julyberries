from uuid import UUID
from fastapi import Request

from core.models.reviews import Reviews
from core.schema.reviews_schema import ReviewsCreate, ReviewsUpdate

from api.Dependencies.service_httpx import is_cast_present_all

from core.config import setting


async def get_product_dict(products_all: list) -> dict:
    # Создаём словарь для быстрого поиска продукта по имени
    return {item["name"]: item for item in products_all}


async def create_reviews(
    data_reviews: ReviewsCreate,
    request: Request,
) -> Reviews:
    product_name = data_reviews.product_name
    products_all = await is_cast_present_all(
        url_service=setting.product_service.url, request=request
    )
    product_dict = await get_product_dict(products_all)
    product = product_dict.get(product_name)
    product_id = str(product.get("id"))
    user_id = str(request.state.user.get("id"))
    review = Reviews(
        product_id=product_id,
        user_id=user_id,
        rating=data_reviews.rating,
        text=data_reviews.text,
    )
    data_review = await review.insert()
    return data_review


async def get_reviews_by_id(product_id: UUID):
    reviews = await Reviews.find(Reviews.product_id == str(product_id)).to_list()
    return reviews


async def get_review_by_id(product_id: UUID):
    reviews = await Reviews.find_one(Reviews.product_id == str(product_id))
    return reviews


async def update_review_by_product_id(
    data_update: ReviewsUpdate,
    data_review: Reviews,
    partial: bool = False,
):

    for name, value in data_update.model_dump(exclude_unset=partial).items():
        setattr(data_review, name, value)
    await data_review.save()
    return data_review
