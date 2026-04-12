from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class EventTypeOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class EventCreatorOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    date: datetime
    location: str | None
    capacity: int | None
    signup_deadline: datetime | None
    contact_info: str | None
    cover_image_url: str | None
    is_published: bool
    slug: str | None
    fee_charged: Decimal | None
    fee_received: Decimal | None
    fee_currency: str | None
    fee_notes: str | None
    event_type: EventTypeOut | None
    creator: EventCreatorOut | None
    categories: list[CategoryOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    date: datetime
    location: str | None = None
    capacity: int | None = None
    signup_deadline: datetime | None = None
    contact_info: str | None = None
    is_published: bool = False
    slug: str | None = None
    event_type_id: int | None = None
    category_ids: list[int] = []
    fee_charged: Decimal | None = None
    fee_received: Decimal | None = None
    fee_currency: str | None = None
    fee_notes: str | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: datetime | None = None
    location: str | None = None
    capacity: int | None = None
    signup_deadline: datetime | None = None
    contact_info: str | None = None
    is_published: bool | None = None
    slug: str | None = None
    event_type_id: int | None = None
    category_ids: list[int] | None = None
    fee_charged: Decimal | None = None
    fee_received: Decimal | None = None
    fee_currency: str | None = None
    fee_notes: str | None = None


class PaginatedEvents(BaseModel):
    items: list[EventOut]
    total: int
    page: int
    page_size: int
