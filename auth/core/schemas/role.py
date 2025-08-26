from pydantic import BaseModel, ConfigDict

from core.types.user_id import UserIdType

class RoleCreate(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleRead(BaseModel):
    id: UserIdType
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
