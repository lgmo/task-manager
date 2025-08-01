#!/bin/bash
uv sync --all-extras --dev

uv run src/manage.py collectstatic --noinput
uv run src/manage.py makemigrations
uv run src/manage.py migrate

echo "Ready!"

tail -f /dev/null
