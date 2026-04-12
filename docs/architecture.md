# Architecture Overview

## System Diagram

```
Browser (Vue 3 + Vuetify)
    │
    │  HTTP/REST (JSON)        WebSocket (Phase 5)
    ▼                                ▼
FastAPI (Python 3.12)  ──────────────────────────
    │                          Socket.io gateway
    │  SQLAlchemy async
    ▼
PostgreSQL
    +
uploads/ directory  (local files — S3-ready via STORAGE_TYPE env var)
    +
Redis + Celery  (Phase 4 — email job queue)
```

## Key Design Decisions

**One router per feature.** Each feature area (`events`, `rsvps`, `users`, etc.) has its own file in `routers/`. Adding a feature means adding a new file and registering it in `main.py` — nothing else changes.

**RBAC is data-driven.** Roles and permissions are stored in the database. The board can create custom roles and assign permissions through the admin UI without any code changes. Every API route declares what permission it requires with `Depends(require_permission("resource", "action"))`.

**Async throughout.** FastAPI + SQLAlchemy async engine means the backend handles concurrent requests efficiently without blocking.

---

## Data Model

```
User
  ├── UserRole (junction) ──► Role
  │                              └── RolePermission (junction) ──► Permission
  ├── RSVP ──► Event
  ├── ChatMessage ──► Event
  └── SectionMembership ──► InstrumentSection

Event
  ├── EventType  (rehearsal / concert / social / meeting / gig / custom)
  ├── EventCategory (junction) ──► Category
  ├── RSVP[]
  ├── ChatMessage[]
  ├── SheetMusicPiece[]
  │       └── SheetMusicFile[]  (one piece = multiple files: score, parts, MuseScore)
  └── SeatingChart  (JSON blob, rendered by frontend)

EmailJob  (tracks outbound email queue — Phase 4)
```

### Permission resources and actions

| Resource | Actions |
|----------|---------|
| events | read, create, update, delete |
| rsvps | read, create, update, delete |
| users | read, create, update, manage_roles |
| roles | read, create, update, delete |
| chat | read, create, delete |
| sections | read, manage |
| sheet_music | read, upload, delete |
| seating | read, manage |
| email_jobs | read |

---

## Request Flow

```
1. Browser sends:  POST /api/auth/login  { email, password }
2. FastAPI auth router validates credentials, returns { token, user }
3. Browser stores token in localStorage
4. All subsequent requests include:  Authorization: Bearer <token>
5. FastAPI dependency get_current_user() decodes JWT → loads User + roles
6. require_permission("events", "create") checks user's roles for that permission
7. If allowed → handler runs → SQLAlchemy query → JSON response
8. If denied  → 403 Forbidden
```

---

## File Storage

Files (sheet music, cover images) are stored under `uploads/` locally in development. The `STORAGE_TYPE` environment variable controls the backend:

- `local` — stored on disk relative to `STORAGE_PATH`
- `s3` — (future) swap the storage service implementation, no router changes needed

Uploaded files are served via a static file mount or a dedicated CDN/proxy in production.

---

## Frontend Structure

```
src/
  services/api.ts      Single Axios client — all API calls go here
  stores/
    auth.ts            Authentication state (user, token, isBoardMember)
    events.ts          (planned) Cached event list — avoid refetching on every mount
    rsvps.ts           (planned) Current user's RSVPs
  composables/         Reusable logic shared across components
  types/index.ts       TypeScript interfaces matching backend Pydantic schemas
  components/
    admin/             Board-only UI components
    shared/            Public-facing components
  views/               Page-level components (one per route)
  router/index.ts      Route definitions + auth guards
```

Route guards check `authStore.isAuthenticated` and `authStore.isBoardMember` — the latter is true if the user has the `Board` or `SuperAdmin` role.
