# Project notes for AI coding assistants (keep under ~50 lines)

## Commands
- Install: `make install` · Run: `make run` · Test: `make test` · Lint/format: `make format`
- Before saying a task is done: `make check` must pass.
- Dependencies: `uv add <pkg>` / `uv add --dev <pkg>` — never pip install, never edit uv.lock by hand.

## Structure
- `src/app/` application code (`main.py` entry with `/health` + `/ready`, `config.py` settings from env)
- New dependency (DB, Redis, model)? Register a check in `READINESS_CHECKS` so `/ready` covers it.
- `tests/` pytest; every new endpoint gets a test
- `docs/decisions.md` record of design decisions

## Rules
- Settings come from env via `app.config.get_settings()`; never hard-code secrets or URLs.
- Small, reviewable changes. Explain non-obvious code with a short comment on WHY.
- Don't add a dependency without saying why it's needed.
