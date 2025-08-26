from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel, ConfigDict


from .role import RoleRead
from ..types.user_id import UserIdType


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: UserIdType
    email: EmailStr
    name: str
    role: Optional["RoleRead"]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
