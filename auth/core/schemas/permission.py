from pydantic import BaseModel, ConfigDict


class PermissionCreate(BaseModel):
    code: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class PermissionRead(PermissionCreate):
    id: int


class PermissionUpdate(BaseModel):
    code: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
