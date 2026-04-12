# Roles & Permissions (RBAC)

## How it works

Every API endpoint that requires authorisation declares what it needs:

```python
@router.post("/events")
async def create_event(
    ...,
    _: None = Depends(require_permission("events", "create")),
):
```

When a request arrives:
1. `get_current_user()` decodes the JWT and loads the user + their roles from the database
2. `require_permission("events", "create")` checks whether any of the user's roles has the `events.create` permission
3. If yes → the handler runs. If no → 403 Forbidden.

## The database tables

```
roles            — id, name, description, is_system
permissions      — id, resource, action
role_permissions — role_id, permission_id  (which permissions a role has)
user_roles       — user_id, role_id        (which roles a user has)
```

Users can have **multiple roles** simultaneously. The permission check passes if *any* of the user's roles has the required permission.

## System roles

These are seeded by `seed.py` and cannot be deleted or modified through the admin UI (`is_system = True`):

| Role | Purpose |
|------|---------|
| SuperAdmin | All permissions — for the developer/server admin |
| Board | Manage events, users, roles, sections, sheet music, seating |
| Member | RSVP, chat, view events and sheet music |
| Guest | View published events only |

## Custom roles

The board can create any number of custom roles through the admin UI:
- Go to Admin → Roles
- Click "Create Role"
- Give it a name (e.g. "Section Leader", "Instrument Manager")
- Tick the permissions it should have
- Save — then assign it to users from Admin → Users

## Adding a new permission when building a feature

1. Add the `(resource, action)` pair to `ALL_PERMISSIONS` in `seed.py`
2. Add it to the appropriate roles in `ROLE_PERMISSIONS` in `seed.py`
3. Re-run `python seed.py` — safe to re-run, skips existing data
4. Decorate your route with `Depends(require_permission("resource", "action"))`
5. The board can now also assign this permission to any custom role they create

## All current permissions

| Resource | Action | Meaning |
|----------|--------|---------|
| events | read | View events |
| events | create | Create events |
| events | update | Edit events |
| events | delete | Delete events |
| rsvps | read | View RSVPs for events |
| rsvps | create | Submit an RSVP |
| rsvps | update | Change own RSVP |
| rsvps | delete | Remove own RSVP |
| users | read | View user list |
| users | create | Invite/create users |
| users | update | Edit user profiles |
| users | manage_roles | Assign roles to users |
| roles | read | View roles and permissions |
| roles | create | Create new roles |
| roles | update | Edit roles / change their permissions |
| roles | delete | Delete custom roles |
| chat | read | Read chat messages |
| chat | create | Post chat messages |
| chat | delete | Delete any chat message |
| sections | read | View instrument sections |
| sections | manage | Create/edit sections and memberships |
| sheet_music | read | Download sheet music |
| sheet_music | upload | Upload new sheet music files |
| sheet_music | delete | Delete sheet music |
| seating | read | View seating charts |
| seating | manage | Edit seating charts |
| email_jobs | read | View email log (Admin → Logs) |
