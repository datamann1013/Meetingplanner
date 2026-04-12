from pydantic import BaseModel


class PermissionOut(BaseModel):
    id: int
    resource: str
    action: str
    model_config = {"from_attributes": True}


class RoleOut(BaseModel):
    id: int
    name: str
    description: str
    is_system: bool
    permissions: list[PermissionOut] = []
    model_config = {"from_attributes": True}


class RoleCreate(BaseModel):
    name: str
    description: str = ""


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RolePermissionAssign(BaseModel):
    permission_ids: list[int]
