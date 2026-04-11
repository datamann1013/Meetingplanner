import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RSVPStatus(str, enum.Enum):
    yes = "yes"
    no = "no"
    maybe = "maybe"


class RSVP(Base):
    __tablename__ = "rsvps"
    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_rsvp_user_event"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[RSVPStatus] = mapped_column(Enum(RSVPStatus))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="rsvps")  # noqa: F821
    event: Mapped["Event"] = relationship("Event", back_populates="rsvps")  # noqa: F821
