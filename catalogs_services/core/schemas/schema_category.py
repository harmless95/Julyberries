from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryRead(CategoryCreate):
    id: int
