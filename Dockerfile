# keep in step with .python-version
FROM python:3.14-slim
# uv binary from the official image (pinned version)
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /bin/uv
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
# 1) dependencies only — this layer is cached until pyproject.toml / uv.lock change
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
# 2) then the code + the project itself
COPY src ./src
RUN uv sync --locked --no-dev
ENV PATH="/app/.venv/bin:$PATH"
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
