import uuid
from fastapi import Request

from core.models.reviews import Reviews
from core.schema.reviews_schema import ReviewsCreate


async def create_reviews(
    data_reviews: ReviewsCreate,
    request: Request,
) -> Reviews:
    user_id = request.state.user.get("id")
    review = Reviews(
        product_id=data_reviews.product_id,
        user_id=user_id,
        rating=data_reviews.rating,
        text=data_reviews.text,
    )
    data_review = await review.insert()
    return data_review
