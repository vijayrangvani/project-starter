# Project name

> One sentence: what this does and for whom.

<!-- Demo GIF or screenshot here. Recruiters look at this first. -->

## Problem
What real problem does this solve? Who has it? Why do existing approaches fall short?

## Architecture
```
client -> FastAPI -> (DB / LLM / queue ...)
```
Short explanation of each component and how a request flows through.

## Tech stack
| Layer | Choice | Why |
|---|---|---|
| API | FastAPI | |
| ... | | |

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
cp .env.example .env
make install
make run          # http://localhost:8000/docs
make test
```

## Key decisions & trade-offs
See [docs/decisions.md](docs/decisions.md). Summarise the 2–3 most important here.

## What I'd do next
Honest limitations and the next improvements (shows engineering judgement).
