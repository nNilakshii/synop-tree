# synop-tree

Hierarchical repo-context service for coding agents, served over MCP.
- Design (source of truth): docs/PROJECT.md. Section refs like §9.4 point there.
- Task list: docs/TRACKER.md. Work in order, one task per commit. The "Now" section says where we are.

## Current status
Phase 0 (foundations). Most commands below don't exist yet: they're created by Phase 0/1 tasks.
Don't assume a file or command exists. Check first, and if it's missing, say which tracker task creates it.

## Naming
repo/PyPI `synop-tree` · import package `synop_tree` (src/synop_tree/) · CLI `synop` · MCP server name `synop-tree`
· URI scheme `synop://` · env prefix `SYNOP_` · DB roles `synop_reader` / `synop_writer`.

## Commands (once created)
- `make check`: ruff format+lint, pyright, pytest (must pass before every commit)
- `make db-up` / `make db-down`: Postgres+pgvector via docker compose
- `uv run synop db migrate`: apply migrations
- `uv run synop index <path-or-slug> --at <sha>` · `uv run synop update <slug> --to <sha>`
- `uv run synop mcp serve --stdio` | `--http --port 8765`

## Architecture (one line each)
ingest → parse (tree-sitter) → tree + hashes → plan → summarize (CAS cache, budget guard) → embed → Postgres.
MCP server (src/synop_tree/mcp_server) is read-only. The worker (src/synop_tree/jobs) is the only writer.

## Workflow
- Start a task with /next-task, end it with /finish-task.
- Plan before code for anything non-trivial. Write the failing test first.
- If code and docs/PROJECT.md disagree, flag it and update the doc in the same commit.
- Dates and timestamps in Pacific Time.

## Rules
- Python 3.12, async I/O, type hints everywhere, pydantic for data models.
- Never call real LLM APIs in tests: use the FakeLLMClient (summarize/fake.py).
- Never hard-code model IDs or prices: read config.yaml / pricing.yaml.
- Never write to stdout inside src/synop_tree/mcp_server (stdio transport). Log to stderr via structlog.
- Never read or print .env or any secret.
- DB changes = a new file in migrations/. Never edit an applied migration.
- Don't modify eval/splits.json or docs/eval_plan.md once frozen.
- Small, reviewable diffs. Ask before adding a dependency. Never push. I push.
