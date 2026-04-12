from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user_roles: Mapped[list["UserRole"]] = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    events_created: Mapped[list["Event"]] = relationship("Event", back_populates="creator")  # noqa: F821
    rsvps: Mapped[list["RSVP"]] = relationship("RSVP", back_populates="user")  # noqa: F821
    chat_messages: Mapped[list["ChatMessage"]] = relationship("ChatMessage", back_populates="user")  # noqa: F821
    section_memberships: Mapped[list["SectionMembership"]] = relationship("SectionMembership", back_populates="user")  # noqa: F821
    sheet_music_uploaded: Mapped[list["SheetMusicPiece"]] = relationship("SheetMusicPiece", back_populates="uploaded_by_user")  # noqa: F821
