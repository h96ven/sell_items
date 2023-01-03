#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
alembic revision --autogenerate
alembic upgrade head

# Start server
echo "Starting server"
uvicorn app.main:app --reload --host 0.0.0.0