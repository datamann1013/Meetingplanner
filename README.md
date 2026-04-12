# Meetingplanner — Student Orchestra System

A self-hosted event management system built for a student orchestra. Handles events, RSVPs, instrument sections, sheet music, seating charts, and a fully configurable role/permission system that the board can manage without touching code.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vuetify 3 + Pinia + TypeScript + Vite |
| Backend | Python 3.12 + FastAPI |
| ORM / Migrations | SQLAlchemy 2 (async) + Alembic |
| Database | PostgreSQL |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Background jobs | Celery + Redis (Phase 4) |

---

## Local Development (DevContainer)

The easiest way to run this project is using the VS Code DevContainer — it sets up Python, Node, and PostgreSQL automatically.

1. Open the repo in VS Code
2. When prompted, click **Reopen in Container**
3. Wait for `setup.sh` to finish (installs frontend deps, starts PostgreSQL, creates DB)

Then in two terminals:

```bash
# Terminal 1 — Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # edit if needed
alembic upgrade head           # run migrations
python seed.py                 # create default roles, permissions, admin user
uvicorn app.main:app --reload --port 8000
```

```bash
# Terminal 2 — Frontend
cd frontend
npm run dev
```

- Backend API + interactive docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Default admin login: `admin@yourorchestra.com` / `changeme123` (set in `.env`)

---

## Project Structure

```
backend/
  app/
    main.py          # FastAPI app — register new routers here
    config.py        # All settings (reads from .env)
    database.py      # DB engine + session
    models/          # SQLAlchemy models (one file per feature)
    schemas/         # Pydantic request/response shapes
    routers/         # API endpoints (one file per feature)
    core/
      security.py    # JWT + password hashing
      dependencies.py  # get_current_user, require_permission()
  alembic/           # Database migrations
  seed.py            # Seeds default roles, permissions, admin user

frontend/
  src/
    services/api.ts  # Axios client — all API calls go through here
    stores/auth.ts   # Pinia auth store
    types/index.ts   # TypeScript interfaces for all entities
    composables/     # Reusable Vue logic
    components/
      admin/         # Board-only components
      shared/        # Public components
    views/           # Page-level components
```

---

## Adding a New Feature

See [docs/adding-a-feature.md](docs/adding-a-feature.md) for the full guide. The short version:

1. Add a model to `backend/app/models/newfeature.py`
2. Import it in `backend/app/models/__init__.py`
3. Add schemas to `backend/app/schemas/newfeature.py`
4. Add a router to `backend/app/routers/newfeature.py`
5. Register the router in `backend/app/main.py`
6. Add any new permissions to `seed.py` → `ALL_PERMISSIONS`
7. Run `alembic revision --autogenerate -m "add newfeature"` then `alembic upgrade head`
8. Re-run `python seed.py` (safe to re-run — skips existing data)

---

## Roles & Permissions

The board can create custom roles and assign permissions through the admin UI — no code changes needed.

System roles (cannot be deleted):
- **SuperAdmin** — all permissions
- **Board** — manage events, users, roles, sections, sheet music, seating
- **Member** — RSVP, chat, view events and sheet music
- **Guest** — view published events only

To add a new permission when building a new feature, add it to `ALL_PERMISSIONS` in `seed.py` and decorate the route:

```python
@router.post("/newfeature")
async def create_thing(
    ...,
    _: None = Depends(require_permission("newfeature", "create")),
):
```

---

## ⚠️ Before Going to Production

Work through this checklist before deploying for real users:

### Secrets & Configuration
- [ ] Generate a strong `JWT_SECRET` (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Change `SEED_ADMIN_PASSWORD` in `.env` — and change the admin password immediately after first login
- [ ] Set `CORS_ORIGINS` to your actual frontend domain (e.g. `https://orchestra.example.com`) — remove `localhost`
- [ ] Set `VITE_API_URL` in `frontend/.env` to your production backend URL
- [ ] Never commit `.env` files to git (`.gitignore` covers this)

### Database
- [ ] Switch from local PostgreSQL to a managed database (or your university's server)
- [ ] Update `DATABASE_URL` with production credentials
- [ ] Run `alembic upgrade head` on the production database
- [ ] Run `python seed.py` once on production to create roles and admin user
- [ ] Set up automated database backups

### Deployment
- [ ] Run `npm run build` in `frontend/` and serve the `dist/` folder via Nginx or similar
- [ ] Run FastAPI with `uvicorn app.main:app --host 0.0.0.0 --port 8000` behind a reverse proxy (Nginx/Caddy)
- [ ] Use a process manager (systemd or supervisord) to keep the backend running
- [ ] Set up HTTPS — Let's Encrypt is free and works with Nginx/Caddy
- [ ] Set `echo=False` in `database.py` (already done) to avoid SQL logging in production

### Email (Phase 4)
- [ ] Configure `SMTP_*` variables with your email provider credentials
- [ ] Start the Celery worker: `celery -A app.tasks.celery_app worker --loglevel=info`
- [ ] Start Redis: `redis-server` (or use a managed Redis service)

### Security
- [ ] Review all `require_permission()` decorators on sensitive routes
- [ ] Ensure uploaded files (`uploads/`) are not directly accessible from the internet without auth
- [ ] Consider rate-limiting the `/api/auth/login` endpoint

---

## Documentation

- [docs/architecture.md](docs/architecture.md) — system overview and data model
- [docs/adding-a-feature.md](docs/adding-a-feature.md) — step-by-step guide for contributors
- [docs/rbac.md](docs/rbac.md) — how roles and permissions work
- [docs/deployment.md](docs/deployment.md) — full deployment guide
- http://localhost:8000/docs — interactive API docs (auto-generated, always up to date)
