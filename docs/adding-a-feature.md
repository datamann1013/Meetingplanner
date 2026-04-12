# Adding a New Feature

This guide walks through the full process of adding a new feature end-to-end, using a hypothetical "Announcements" feature as an example.

---

## Step 1 — Define the database model

Create `backend/app/models/announcement.py`:

```python
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    created_by: Mapped["User | None"] = relationship("User")
```

Then register it in `backend/app/models/__init__.py`:

```python
from app.models.announcement import Announcement  # noqa: F401
```

---

## Step 2 — Define Pydantic schemas

Create `backend/app/schemas/announcement.py`:

```python
from datetime import datetime
from pydantic import BaseModel

class AnnouncementOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    model_config = {"from_attributes": True}

class AnnouncementCreate(BaseModel):
    title: str
    body: str
```

---

## Step 3 — Add permissions to the seed script

In `backend/seed.py`, add to `ALL_PERMISSIONS`:

```python
("announcements", "read"),
("announcements", "create"),
("announcements", "delete"),
```

And add them to the relevant roles in `ROLE_PERMISSIONS` (e.g. Board gets create/delete, Member gets read).

Re-run `python seed.py` — it's safe, it skips existing data.

---

## Step 4 — Write the router

Create `backend/app/routers/announcements.py`:

```python
"""
Announcement routes.

GET    /api/announcements        — list all (public or members-only)
POST   /api/announcements        — create (requires announcements.create)
DELETE /api/announcements/{id}   — delete (requires announcements.delete)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_permission
from app.database import get_db
from app.models.announcement import Announcement
from app.models.user import User
from app.schemas.announcement import AnnouncementCreate, AnnouncementOut

router = APIRouter(prefix="/announcements", tags=["announcements"])

@router.get("", response_model=list[AnnouncementOut])
async def list_announcements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Announcement).order_by(Announcement.created_at.desc()))
    return result.scalars().all()

@router.post("", response_model=AnnouncementOut, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    body: AnnouncementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("announcements", "create")),
):
    ann = Announcement(title=body.title, body=body.body, created_by_id=current_user.id)
    db.add(ann)
    await db.commit()
    await db.refresh(ann)
    return ann

@router.delete("/{ann_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    ann_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
    _: None = Depends(require_permission("announcements", "delete")),
):
    result = await db.execute(select(Announcement).where(Announcement.id == ann_id))
    ann = result.scalar_one_or_none()
    if ann is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await db.delete(ann)
    await db.commit()
```

---

## Step 5 — Register the router in main.py

In `backend/app/main.py`, add:

```python
from app.routers import announcements   # add this line

app.include_router(announcements.router, prefix="/api")   # add this line
```

---

## Step 6 — Create the migration

```bash
cd backend
alembic revision --autogenerate -m "add announcements table"
alembic upgrade head
```

Verify the migration file in `alembic/versions/` looks correct before running.

---

## Step 7 — Frontend: add the TypeScript type

In `frontend/src/types/index.ts`:

```typescript
export interface Announcement {
  id: number
  title: string
  body: string
  created_at: string
}
```

---

## Step 8 — Frontend: fetch and display

Call the API from a composable or component:

```typescript
import { api } from '@/services/api'
import type { Announcement } from '@/types'

const { data } = await api.get<Announcement[]>('/announcements')
```

Add the component to the relevant view and register a route in `frontend/src/router/index.ts` if needed.

---

## Done

The new feature is:
- Stored in the database (model + migration)
- Accessible via REST API (router)
- Permission-gated (RBAC — board controls who can do what)
- Typed end-to-end (Pydantic on backend, TypeScript on frontend)
- Automatically documented at `/docs` (Swagger UI)
