from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SeatingChart(Base):
    """
    Stores the seating layout for an event as JSON.
    The frontend reads this data and renders a visual grid — all visualisation
    logic lives in the frontend; this model is pure data storage.

    JSON data format:
        {
            "rows": 8,
            "cols": 12,
            "seats": [
                {"row": 0, "col": 0, "user_id": 5, "section_id": 2},
                {"row": 0, "col": 1, "user_id": null, "section_id": null},
                ...
            ]
        }

    Null user_id means the seat is empty. Seats not listed are assumed empty.
    """
    __tablename__ = "seating_charts"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(JSON, default=dict)

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), unique=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    event: Mapped["Event"] = relationship("Event", back_populates="seating_chart")  # noqa: F821
