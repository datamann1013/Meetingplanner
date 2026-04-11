from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EventType(Base):
    """Categorises events by kind: rehearsal, concert, social, meeting, custom."""
    __tablename__ = "event_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    events: Mapped[list["Event"]] = relationship("Event", back_populates="event_type")


class Category(Base):
    """Freeform tags that can be applied to events (e.g. 'Beethoven', 'Outdoor')."""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    event_categories: Mapped[list["EventCategory"]] = relationship(
        "EventCategory", back_populates="category", cascade="all, delete-orphan"
    )


class EventCategory(Base):
    """Junction table: many-to-many between Event and Category."""
    __tablename__ = "event_categories"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

    event: Mapped["Event"] = relationship("Event", back_populates="event_categories")
    category: Mapped["Category"] = relationship("Category", back_populates="event_categories")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str | None] = mapped_column(String(500))
    capacity: Mapped[int | None] = mapped_column(Integer)
    signup_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    contact_info: Mapped[str | None] = mapped_column(Text)
    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    is_published: Mapped[bool] = mapped_column(default=False)
    slug: Mapped[str | None] = mapped_column(String(255), unique=True)  # used for public concert pages

    event_type_id: Mapped[int | None] = mapped_column(ForeignKey("event_types.id"))
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    event_type: Mapped["EventType | None"] = relationship("EventType", back_populates="events")
    creator: Mapped["User | None"] = relationship("User", back_populates="events_created")  # noqa: F821
    event_categories: Mapped[list["EventCategory"]] = relationship(
        "EventCategory", back_populates="event", cascade="all, delete-orphan"
    )
    rsvps: Mapped[list["RSVP"]] = relationship("RSVP", back_populates="event", cascade="all, delete-orphan")  # noqa: F821
    chat_messages: Mapped[list["ChatMessage"]] = relationship("ChatMessage", back_populates="event", cascade="all, delete-orphan")  # noqa: F821
    attendances: Mapped[list["Attendance"]] = relationship("Attendance", back_populates="event", cascade="all, delete-orphan")  # noqa: F821
    sheet_music: Mapped[list["SheetMusic"]] = relationship("SheetMusic", back_populates="event")  # noqa: F821
    seating_chart: Mapped["SeatingChart | None"] = relationship("SeatingChart", back_populates="event", uselist=False)  # noqa: F821
