"""
Meetingplanner — Student Orchestra System
FastAPI application entry point.

Start the dev server:
    uvicorn app.main:app --reload --port 8000

Interactive API docs (auto-generated):
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, events, roles, rsvps, users

app = FastAPI(
    title="Meetingplanner — Orchestra API",
    description="Backend API for the student orchestra event management system.",
    version="1.0.0",
)

# CORS — allow the Vue frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers under /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(rsvps.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(roles.router, prefix="/api")


@app.get("/health")
async def health():
    """Health check — used by deployment infrastructure."""
    return {"status": "ok"}
