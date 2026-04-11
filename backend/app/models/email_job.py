import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EmailJobStatus(str, enum.Enum):
    queued = "queued"
    sent = "sent"
    failed = "failed"


class EmailJob(Base):
    """Tracks outbound email jobs. Used by Celery workers (Phase 4) and visible in Admin → Logs."""
    __tablename__ = "email_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_type: Mapped[str] = mapped_column(String(100))          # e.g. "event_published"
    subject: Mapped[str] = mapped_column(String(500))
    recipient_ids: Mapped[list] = mapped_column(JSON, default=list)  # list of user IDs
    status: Mapped[EmailJobStatus] = mapped_column(Enum(EmailJobStatus), default=EmailJobStatus.queued)
    error: Mapped[str | None] = mapped_column(Text)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
