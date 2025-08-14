from datetime import datetime
from typing import TYPE_CHECKING, Optional
from pydantic import EmailStr, BaseModel, ConfigDict

if TYPE_CHECKING:
    from core.model import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    role_id: Optional["Role"]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None
    role_id: Optional[int] | None = None
    created_at: datetime | None = None


class UserToken(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: str
    name: str
