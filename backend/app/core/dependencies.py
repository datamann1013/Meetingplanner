"""
FastAPI dependency functions used across routers.

Usage:
    # Require a logged-in user:
    user: User = Depends(get_current_user)

    # Require a specific permission:
    _: None = Depends(require_permission("events", "create"))
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import decode_access_token
from app.database import get_db
from app.models.role import RolePermission, UserRole
from app.models.user import User

_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Validate JWT and return the authenticated user. Raises 401 if invalid."""
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    result = await db.execute(
        select(User)
        .where(User.id == user_id, User.is_active == True)  # noqa: E712
        .options(
            selectinload(User.user_roles).selectinload(UserRole.role).selectinload(
                # noqa: F821 — avoids circular import issue at module load
                RolePermission.permission  # type: ignore[attr-defined]
            )
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user


def get_current_user_optional(
    db: AsyncSession = Depends(get_db),
) -> None:
    """Placeholder for optional auth (public routes that optionally enrich with user data)."""
    # Implemented per-router as needed
    return None


def require_permission(resource: str, action: str):
    """
    Dependency factory for RBAC gate.

    Example:
        @router.delete("/events/{id}")
        async def delete_event(
            ...,
            _: None = Depends(require_permission("events", "delete")),
        ):
    """
    async def _check(user: User = Depends(get_current_user)) -> None:
        for user_role in user.user_roles:
            for rp in user_role.role.role_permissions:
                if rp.permission.resource == resource and rp.permission.action == action:
                    return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {resource}.{action}",
        )

    return _check
