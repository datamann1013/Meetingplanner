from datetime import datetime

from pydantic import BaseModel

from app.models.rsvp import RSVPStatus


class RSVPOut(BaseModel):
    id: int
    status: RSVPStatus
    user_id: int
    event_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class RSVPCreate(BaseModel):
    event_id: int
    status: RSVPStatus


class RSVPUpdate(BaseModel):
    status: RSVPStatus
