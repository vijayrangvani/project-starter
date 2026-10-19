# project-starter

A lean Python/FastAPI template I use to start new projects with tests, linting, CI and Docker already working — so day one is spent on the actual problem, not setup.

## What you get
| Piece | Choice | Why |
|---|---|---|
| Dependencies | uv + `uv.lock` | Fast, reproducible installs; CI fails if the lock is stale |
| API | FastAPI | Most of my AI/backend projects end up served behind an API |
| Config | pydantic-settings | All settings from env vars, validated at startup; no secrets in code |
| Health | `/health` + `/ready` | Liveness never checks dependencies (a slow DB shouldn't restart the pod); readiness runs registered checks (each with its own client timeout) and returns 503 on failure |
| Quality | ruff, pytest, pre-commit | `make check` runs the same lint, format and test steps as CI (CI also builds the Docker image) |
| Container | Dockerfile | Cached dependency layer, locked versions, no dev deps, non-root user |
| Decisions | `docs/decisions.md` | Record of why each choice was made |

Deliberately **not** included: databases, LLM clients, RAG, auth. Each project needs different ones; they get added when a real project needs them.

## Start a new project from it
1. On GitHub: **Use this template → Create a new repository**, then clone it.
2. Rename the project in `pyproject.toml` (`name`, `description`) and `APP_NAME` in `.env.example`.
3. `README.md` is already the project README template: replace every `<PLACEHOLDER>`, delete sections that don't apply, then delete `docs/STARTER.md`.
4. Run it:
   ```bash
   # one-time: install uv  →  curl -LsSf https://astral.sh/uv/install.sh | sh
   cp .env.example .env
   make install   # .venv with locked versions + git hooks
   make check     # lint + format check + tests — must pass before the first commit
   make run       # http://localhost:8000/docs
   ```
5. Adding a dependency such as a database? `uv add <pkg>`, then register a check in `READINESS_CHECKS` in `src/app/main.py` so `/ready` covers it, using the client's own timeout.

Not building an API (CLI, pipeline, batch job)? See [Not building an API?](#not-building-an-api) below.

## Commands
`make help` lists them all: `install`, `run`, `test`, `lint`, `format`, `check`, `lock`, `upgrade`, `docker`.

## Not building an API?

This starter defaults to FastAPI. For a CLI tool, data pipeline or batch job, keep everything else and change 4 things:

1. **Dependencies:** `uv remove fastapi uvicorn` (keep `pydantic-settings`), then `uv add` what you need. Commit `pyproject.toml` and `uv.lock` together.
2. **Entry point:** replace `src/app/main.py` with a plain `run() -> int` function and `if __name__ == "__main__": raise SystemExit(run())`.
3. **Test:** replace `tests/test_health.py` with `assert run() == 0`.
4. **Run + Docker:** in the `Makefile`, change `run` to `uv run python -m app.main`. Delete the `Dockerfile` and the CI `docker build` step if nothing is deployed; otherwise set `CMD ["python", "-m", "app.main"]` and drop `EXPOSE 8000`.

Then run `make check`: it should pass before your first real commit.
