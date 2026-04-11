# Import all models here so Alembic can discover them via Base.metadata
from app.models.user import User  # noqa: F401
from app.models.role import Role, Permission, RolePermission, UserRole  # noqa: F401
from app.models.event import Event, EventType, Category, EventCategory  # noqa: F401
from app.models.rsvp import RSVP  # noqa: F401
from app.models.chat import ChatMessage  # noqa: F401
from app.models.section import InstrumentSection, SectionMembership  # noqa: F401
from app.models.sheet_music import SheetMusicPiece, SheetMusicFile  # noqa: F401
from app.models.seating import SeatingChart  # noqa: F401
from app.models.email_job import EmailJob  # noqa: F401
