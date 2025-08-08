FROM node:24-slim as base

ENV NODE_ENV=development

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /frontend

RUN useradd --create-home --shell /bin/bash appuser && \
    mkdir -p /frontend && \
    chown -R appuser:appuser /frontend

USER appuser

COPY --chown=appuser:appuser package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY --chown=appuser:appuser . .