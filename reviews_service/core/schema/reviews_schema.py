from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ReviewsCreate(BaseModel):
    product_id: str
    rating: int
    text: str = Field(default="")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class ReviewsRead(BaseModel):
    id: str = Field(alias="_id")
    product_id: str
    user_id: str
    rating: int
    text: str = Field(default="")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
