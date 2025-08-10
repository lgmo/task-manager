FROM node:24-slim as base

WORKDIR /frontend

RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip

RUN curl -fsSL https://bun.sh/install | bash

COPY . .

RUN chmod +x .docker/entrypoint.sh