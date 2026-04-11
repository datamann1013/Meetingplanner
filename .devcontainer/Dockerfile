FROM mcr.microsoft.com/devcontainers/javascript-node:22-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        pkg-config \
        postgresql \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
