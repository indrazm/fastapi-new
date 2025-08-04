#!/bin/sh
set -e  # Exit on any error

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting the application..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000