from core.models.reviews import Reviews
from uuid import UUID


async def create_reviews(data_reviews) -> Reviews:
    user_id = "00000000-0000-0000-0000-000000000000"
    review = Reviews(
        product_id=data_reviews.product_id,
        user_id=user_id,
        rating=data_reviews.rating,
        text=data_reviews.text,
    )
    data_review = await review.insert()
    return data_review
