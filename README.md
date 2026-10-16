# project-starter

A lean Python/FastAPI template I use to start new projects with tests, linting, CI and Docker already working — so day one is spent on the actual problem, not setup.

## What you get
| Piece | Choice | Why |
|---|---|---|
| Dependencies | uv + `uv.lock` | Fast, reproducible installs; CI fails if the lock is stale |
| API | FastAPI | Most of my AI/backend projects end up served behind an API |
| Config | pydantic-settings | All settings from env vars, validated at startup; no secrets in code |
| Health | `/health` + `/ready` | Liveness never checks dependencies (a slow DB shouldn't restart the pod); readiness runs registered checks with a timeout and returns 503 on failure |
| Quality | ruff, pytest, pre-commit | Same checks locally (`make check`) and in CI |
| Container | Dockerfile | Cached dependency layer, locked versions, no dev deps, non-root user |
| Decisions | `docs/decisions.md` | Record of why each choice was made |

Deliberately **not** included: databases, LLM clients, RAG, auth. Each project needs different ones; they get added when a real project needs them.

## Start a new project from it
1. On GitHub: **Use this template → Create a new repository**, then clone it.
2. Rename the project in `pyproject.toml` (`name`, `description`) and `APP_NAME` in `.env.example`.
3. Replace this README with [`docs/README_TEMPLATE.md`](docs/README_TEMPLATE.md) and fill it in.
4. Run it:
   ```bash
   # one-time: install uv  →  curl -LsSf https://astral.sh/uv/install.sh | sh
   cp .env.example .env
   make install   # .venv with locked versions + git hooks
   make check     # lint + format check + tests — must pass before the first commit
   make run       # http://localhost:8000/docs
   ```
5. Adding a dependency such as a database? `uv add <pkg>`, then register a check in `READINESS_CHECKS` in `src/app/main.py` so `/ready` covers it.

Not building an API (CLI, pipeline, batch job)? See "Not building an API?" in the README template.

## Commands
`make help` lists them all: `install`, `run`, `test`, `lint`, `format`, `check`, `lock`, `upgrade`, `docker`.
