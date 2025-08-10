FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY . .

RUN chmod +x .docker/entrypoint.sh
