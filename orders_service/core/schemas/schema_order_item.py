from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    name: str
    count: int
