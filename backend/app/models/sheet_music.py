from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SheetMusicPiece(Base):
    """
    A musical piece or work (e.g. "Beethoven Symphony No. 5").
    A piece groups multiple files — score, individual parts, MuseScore source, etc.
    Can be linked to a specific event or stored in the global library (event_id=None).
    """
    __tablename__ = "sheet_music_pieces"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    composer: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)   # free-text notes for this piece

    # If linked to an event, this piece is shown on that event's page.
    # If None, it lives in the global sheet music library.
    event_id: Mapped[int | None] = mapped_column(ForeignKey("events.id"))
    uploaded_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    files: Mapped[list["SheetMusicFile"]] = relationship(
        "SheetMusicFile", back_populates="piece", cascade="all, delete-orphan"
    )
    event: Mapped["Event | None"] = relationship("Event", back_populates="sheet_music_pieces")  # noqa: F821
    uploaded_by_user: Mapped["User | None"] = relationship("User", back_populates="sheet_music_uploaded")  # noqa: F821


class SheetMusicFile(Base):
    """
    A single file belonging to a SheetMusicPiece.
    Examples for one piece: "Full Score (PDF)", "Violin I Part (PDF)", "Score (MuseScore)".
    """
    __tablename__ = "sheet_music_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255))   # e.g. "Violin I Part", "Full Score"
    file_path: Mapped[str] = mapped_column(String(500))  # relative to STORAGE_PATH
    mime_type: Mapped[str] = mapped_column(String(100))  # e.g. "application/pdf"
    file_size_bytes: Mapped[int | None] = mapped_column()

    piece_id: Mapped[int] = mapped_column(ForeignKey("sheet_music_pieces.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    piece: Mapped["SheetMusicPiece"] = relationship("SheetMusicPiece", back_populates="files")
