#!/bin/bash
# Dev environment setup — runs once after container creation.
set -e

echo "==> Starting PostgreSQL..."
sudo service postgresql start

echo "==> Creating database user and database..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='meetingplanner'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER meetingplanner WITH PASSWORD 'devpassword';"
sudo -u postgres createdb -O meetingplanner meetingplanner 2>/dev/null || echo "    Database already exists, skipping."

echo "==> Installing frontend dependencies..."
cd /workspaces/Meetingplanner/frontend
npm ci --no-audit --no-fund
npm cache clean --force

echo ""
echo "==> Setup complete!"
echo "    PostgreSQL: localhost:5432  (user: meetingplanner, pass: devpassword, db: meetingplanner)"
echo "    Frontend:   cd frontend && npm run dev"
echo "    Backend:    cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
