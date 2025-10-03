from pydantic import BaseModel, ConfigDict, Field


class ReviewsCreate(BaseModel):
    product_name: str
    rating: int
    text: str = Field(default="")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class ReviewsUpdate(BaseModel):
    product_id: str | None = None
    user_id: str | None = None
    rating: int | None = None
    text: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
