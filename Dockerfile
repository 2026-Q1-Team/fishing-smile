FROM ghcr.io/astral-sh/uv:python3.13-alpine AS base

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies
WORKDIR /opt/app
COPY pyproject.toml uv.lock ./
RUN \
  --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-install-project

# Install application source code
COPY README.md ./
COPY src/fishing_smile src/fishing_smile/
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked

ENV PATH="/opt/app/.venv/bin:$PATH"

# Switch to non-root executing user
USER 1000:1000
WORKDIR /opt/app/workdir
ENTRYPOINT ["fishing-smile"]
CMD []

