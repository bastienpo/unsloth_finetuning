FROM python:3.12-slim AS build 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ninja-build \
    libopenblas-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY ./pyproject.toml .

RUN uv venv opt/venv && uv pip install -r pyproject.toml

FROM python:3.12-slim-bullseye
COPY --from=build /opt/venv /opt/venv

COPY ./src .

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["gunicorn", "-w", "2", "web.app:app"]
