"""
Role and permission management (board-configurable RBAC).

GET    /api/roles              — list all roles with their permissions
GET    /api/permissions        — list all available permissions
POST   /api/roles              — create a new custom role
PUT    /api/roles/{id}         — rename / re-describe a role
DELETE /api/roles/{id}         — delete a role (system roles are protected)
PUT    /api/roles/{id}/permissions — replace a role's permission set
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user, require_permission
from app.database import get_db
from app.models.role import Permission, Role, RolePermission
from app.models.user import User
from app.schemas.role import PermissionOut, RoleCreate, RoleOut, RolePermissionAssign, RoleUpdate

router = APIRouter(tags=["roles"])


def _role_to_out(role: Role) -> RoleOut:
    return RoleOut(
        id=role.id,
        name=role.name,
        description=role.description,
        is_system=role.is_system,
        permissions=[
            PermissionOut(id=rp.permission.id, resource=rp.permission.resource, action=rp.permission.action)
            for rp in role.role_permissions
        ],
    )


def _load_opts():
    return [selectinload(Role.role_permissions).selectinload(RolePermission.permission)]


@router.get("/roles", response_model=list[RoleOut])
async def list_roles(
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("roles", "read")),
):
    result = await db.execute(select(Role).options(*_load_opts()).order_by(Role.name))
    return [_role_to_out(r) for r in result.scalars().all()]


@router.get("/permissions", response_model=list[PermissionOut])
async def list_permissions(
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("roles", "read")),
):
    result = await db.execute(select(Permission).order_by(Permission.resource, Permission.action))
    return result.scalars().all()


@router.post("/roles", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(
    body: RoleCreate,
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("roles", "create")),
):
    role = Role(name=body.name, description=body.description, is_system=False)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    result = await db.execute(select(Role).where(Role.id == role.id).options(*_load_opts()))
    return _role_to_out(result.scalar_one())


@router.put("/roles/{role_id}", response_model=RoleOut)
async def update_role(
    role_id: int,
    body: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("roles", "update")),
):
    result = await db.execute(select(Role).where(Role.id == role_id).options(*_load_opts()))
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if role.is_system:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="System roles cannot be modified")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(role, field, value)
    await db.commit()
    result = await db.execute(select(Role).where(Role.id == role_id).options(*_load_opts()))
    return _role_to_out(result.scalar_one())


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("roles", "delete")),
):
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if role.is_system:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="System roles cannot be deleted")
    await db.delete(role)
    await db.commit()


@router.put("/roles/{role_id}/permissions", response_model=RoleOut)
async def set_role_permissions(
    role_id: int,
    body: RolePermissionAssign,
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("roles", "update")),
):
    result = await db.execute(select(Role).where(Role.id == role_id).options(*_load_opts()))
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if role.is_system:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="System role permissions cannot be changed")

    perms_result = await db.execute(select(Permission).where(Permission.id.in_(body.permission_ids)))
    found_perms = perms_result.scalars().all()
    if len(found_perms) != len(body.permission_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more permission IDs not found")

    for rp in list(role.role_permissions):
        await db.delete(rp)
    for perm_id in body.permission_ids:
        db.add(RolePermission(role_id=role.id, permission_id=perm_id))

    await db.commit()
    result = await db.execute(select(Role).where(Role.id == role_id).options(*_load_opts()))
    return _role_to_out(result.scalar_one())
