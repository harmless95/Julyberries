from beanie import Indexed, Document
from pydantic import Field, conint
from datetime import datetime


class Reviews(Document):
    product_id: Indexed(str)
    user_id: str
    rating: conint(ge=1, le=5)
    text: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reviews-database"
