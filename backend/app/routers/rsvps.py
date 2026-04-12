"""
RSVP routes.

GET  /api/rsvps?event_id=X  — list RSVPs for an event
POST /api/rsvps             — create/update own RSVP (deadline enforced server-side)
PUT  /api/rsvps/{id}        — update own RSVP (deadline enforced)
DELETE /api/rsvps/{id}      — delete own RSVP
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.event import Event
from app.models.rsvp import RSVP
from app.models.user import User
from app.schemas.rsvp import RSVPCreate, RSVPOut, RSVPUpdate

router = APIRouter(prefix="/rsvps", tags=["rsvps"])


async def _get_event_or_404(event_id: int, db: AsyncSession) -> Event:
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


def _check_deadline(event: Event) -> None:
    if event.signup_deadline and datetime.now(UTC) > event.signup_deadline.replace(tzinfo=UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RSVP deadline has passed for this event",
        )


@router.get("", response_model=list[RSVPOut])
async def list_rsvps(
    event_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(RSVP).where(RSVP.event_id == event_id).options(selectinload(RSVP.user))
    )
    return result.scalars().all()


@router.post("", response_model=RSVPOut, status_code=status.HTTP_201_CREATED)
async def create_rsvp(
    body: RSVPCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = await _get_event_or_404(body.event_id, db)
    _check_deadline(event)

    # Upsert: if the user already has an RSVP, update it
    result = await db.execute(
        select(RSVP).where(RSVP.user_id == current_user.id, RSVP.event_id == body.event_id)
    )
    rsvp = result.scalar_one_or_none()
    if rsvp:
        rsvp.status = body.status
    else:
        rsvp = RSVP(user_id=current_user.id, event_id=body.event_id, status=body.status)
        db.add(rsvp)

    await db.commit()
    await db.refresh(rsvp)
    return rsvp


@router.put("/{rsvp_id}", response_model=RSVPOut)
async def update_rsvp(
    rsvp_id: int,
    body: RSVPUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(RSVP).where(RSVP.id == rsvp_id))
    rsvp = result.scalar_one_or_none()
    if rsvp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RSVP not found")
    if rsvp.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot edit another user's RSVP")

    event = await _get_event_or_404(rsvp.event_id, db)
    _check_deadline(event)

    rsvp.status = body.status
    await db.commit()
    await db.refresh(rsvp)
    return rsvp


@router.delete("/{rsvp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rsvp(
    rsvp_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(RSVP).where(RSVP.id == rsvp_id))
    rsvp = result.scalar_one_or_none()
    if rsvp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RSVP not found")
    if rsvp.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user's RSVP")
    await db.delete(rsvp)
    await db.commit()
