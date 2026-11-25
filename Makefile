.PHONY: fmt lint typecheck test check db-up db-down

# Apply formatting and autofixable lint fixes.
fmt:
	uv run ruff format .
	uv run ruff check --fix .

# Read-only checks (never modify files).
lint:
	uv run ruff format --check .
	uv run ruff check .

typecheck:
	uv run pyright

test:
	uv run pytest

# Must pass before every commit.
check: lint typecheck test

# Postgres + pgvector (docker-compose.yml arrives in P0.1.10).
db-up:
	docker compose up -d --wait

db-down:
	docker compose down
