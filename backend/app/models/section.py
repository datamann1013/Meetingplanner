from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InstrumentSection(Base):
    """An instrument section in the orchestra (e.g. Strings, Brass, Woodwinds)."""
    __tablename__ = "instrument_sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(500))

    memberships: Mapped[list["SectionMembership"]] = relationship(
        "SectionMembership", back_populates="section", cascade="all, delete-orphan"
    )


class SectionMembership(Base):
    """
    Links a user to an instrument section with an optional position/chair label.

    A single user CAN belong to multiple sections simultaneously
    (e.g. someone who plays both piano and violin).
    The unique constraint only prevents the *same* (user, section) pair from
    being added twice — it does NOT limit how many sections a user can join.
    """
    __tablename__ = "section_memberships"

    id: Mapped[int] = mapped_column(primary_key=True)
    position: Mapped[str | None] = mapped_column(String(100))  # e.g. "Principal", "1st Chair"
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    section_id: Mapped[int] = mapped_column(ForeignKey("instrument_sections.id"))

    user: Mapped["User"] = relationship("User", back_populates="section_memberships")  # noqa: F821
    section: Mapped["InstrumentSection"] = relationship("InstrumentSection", back_populates="memberships")
