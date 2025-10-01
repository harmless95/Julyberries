from pydantic import BaseModel, ConfigDict, Field


class ReviewsCreate(BaseModel):
    product_name: str
    rating: int
    text: str = Field(default="")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class ReviewsRead(BaseModel):
    id: str = Field(alias="_id")
    product_name: str
    user_id: str
    rating: int
    text: str = Field(default="")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
