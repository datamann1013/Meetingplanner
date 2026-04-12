"""
Event routes.

GET    /api/events          — list events (paginated, filterable)
POST   /api/events          — create event (requires events.create)
GET    /api/events/{id}     — get single event with relations
PUT    /api/events/{id}     — update event (requires events.update)
DELETE /api/events/{id}     — delete event (requires events.delete)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user, require_permission
from app.database import get_db
from app.models.event import Category, Event, EventCategory, EventType
from app.models.user import User
from app.schemas.event import (
    CategoryOut,
    EventCreate,
    EventOut,
    EventTypeOut,
    EventUpdate,
    PaginatedEvents,
)

router = APIRouter(prefix="/events", tags=["events"])


def _load_options():
    return [
        selectinload(Event.event_type),
        selectinload(Event.creator),
        selectinload(Event.event_categories).selectinload(EventCategory.category),
    ]


def _event_to_out(event: Event) -> EventOut:
    return EventOut(
        id=event.id,
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        capacity=event.capacity,
        signup_deadline=event.signup_deadline,
        contact_info=event.contact_info,
        cover_image_url=event.cover_image_url,
        is_published=event.is_published,
        slug=event.slug,
        fee_charged=event.fee_charged,
        fee_received=event.fee_received,
        fee_currency=event.fee_currency,
        fee_notes=event.fee_notes,
        event_type=EventTypeOut.model_validate(event.event_type) if event.event_type else None,
        creator=None if event.creator is None else type("C", (), {"id": event.creator.id, "username": event.creator.username})(),  # noqa: E501
        categories=[CategoryOut.model_validate(ec.category) for ec in event.event_categories],
        created_at=event.created_at,
        updated_at=event.updated_at,
    )


@router.get("", response_model=PaginatedEvents)
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    published_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """List events. Public endpoint — unpublished events hidden unless published_only=false."""
    query = select(Event)
    if published_only:
        query = query.where(Event.is_published == True)  # noqa: E712

    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar_one()

    result = await db.execute(
        query.options(*_load_options())
        .order_by(Event.date.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    events = result.scalars().all()
    return PaginatedEvents(items=[_event_to_out(e) for e in events], total=total, page=page, page_size=page_size)


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id).options(*_load_options()))
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return _event_to_out(event)


@router.post("", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def create_event(
    body: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("events", "create")),
):
    event = Event(
        title=body.title,
        description=body.description,
        date=body.date,
        location=body.location,
        capacity=body.capacity,
        signup_deadline=body.signup_deadline,
        contact_info=body.contact_info,
        is_published=body.is_published,
        slug=body.slug,
        event_type_id=body.event_type_id,
        fee_charged=body.fee_charged,
        fee_received=body.fee_received,
        fee_currency=body.fee_currency,
        fee_notes=body.fee_notes,
        created_by_id=current_user.id,
    )
    db.add(event)
    await db.flush()  # get event.id before adding categories

    for cat_id in body.category_ids:
        db.add(EventCategory(event_id=event.id, category_id=cat_id))

    await db.commit()
    await db.refresh(event)

    # Reload with relations
    result = await db.execute(select(Event).where(Event.id == event.id).options(*_load_options()))
    return _event_to_out(result.scalar_one())


@router.put("/{event_id}", response_model=EventOut)
async def update_event(
    event_id: int,
    body: EventUpdate,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
    _: None = Depends(require_permission("events", "update")),
):
    result = await db.execute(select(Event).where(Event.id == event_id).options(*_load_options()))
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    for field, value in body.model_dump(exclude_unset=True, exclude={"category_ids"}).items():
        setattr(event, field, value)

    if body.category_ids is not None:
        # Replace all categories
        for ec in list(event.event_categories):
            await db.delete(ec)
        for cat_id in body.category_ids:
            db.add(EventCategory(event_id=event.id, category_id=cat_id))

    await db.commit()
    result = await db.execute(select(Event).where(Event.id == event_id).options(*_load_options()))
    return _event_to_out(result.scalar_one())


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
    _: None = Depends(require_permission("events", "delete")),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    await db.delete(event)
    await db.commit()


# --- Event types and categories (board-managed reference data) ---

@router.get("/types/all", response_model=list[EventTypeOut], tags=["event-types"])
async def list_event_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EventType).order_by(EventType.name))
    return result.scalars().all()


@router.get("/categories/all", response_model=list[CategoryOut], tags=["categories"])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.name))
    return result.scalars().all()
