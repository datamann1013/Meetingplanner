"""
User management routes.

GET  /api/users           — list all users (requires users.read)
GET  /api/users/{id}      — get a user (requires users.read or own profile)
POST /api/users           — create a user / invite member (requires users.create)
PUT  /api/users/{id}      — update user info (requires users.update or own profile)
PUT  /api/users/{id}/roles — assign roles to a user (requires users.manage_roles)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user, require_permission
from app.core.security import hash_password
from app.database import get_db
from app.models.role import Role, UserRole
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserRoleAssign, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def _user_to_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        roles=[ur.role.name for ur in user.user_roles],
        created_at=user.created_at,
    )


def _load_opts():
    return [selectinload(User.user_roles).selectinload(UserRole.role)]


@router.get("", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("users", "read")),
):
    result = await db.execute(select(User).options(*_load_opts()).order_by(User.username))
    return [_user_to_out(u) for u in result.scalars().all()]


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("users", "read")),
):
    result = await db.execute(select(User).where(User.id == user_id).options(*_load_opts()))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _user_to_out(user)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("users", "create")),
):
    # Check uniqueness
    exists = await db.execute(
        select(User).where((User.email == body.email) | (User.username == body.username))
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already in use")

    user = User(email=body.email, username=body.username, hashed_password=hash_password(body.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Reload with roles
    result = await db.execute(select(User).where(User.id == user.id).options(*_load_opts()))
    return _user_to_out(result.scalar_one())


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("users", "update")),
):
    result = await db.execute(select(User).where(User.id == user_id).options(*_load_opts()))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    result = await db.execute(select(User).where(User.id == user_id).options(*_load_opts()))
    return _user_to_out(result.scalar_one())


@router.put("/{user_id}/roles", response_model=UserOut)
async def assign_roles(
    user_id: int,
    body: UserRoleAssign,
    db: AsyncSession = Depends(get_db),
    _current: User = Depends(get_current_user),
    _: None = Depends(require_permission("users", "manage_roles")),
):
    result = await db.execute(select(User).where(User.id == user_id).options(*_load_opts()))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verify all role IDs exist
    roles_result = await db.execute(select(Role).where(Role.id.in_(body.role_ids)))
    found_roles = roles_result.scalars().all()
    if len(found_roles) != len(body.role_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more role IDs not found")

    # Replace all roles
    for ur in list(user.user_roles):
        await db.delete(ur)
    for role_id in body.role_ids:
        db.add(UserRole(user_id=user.id, role_id=role_id))

    await db.commit()
    result = await db.execute(select(User).where(User.id == user_id).options(*_load_opts()))
    return _user_to_out(result.scalar_one())
