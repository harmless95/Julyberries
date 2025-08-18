from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleRead(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
