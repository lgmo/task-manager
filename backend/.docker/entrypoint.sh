#!/bin/bash
uv sync --all-extras --dev

uv run src/manage.py makemigrations
uv run src/manage.py migrate

if [ "$ENV" = "prod" ]; then
    uv run src/manage.py collectstatic --noinput
else
    uv run src/manage.py runserver 0.0.0.0:8000
fi