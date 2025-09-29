from uuid import UUID
from beanie import Indexed, Document
from pydantic import Field

from core.config import setting


class Reviews(Document):
    product_id: Indexed(str)
    user_id: UUID
    rating: int
    text: str = Field(default="")

    class Settings:
        name = "reviews-database"
