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

# Create non-root user and workspace
RUN useradd --create-home --shell /bin/bash appuser && \
    mkdir -p /backend && \
    chown -R appuser:appuser /backend

WORKDIR /backend

# Copy application files with correct permissions
COPY --chown=appuser:appuser pyproject.toml .
COPY --chown=appuser:appuser uv.lock .

COPY --chown=appuser:appuser . .
RUN chmod +x .docker/entrypoint.dev.sh

# Switch to non-root user
USER appuser
