# Short names for commands you run 20 times a day. `make help` lists them.
# NOTE: indentation in Makefiles must be a TAB, not spaces.
# Everything runs through uv: `uv run X` uses the project's .venv, no activate needed.
.PHONY: help install run test lint format check lock upgrade docker

help:            ## list commands
	@grep -E '^[a-z]+:.*##' Makefile | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

install:         ## create .venv with exact locked versions + git hooks
	uv sync
	uv run pre-commit install

run:             ## start the API with auto-reload
	uv run uvicorn app.main:app --reload

test:            ## run tests
	uv run pytest

lint:            ## check style / bugs
	uv run ruff check .

format:          ## auto-fix formatting and imports
	uv run ruff format .
	uv run ruff check --fix .

check: lint test ## what CI runs

lock:            ## re-resolve uv.lock after editing pyproject.toml by hand
	uv lock

upgrade:         ## upgrade all packages within pyproject ranges (review the diff!)
	uv lock --upgrade
	uv sync

docker:          ## build and run the image
	docker build -t app .
	docker run --rm -p 8000:8000 --env-file .env app
