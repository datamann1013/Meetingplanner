"""
Database seeder — run once after `alembic upgrade head`.

Creates:
  - All permissions (resource × action pairs)
  - System roles: SuperAdmin, Board, Member, Guest
  - Default event types: Rehearsal, Concert, Social, Meeting, Gig
  - One SuperAdmin user (credentials from .env)

Usage:
    python seed.py

Safe to re-run — skips anything that already exists.
"""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.core.security import hash_password
from app.models.event import EventType
from app.models.role import Permission, Role, RolePermission, UserRole
from app.models.user import User

# ---------------------------------------------------------------------------
# Permission catalogue — add new resources here as features are built
# ---------------------------------------------------------------------------
ALL_PERMISSIONS: list[tuple[str, str]] = [
    # Events
    ("events", "read"),
    ("events", "create"),
    ("events", "update"),
    ("events", "delete"),
    # RSVPs
    ("rsvps", "read"),
    ("rsvps", "create"),
    ("rsvps", "update"),
    ("rsvps", "delete"),
    # Users
    ("users", "read"),
    ("users", "create"),
    ("users", "update"),
    ("users", "manage_roles"),
    # Roles
    ("roles", "read"),
    ("roles", "create"),
    ("roles", "update"),
    ("roles", "delete"),
    # Chat
    ("chat", "read"),
    ("chat", "create"),
    ("chat", "delete"),
    # Sections
    ("sections", "read"),
    ("sections", "manage"),
    # Sheet music
    ("sheet_music", "read"),
    ("sheet_music", "upload"),
    ("sheet_music", "delete"),
    # Seating
    ("seating", "read"),
    ("seating", "manage"),
    # Email jobs (view logs)
    ("email_jobs", "read"),
]

# Permissions granted to each system role
ROLE_PERMISSIONS: dict[str, list[tuple[str, str]]] = {
    "SuperAdmin": ALL_PERMISSIONS,  # all permissions
    "Board": [
        ("events", "read"), ("events", "create"), ("events", "update"), ("events", "delete"),
        ("rsvps", "read"), ("rsvps", "create"), ("rsvps", "update"), ("rsvps", "delete"),
        ("users", "read"), ("users", "create"), ("users", "update"), ("users", "manage_roles"),
        ("roles", "read"), ("roles", "create"), ("roles", "update"), ("roles", "delete"),
        ("chat", "read"), ("chat", "create"), ("chat", "delete"),
        ("sections", "read"), ("sections", "manage"),
        ("sheet_music", "read"), ("sheet_music", "upload"), ("sheet_music", "delete"),
        ("seating", "read"), ("seating", "manage"),
        ("email_jobs", "read"),
    ],
    "Member": [
        ("events", "read"),
        ("rsvps", "read"), ("rsvps", "create"), ("rsvps", "update"), ("rsvps", "delete"),
        ("chat", "read"), ("chat", "create"),
        ("sections", "read"),
        ("sheet_music", "read"),
        ("seating", "read"),
    ],
    "Guest": [
        ("events", "read"),
    ],
}

DEFAULT_EVENT_TYPES = ["Rehearsal", "Concert", "Social", "Meeting", "Gig"]


async def seed(db: AsyncSession) -> None:
    print("Seeding permissions...")
    perm_map: dict[tuple[str, str], Permission] = {}
    for resource, action in ALL_PERMISSIONS:
        result = await db.execute(
            select(Permission).where(Permission.resource == resource, Permission.action == action)
        )
        perm = result.scalar_one_or_none()
        if perm is None:
            perm = Permission(resource=resource, action=action)
            db.add(perm)
            await db.flush()
            print(f"  + permission: {resource}.{action}")
        perm_map[(resource, action)] = perm

    print("Seeding roles...")
    role_map: dict[str, Role] = {}
    for role_name, role_perms in ROLE_PERMISSIONS.items():
        result = await db.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()
        if role is None:
            role = Role(name=role_name, description=f"System role: {role_name}", is_system=True)
            db.add(role)
            await db.flush()
            print(f"  + role: {role_name}")
        role_map[role_name] = role

        # Assign permissions to role (skip if already assigned)
        existing_result = await db.execute(
            select(RolePermission).where(RolePermission.role_id == role.id)
        )
        existing_perm_ids = {rp.permission_id for rp in existing_result.scalars().all()}
        for resource, action in role_perms:
            perm = perm_map.get((resource, action))
            if perm and perm.id not in existing_perm_ids:
                db.add(RolePermission(role_id=role.id, permission_id=perm.id))

    print("Seeding event types...")
    for et_name in DEFAULT_EVENT_TYPES:
        result = await db.execute(select(EventType).where(EventType.name == et_name))
        if result.scalar_one_or_none() is None:
            db.add(EventType(name=et_name))
            print(f"  + event type: {et_name}")

    print("Seeding SuperAdmin user...")
    result = await db.execute(select(User).where(User.email == settings.seed_admin_email))
    admin = result.scalar_one_or_none()
    if admin is None:
        admin = User(
            email=settings.seed_admin_email,
            username=settings.seed_admin_username,
            hashed_password=hash_password(settings.seed_admin_password),
            is_active=True,
        )
        db.add(admin)
        await db.flush()
        db.add(UserRole(user_id=admin.id, role_id=role_map["SuperAdmin"].id))
        print(f"  + admin user: {settings.seed_admin_email}")
    else:
        print(f"  ~ admin user already exists: {settings.seed_admin_email}")

    await db.commit()
    print("\nSeed complete.")


async def main() -> None:
    engine = create_async_engine(settings.database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db:
        await seed(db)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
