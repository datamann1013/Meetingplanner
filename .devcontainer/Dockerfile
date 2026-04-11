FROM mcr.microsoft.com/devcontainers/javascript-node:22-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3 \
        pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
