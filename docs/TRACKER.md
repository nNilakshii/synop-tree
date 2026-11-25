# synop-tree Tracker

> Design reference: `docs/PROJECT.md` (section numbers like §9.4 point there).
> Dates in PT. Last updated: 2026-11-17.

## How to use this file
- Work top to bottom. **One task ≈ 30–120 min.** If a task takes longer, split it here first.
- Each task has an ID (`P2.4.3`), a checkbox and a **done when** condition. A task is done only when its condition is met **and** `make check` passes.
- Commit message = `<ID>: <summary>`. Tick the box in the same commit.
- Claude Code: `/next-task` picks the first unchecked task in the current phase. `/finish-task` ticks it and commits.
- `⏸` before a task = blocked (write why in **Blockers**). `★` = stretch (skip for MVP).

## Now
- **Current phase:** 0
- **Current task:** P0.3.4
- **Started:** ____ (PT)

## Progress

| Phase | Name | Tasks | Done | Est. h | Start (PT) | End (PT) |
|---|---|---|---|---|---|---|
| 0 | Foundations & MCP 101 | 30 | 23 | 12 | | |
| 1 | Walking skeleton | 24 | 0 | 16 | | |
| 2 | Robust indexer | 44 | 0 | 30 | | |
| 3 | Search + production MCP server | 36 | 0 | 26 | | |
| 4 | Incremental updates | 27 | 0 | 24 | | |
| 5 | Evaluation | 40 | 0 | 42 | | |
| 6 | Ship | 17 | 0 | 16 | | |
| | **Total** | **218** | **23** | **~166** | | |

---

## Phase 0: Foundations & MCP 101 (≈12 h)
**Exit:** CI green on an empty package. A toy MCP server works in MCP Inspector (stdio + HTTP) and in Claude Code. Claude Code workflow (CLAUDE.md, commands, hooks) set up.

### P0.1 Machine and repo setup
- [x] **P0.1.1** Install/verify `uv`, Python 3.12, Docker Desktop, git ≥ 2.40, Node ≥ 20 (for `npx` Inspector), ripgrep (`rg`), Claude Code CLI + VS Code extension. *Done when:* every `--version` prints and is noted in `docs/notes/setup.md`.
- [x] **P0.1.2** Choose the final project name. Check GitHub + PyPI availability. *Done when:* the name is free on both and recorded in Decision log.
- [x] **P0.1.3** Create the public GitHub repo (MIT license, Python `.gitignore`) and clone it. *Done when:* first commit pushed.
- [x] **P0.1.4** `uv init --package`, `requires-python = ">=3.12"`, `src/synop_tree/__init__.py`. *Done when:* `uv run python -c "import synop_tree"` works.
- [x] **P0.1.5** Add dev deps: ruff, pyright, pytest, pytest-asyncio, pre-commit. Config lives in `pyproject.toml`. *Done when:* `uv run ruff check .` and `uv run pyright` run clean.
- [x] **P0.1.6** `Makefile` with `fmt`, `lint`, `typecheck`, `test`, `check`, `db-up`, `db-down`. *Done when:* `make check` passes on an empty test.
- [x] **P0.1.7** `.pre-commit-config.yaml` (ruff, ruff-format, end-of-file-fixer, check-yaml). *Done when:* `pre-commit run --all-files` passes.
- [x] **P0.1.8** GitHub Actions workflow: `uv sync` + `make check` on push/PR, no secrets. *Done when:* the badge is green.
- [x] **P0.1.9** `.env.example` (§15), `.env` in `.gitignore`, `src/synop_tree/config.py` with pydantic-settings loading `.env` + `config.yaml`. *Done when:* a unit test loads config from a temp yaml.
- [x] **P0.1.10** `docker-compose.yml` with `pgvector/pgvector:pg16`, a healthcheck and a named volume. *Done when:* `make db-up` → `psql -c "CREATE EXTENSION vector;"` succeeds.
- [x] **P0.1.11** Copy `PROJECT.md` and `TRACKER.md` into `docs/`. Create `docs/adr/`, `docs/notes/`, `docs/results/`. *Done when:* committed.

### P0.2 Claude Code workflow
- [x] **P0.2.1** Review the provided root `CLAUDE.md` and adjust it to taste. *Done when:* a new Claude Code session can summarize the project rules back correctly.
- [x] **P0.2.2** `.claude/settings.json`: deny `Read(./.env)`, allow `uv run *`, `make *`, `docker compose *`, read-only git. *Done when:* Claude can't read `.env` (test it).
- [x] **P0.2.3** Test the provided slash command `.claude/commands/next-task.md` (reads TRACKER "Now", picks the first unchecked task, restates done-when, plans). *Done when:* `/next-task` returns the first unchecked task of the current phase (verified 2026-11-24: picked P0.1.1, then P0.1.4).
- [x] **P0.2.4** Test the provided slash command `.claude/commands/finish-task.md` (runs checks, ticks the box, updates "Now", commits `<ID>: …`). *Done when:* used successfully once.
- [x] **P0.2.5** PostToolUse hook: `ruff format` on edited `*.py`. *Done when:* an unformatted edit gets auto-formatted.
- [x] **P0.2.6** Subagent `.claude/agents/reviewer.md` (correctness, security, tests, PROJECT.md rules). *Done when:* it reviews one diff with useful comments.
- [x] **P0.2.7** Slash command `.claude/commands/adr.md` that drafts `docs/adr/NNN-*.md`. Create ADR-001…012 stubs from §6. *Done when:* the 12 files exist.
- [x] **P0.2.8** `docs/notes/learning-log.md` template (date, task ID, what I learned, what surprised me). *Done when:* the first entry is written.

### P0.3 MCP 101 (learning)
- [x] **P0.3.1** Read the MCP 2026-07-28 spec: Architecture, Base Protocol, Server Features, Security. Write ≤ 15 lines of notes in `docs/notes/mcp.md` (stateless requests, `_meta`, tools/resources/prompts, deprecations). *Done when:* notes committed.
- [x] **P0.3.2** Read Python SDK v2 docs (quickstart, what's new, migration). Confirm the import paths used in PROJECT.md §12.1 and fix the doc if they differ. Pin the `mcp` version. *Done when:* PROJECT.md §12.1 verified.
- [x] **P0.3.3** `toys/hello_server.py`: `MCPServer("hello")` with 1 tool (`add(a,b)`), 1 resource template (`hello://greeting/{name}`), 1 prompt. *Done when:* it runs over stdio without errors.
- [ ] **P0.3.4** Connect MCP Inspector over stdio. Call the tool, read the resource, get the prompt. *Done when:* screenshot in `docs/notes/`.
- [ ] **P0.3.5** Run the same server over Streamable HTTP (`127.0.0.1:8000/mcp`) and connect Inspector. *Done when:* the tool call works over HTTP.
- [ ] **P0.3.6** Register in Claude Code (`claude mcp add --transport stdio hello -- uv run python toys/hello_server.py`) and ask Claude to use the tool. *Done when:* `/mcp` shows connected and the tool call appears in the transcript.
- [x] **P0.3.7** In-memory test: `async with Client(server)` → call `add`. *Done when:* the pytest passes.
- [ ] **P0.3.8** Experiment: add a `print()` in a stdio tool, observe the breakage in Inspector, then fix it with stderr logging. *Done when:* the learning log entry is written.
- [ ] **P0.3.9** `toys/hello_client.py`: connect over stdio, `list_tools`, call `add`, print the result. *Done when:* the script prints the correct sum.
- [ ] **P0.3.10** Anthropic API smoke test: one Messages call with a single tool (tool_use round trip), printing token usage. *Done when:* the script works with your key.
- [ ] **P0.3.11** Mini-exercise: in `hello_client.py`, convert MCP tool schemas → Anthropic tool definitions and let Claude call `add` through MCP (a 40-line agent loop). *Done when:* Claude answers "what is 17+25" via the MCP tool. *(This is the seed of the eval bridge, P5.3.5.)*

---

## Phase 1: Walking skeleton (≈16 h)
**Exit:** `synop index tests/fixtures/tiny_repo` → `synop mcp serve --stdio` → Claude Code answers "what does this repo do / where is X handled?" using synop-tree tools. Then the same on `psf/requests`.

### P1.1 Database baseline
- [ ] **P1.1.1** Migration runner `src/synop_tree/store/migrate.py` + `schema_migrations` table + `synop db migrate` CLI. *Done when:* applying twice is a no-op.
- [ ] **P1.1.2** `migrations/001_core.sql`: `repos`, `snapshots`, `summaries`, `nodes` (§7, minimal columns OK). *Done when:* migrate succeeds on a fresh DB.
- [ ] **P1.1.3** `store/db.py`: psycopg 3 async pool, `healthcheck()`. *Done when:* `synop db ping` prints OK.
- [ ] **P1.1.4** Test fixture: a separate `synop_test` DB, migrated once per session, truncated per test. *Done when:* two DB tests run in isolation.
- [ ] **P1.1.5** Create `synop_reader` (SELECT only) and `synop_writer` roles in a migration or init script. *Done when:* the reader can't INSERT (test).

### P1.2 Minimal parse and tree
- [ ] **P1.2.1** `tests/fixtures/tiny_repo/` (6 files: package, class with methods, nested dir, README, a test file). *Done when:* committed, with its own `git init` handled by a fixture builder script.
- [ ] **P1.2.2** `ingest/walker.py`: list `.py` files via `git ls-files`. *Done when:* the test lists the fixture files.
- [ ] **P1.2.3** `parse/python_ts.py`: tree-sitter parser wrapper. Extract top-level functions, classes and methods with line ranges. *Done when:* the unit test matches the expected symbols.
- [ ] **P1.2.4** `parse/models.py`: `ParsedSymbol`, `TreeNode` pydantic models. *Done when:* they type-check.
- [ ] **P1.2.5** `tree/builder.py`: build repo → dir → file → class → function with node_keys (`path::Qual.name`). *Done when:* the golden-tree test passes.

### P1.3 Minimal summarizer
- [ ] **P1.3.1** `summarize/client.py`: `LLMClient` protocol + `AnthropicClient` (Messages API, async). *Done when:* a live smoke test (`-m live`) returns text.
- [ ] **P1.3.2** `summarize/fake.py`: deterministic `FakeLLMClient` (summary = f(node_key)). *Done when:* used by tests.
- [ ] **P1.3.3** Prompt v0 (plain-text one-liner) for leaves and parents. *Done when:* the template files exist.
- [ ] **P1.3.4** Post-order scheduler (sequential for now). *Done when:* parents are summarized after their children (asserted in a test).
- [ ] **P1.3.5** Persist snapshot + nodes + summaries, then set the snapshot `ready`. *Done when:* the integration test indexes tiny_repo with the fake client.
- [ ] **P1.3.6** CLI `synop index <path>` (typer) printing node counts, LLM calls and rough cost. *Done when:* it runs on tiny_repo with the real API.

### P1.4 Minimal MCP server
- [ ] **P1.4.1** `mcp_server/server.py`: `MCPServer("synop-tree")`, lifespan opens the read-only DB pool, snapshot from `SYNOP_SNAPSHOT`/latest. *Done when:* the server starts over stdio.
- [ ] **P1.4.2** Tool `repo_overview`. *Done when:* the in-memory test returns the root summary + children.
- [ ] **P1.4.3** Tool `list_children(node)`. *Done when:* the in-memory test passes.
- [ ] **P1.4.4** Tool `read_code(node)` returning source with line numbers. *Done when:* the in-memory test passes.
- [ ] **P1.4.5** `.mcp.json` project entry for synop-tree (stdio). Try it in Claude Code on tiny_repo. *Done when:* the transcript is saved to `docs/notes/skeleton-transcript.md`.

### P1.5 Skeleton on a real repo + retro
- [ ] **P1.5.1** Index `psf/requests` at a fixed SHA. Record nodes, LLM calls, USD, minutes in `docs/results/skeleton.md`. *Done when:* the numbers are recorded.
- [ ] **P1.5.2** Ask Claude Code 5 questions about requests via synop-tree. Note what worked and what was missing. *Done when:* notes committed.
- [ ] **P1.5.3** Retro: list what broke, add any new tasks to Phase 2. *Done when:* the retro is in `docs/notes/retro-p1.md`.

---

## Phase 2: Robust indexer (≈30 h)
**Exit:** 3 SWE-bench repos indexed at one commit each, resumable, inside budget. Human audit < 10% wrong. Stats table in `docs/results/indexing.md`.

### P2.1 Ingestion and filtering (§8.1)
- [ ] **P2.1.1** `ingest/git.py`: bare clone to `workspace/repos/<owner>__<name>.git`, fetch, `worktree_for(sha)` (cached, detached). *Done when:* two SHAs get two worktrees, and a reused SHA isn't re-created.
- [ ] **P2.1.2** `ingest/filters.py`: default ignore globs + config override. *Done when:* the unit test excludes vendor/`_pb2`/migrations.
- [ ] **P2.1.3** Binary sniff (null byte in first 8 KB) + size cap → path-only node. *Done when:* the test covers both.
- [ ] **P2.1.4** Encoding: UTF-8 with replace + flag. *Done when:* a Latin-1 fixture file indexes with a flag.
- [ ] **P2.1.5** `doc` nodes for README / docs md/rst (first 80 lines). Other files become path-only nodes. *Done when:* the tree test shows them.
- [ ] **P2.1.6** `repos` table registration via `synop repo add <slug|url>`. *Done when:* the repo row is created idempotently.

### P2.2 Extraction details (§8.2)
- [ ] **P2.2.1** Signatures including decorators, and docstrings (first string statement). *Done when:* the golden test passes.
- [ ] **P2.2.2** Nested functions/classes as children. *Done when:* the golden test passes.
- [ ] **P2.2.3** Duplicate qualname disambiguation (`#2`), e.g. property setter, `if TYPE_CHECKING` defs. *Done when:* the golden test passes.
- [ ] **P2.2.4** Module preamble (imports, top-level assignments) captured as file own-content. *Done when:* the test passes.
- [ ] **P2.2.5** `migrations/002_edges.sql` + import extraction → edges (resolve in-repo, else `external:<mod>`). *Done when:* the fixture import graph matches the expected edges.
- [ ] **P2.2.6** Parse-error handling: partial parse → `parse_status='partial'`. Unusable → whole-file leaf. *Done when:* the syntax-error and py2 `print x` fixtures pass.
- [ ] **P2.2.7** Test-file tagging (`is_test`). *Done when:* the test passes.
- [ ] **P2.2.8** `tests/fixtures/tricky_repo/` covering all of the above, plus golden snapshot tests. *Done when:* committed and green.

### P2.3 Hashing and identity (§8.3)
- [ ] **P2.3.1** `tree/hashing.py`: normalized `content_hash` (newlines, trailing whitespace). *Done when:* a whitespace-only change gives the same hash, and a comment change gives a different one.
- [ ] **P2.3.2** `merkle_hash` for internal nodes. *Done when:* changing one leaf changes exactly its ancestors' hashes.
- [ ] **P2.3.3** `input_hash` + `summary_key` = sha256(kind|input_hash|prompt_version|model). *Done when:* the unit test passes.
- [ ] **P2.3.4** Fan-out grouping (`tree/grouping.py`): > `max_children` → `group` nodes. *Done when:* a 100-file dir produces 3 groups of ≤ 40.
- [ ] **P2.3.5** Determinism test: indexing the same SHA twice → identical node rows and merkle hashes. *Done when:* the test passes.

### P2.4 Structured summaries (§9)
- [ ] **P2.4.1** `SummaryPayload` pydantic model (§9.2). *Done when:* it type-checks and has a JSON schema export.
- [ ] **P2.4.2** Prompt templates `function.v1`, `class.v1`, `file.v1`, `dir.v1`, `repo.v1` in `summarize/prompts/`. *Done when:* files exist and the renderer test passes.
- [ ] **P2.4.3** Force JSON via a forced tool call (`record_summary`) + pydantic validation + 1 repair retry, else `missing`. *Done when:* the fake client returning bad JSON triggers the retry, then `missing`.
- [ ] **P2.4.4** Code-as-data delimiting + injection-resistant system prompt (§9.3). *Done when:* the template is reviewed by the reviewer subagent.
- [ ] **P2.4.5** Template summaries for trivial nodes (§9.4). *Done when:* the test classifies getters/pass/attr-only `__init__` as trivial.
- [ ] **P2.4.6** Huge-node truncation (§9.5) + `truncated` flag. *Done when:* the test with a 2,000-line function passes.
- [ ] **P2.4.7** Two-tier model routing from config (leaf vs upper). *Done when:* the test asserts the model per level.
- [ ] **P2.4.8** Grounding check: drop unknown `key_symbols`, record them in flags. *Done when:* the test passes.
- [ ] **P2.4.9** Injection heuristic flag. *Done when:* the test with a malicious docstring sets the flag.

### P2.5 Throughput, cost and resilience (§9.7)
- [ ] **P2.5.1** Level-by-level async scheduling with `Semaphore(concurrency)`. *Done when:* a fake client with latency shows parallel speedup in the test.
- [ ] **P2.5.2** Token-bucket rate limiter (RPM + TPM). *Done when:* the unit test enforces limits.
- [ ] **P2.5.3** Retries with exponential backoff + full jitter on 429/529/timeout, honouring `retry-after`. *Done when:* the fake client injecting errors succeeds after retries.
- [ ] **P2.5.4** `migrations/003_llm_calls.sql` + logging every call (tokens, cache tokens, USD, latency). *Done when:* rows are written in the integration test.
- [ ] **P2.5.5** `pricing.yaml` (from Anthropic's pricing page, with the date checked) + cost function. *Done when:* the unit test computes the expected USD.
- [ ] **P2.5.6** `synop estimate <repo> --at <sha>`: node counts by kind, template vs LLM split, token estimate from a 2% sample, USD. No API calls. *Done when:* it runs on requests and flask.
- [ ] **P2.5.7** Budget guard: stop at `max_usd_per_build`, snapshot `failed` with `budget_exceeded`. *Done when:* the test with a tiny cap stops the build.
- [ ] **P2.5.8** Resumability: rerunning a failed/killed build reuses CAS summaries. *Done when:* a kill -9 mid-build, then a rerun, makes 0 duplicate LLM calls for finished nodes.
- [ ] **P2.5.9** Prompt caching for system prompt + tool schema. *Done when:* `cache_read_tokens > 0` on the 2nd+ call (live check).
- [ ] **P2.5.10** ★ Batch API mode (`--batch`) for leaf summaries in full builds. *Done when:* requests is fully indexed via batch.
- [ ] **P2.5.11** Snapshot `stats` JSON (nodes by kind, cache hits, template count, LLM calls, USD, secs, grounding drop rate, flagged). *Done when:* `synop stats <repo>` prints it.

### P2.6 Quality audit and real repos
- [ ] **P2.6.1** Audit script: sample 30 random LLM-summarized nodes → markdown sheet with code + summary + rubric columns. *Done when:* the sheet is generated for requests.
- [ ] **P2.6.2** Rate the 30 nodes (accurate / partial / wrong). Record the wrong-rate and grounding drop rate. *Done when:* results are in `docs/results/audit-v1.md`.
- [ ] **P2.6.3** If wrong-rate > 10%: revise prompts → v2, re-audit. *Done when:* wrong-rate < 10% (or documented why not).
- [ ] **P2.6.4** Run `synop estimate` on 5–6 candidate SWE-bench repos. Pick 3 for Phase 2 and record the choice in the Decision log. *Done when:* the decision is logged.
- [ ] **P2.6.5** Full index of the 3 chosen repos at one SHA each. *Done when:* the `docs/results/indexing.md` table has nodes, % template, % cache, USD, minutes and grounding drop per repo.

---

## Phase 3: Search + production MCP server (≈26 h)
**Exit:** 7 tools + 2 resources + 2 prompts. stdio + Streamable HTTP (auth). Contract tests green. p95 tool latency < 150 ms on the largest indexed repo. Dogfooding in Claude Code for ≥ 2 days.

### P3.1 Embeddings and search (§11)
- [ ] **P3.1.1** `embed/base.py` interface + `embed/local.py` (sentence-transformers, `BAAI/bge-small-en-v1.5`). *Done when:* it embeds 100 texts in the test (marked slow).
- [ ] **P3.1.2** ★ `embed/voyage.py` (`voyage-code-3`). *Done when:* the live smoke test passes.
- [ ] **P3.1.3** `migrations/004_embeddings.sql` with an HNSW index. *Done when:* migrate passes.
- [ ] **P3.1.4** Embed job: all summaries without embeddings → batch embed → insert. *Done when:* the 3 repos are fully embedded.
- [ ] **P3.1.5** Identifier FTS: populate `nodes.ident_fts` with snake/Camel/dotted splitting. *Done when:* a search for `send request` finds `Session.send` and `prepare_request`.
- [ ] **P3.1.6** `search/hybrid.py`: RRF over vector + summary FTS + ident FTS, exact-qualname boost, scope prefix, kinds, include_tests. *Done when:* the unit test checks the fusion math.
- [ ] **P3.1.7** Search smoke set: 20 hand-written queries on a dev repo (not an eval test task) → recall@10. *Done when:* recall@10 ≥ 0.7 is recorded in `docs/results/search-smoke.md`.

### P3.2 Tool surface (§12.2)
- [ ] **P3.2.1** `mcp_server/resolve.py`: accept node_key | path | qualname. On a miss, return the top-3 suggestions. *Done when:* the test for typos returns the correct suggestion.
- [ ] **P3.2.2** `mcp_server/formatting.py`: header line, row formatting, token-budget truncation with explicit note. *Done when:* the test passes.
- [ ] **P3.2.3** Dual output: text + `structured_content`. *Done when:* the contract test reads both.
- [ ] **P3.2.4** `mcp_server/cursor.py`: base64url JSON + HMAC. Reject tampered or foreign-snapshot cursors. *Done when:* the tamper test passes.
- [ ] **P3.2.5** Upgrade `list_children` with cursor + limit + status. *Done when:* pagination over a 100-child node works.
- [ ] **P3.2.6** Tool `get_node(node, detail)`. *Done when:* the contract test passes.
- [ ] **P3.2.7** Tool `search(query, scope, kinds, include_tests, k)`. *Done when:* the contract test passes.
- [ ] **P3.2.8** Tool `find_symbol(name, kind)` (exact + trigram fuzzy). *Done when:* the contract test passes.
- [ ] **P3.2.9** Tool `index_status` (indexed SHA vs worktree HEAD, stale count, policy). *Done when:* the contract test passes.
- [ ] **P3.2.10** Harden `read_code`: path/line inputs, 200-line cap, path-traversal + symlink guard, secret-file denylist. *Done when:* tests for `../../etc/passwd`, a symlink escape and `.env` all fail safely.
- [ ] **P3.2.11** Upgrade `repo_overview` to the final format with the snapshot header. *Done when:* the contract test passes.
- [ ] **P3.2.12** `mcp_server/descriptions.py`: v1 descriptions (when to use, returns, limits, example) for all tools. *Done when:* reviewed by the reviewer subagent.
- [ ] **P3.2.13** Actionable errors (`is_error` + hint) everywhere. *Done when:* every tool has an error-path contract test.

### P3.3 Resources and prompts (§12.3)
- [ ] **P3.3.1** Resource template `synop://{repo}/node/{node_key}`. *Done when:* read via in-memory Client.
- [ ] **P3.3.2** Resource `synop://{repo}/tree` (depth-2 markdown outline). *Done when:* read via in-memory Client.
- [ ] **P3.3.3** Prompt `explore_repo(goal)`. *Done when:* `get_prompt` returns the rendered messages.
- [ ] **P3.3.4** Prompt `localize_issue(issue_text)`. *Done when:* `get_prompt` returns the rendered messages.

### P3.4 Transports and security (§12.4)
- [ ] **P3.4.1** `synop mcp serve --stdio`, structlog → stderr only. A test spawns the server, makes calls, and asserts stdout contains only valid JSON-RPC. *Done when:* the test passes.
- [ ] **P3.4.2** FastAPI app `api/app.py` with `/healthz`, `/repos/{slug}/status`. Mount the MCP `streamable_http_app()` at `/mcp`. *Done when:* Inspector connects over HTTP.
- [ ] **P3.4.3** Bearer-token middleware (required unless bound to 127.0.0.1) + SDK transport security / Origin validation. *Done when:* a missing or wrong token → 401 (test).
- [ ] **P3.4.4** MCP server uses `DATABASE_URL_READONLY`. *Done when:* the test proves a write attempt fails.
- [ ] **P3.4.5** `--enable-admin` flag registering `request_reindex` (enqueues a job). Off by default. *Done when:* the tool list differs with and without the flag (test).
- [ ] **P3.4.6** ★ Tasks extension: expose `request_reindex` as a long-running task (poll status). *Done when:* Inspector shows task progress.

### P3.5 Testing, performance and dogfooding
- [ ] **P3.5.1** Contract test suite covering every tool, resource and prompt (happy + error + pagination + truncation). *Done when:* green in CI.
- [ ] **P3.5.2** Latency benchmark script: p50/p95 per tool on the largest indexed repo. *Done when:* p95 < 150 ms or an index fix is logged.
- [ ] **P3.5.3** Inspector session over HTTP. Screenshots in `docs/`. *Done when:* committed.
- [ ] **P3.5.4** Index the synop-tree repo itself. Point `.mcp.json` at it and use it in Claude Code for ≥ 2 working days. *Done when:* `docs/notes/dogfood.md` has ≥ 10 observations.
- [ ] **P3.5.5** Tool-description v2 from dogfood observations (non-eval repos only). *Done when:* diff + rationale committed.
- [ ] **P3.5.6** Write ADR for the final tool surface (why 7 tools, why these outputs). *Done when:* ADR committed.

---

## Phase 4: Incremental updates (≈24 h)
**Exit:** `synop update` works across real commit ranges with 3 policies. The worker survives crashes. Cost-vs-diff-size curves in `docs/results/incremental.md`.

### P4.1 Snapshot model (§10.3)
- [ ] **P4.1.1** Snapshot lifecycle helpers (`create_building`, `publish_ready` in one txn, `mark_failed`). Readers query `ready` only. *Done when:* the test shows a building snapshot is invisible to tools.
- [ ] **P4.1.2** Base-snapshot selection: nearest `ready` ancestor (`git merge-base --is-ancestor`, newest by commit date), else full. *Done when:* the test on a fixture repo with 5 commits passes.

### P4.2 Diff and planning (§10.1)
- [ ] **P4.2.1** `update/diff.py`: parse `git diff --name-status -M` (A/M/D/R + score). *Done when:* the test with add/modify/delete/rename passes.
- [ ] **P4.2.2** Copy unchanged node rows forward with a single `INSERT … SELECT`. *Done when:* the row count matches and it runs in < 2 s on the largest repo.
- [ ] **P4.2.3** Re-parse changed files only. Handle deletes and renames (rename + same content → cache hit). *Done when:* the rename test shows 0 LLM calls for the moved function.
- [ ] **P4.2.4** Recompute ancestor merkle hashes bottom-up for touched paths only. *Done when:* the test shows only ancestors change.
- [ ] **P4.2.5** Dirty-set computation (input_hash not in CAS). *Done when:* the test passes.
- [ ] **P4.2.6** Large-diff fallback (`full_rebuild_ratio`). *Done when:* the test with 40% changed files triggers full mode.
- [ ] **P4.2.7** `synop update <repo> --to <sha> --policy …` CLI. *Done when:* it works end-to-end on the fixture repo.

### P4.3 Propagation policies (§10.2)
- [ ] **P4.3.1** `eager` policy. *Done when:* the test shows the root re-summarized after a leaf change.
- [ ] **P4.3.2** `threshold` policy (embedding cosine ≥ τ → stop, mark `stale`). *Done when:* the test with a near-identical summary stops propagation.
- [ ] **P4.3.3** `debounced` policy + `refresh_stale` job. *Done when:* the test shows ancestors stale and then refreshed after the job.
- [ ] **P4.3.4** `summary_status` surfaced in all tool outputs + stale count in `index_status`. *Done when:* the contract test shows `[stale]`.

### P4.4 Jobs and workers (§10.3)
- [ ] **P4.4.1** `migrations/005_jobs.sql`. *Done when:* migrate passes.
- [ ] **P4.4.2** `jobs/queue.py`: idempotent `enqueue` (ON CONFLICT DO NOTHING). *Done when:* a double enqueue → 1 row.
- [ ] **P4.4.3** Claim with `FOR UPDATE SKIP LOCKED` + lease. *Done when:* 2 concurrent workers never claim the same job (test).
- [ ] **P4.4.4** Heartbeat (extend lease every 60 s) + reclaim expired leases. *Done when:* the test with a short lease reclaims the job.
- [ ] **P4.4.5** Retries + `dead` after `max_attempts` with `last_error`. *Done when:* the test passes.
- [ ] **P4.4.6** Per-repo advisory lock in the worker. *Done when:* two jobs for the same repo run serially (test).
- [ ] **P4.4.7** `synop worker` CLI (graceful shutdown on SIGTERM). *Done when:* Ctrl-C finishes the current node and releases the lease.
- [ ] **P4.4.8** Crash test: `kill -9` the worker mid-job → second worker completes it. 0 duplicate summaries. *Done when:* the integration test passes.
- [ ] **P4.4.9** `scripts/post-commit` git hook that enqueues HEAD. *Done when:* committing in a test repo enqueues a job.
- [ ] **P4.4.10** ★ `POST /webhooks/github` with HMAC-SHA256 verification. *Done when:* a bad signature → 401 and a good one → job enqueued.

### P4.5 Measurement
- [ ] **P4.5.1** Experiment script: walk 30 consecutive commits of one indexed repo. Per step and per policy, record diff files, dirty nodes, LLM calls, USD and latency, plus full-rebuild cost at 3 checkpoints. *Done when:* the CSV is in `docs/results/`.
- [ ] **P4.5.2** Plots (cost vs diff size per policy, staleness count over time) + a 1-paragraph finding. *Done when:* `docs/results/incremental.md` is committed.
- [ ] **P4.5.3** `synop prune <repo> --keep N` (delete old snapshots, keep CAS). *Done when:* the test passes.
- [ ] **P4.5.4** ★ Resource-updated notification when a new snapshot publishes. *Done when:* a subscribed client receives it.

---

## Phase 5: Evaluation (≈42 h)
**Exit:** pre-registered eval plan, 100 test tasks × C0/C1/C2 (Sonnet-class) + Haiku-class run + ablations + fresh set, with bootstrap CIs and an error analysis in `eval/reports/`.

### P5.1 Dataset (§13.2)
- [ ] **P5.1.1** `eval/datasets/swebench.py`: load SWE-bench Verified from HF with the revision pinned. Cache locally. *Done when:* 500 rows load with the expected fields.
- [ ] **P5.1.2** `eval/datasets/gold.py`: gold files from `patch` (non-test). *Done when:* the unit test on 3 hand-checked instances passes.
- [ ] **P5.1.3** Gold functions: map hunk pre-image ranges → base-commit function nodes. *Done when:* the same 3 instances match a manual check.
- [ ] **P5.1.4** Leakage tags `mentions_gold_file`, `mentions_gold_symbol`. *Done when:* the distribution is printed and sanity-checked.
- [ ] **P5.1.5** Repo selection with `synop estimate` on candidate commits. Cluster by `version`. Record the cost projection and choice in the Decision log. *Done when:* the decision is logged.
- [ ] **P5.1.6** Sample 130 tasks → 30 dev / 100 test (seed fixed, stratified) → `eval/splits.json`. *Done when:* committed. **Do not edit after this.**
- [ ] **P5.1.7** Fresh set: 20–30 post-cutoff tasks (SWE-bench-Live, or self-built from recent merged bug-fix PRs). *Done when:* `eval/fresh.json` is committed with a provenance note.

### P5.2 Index preparation
- [ ] **P5.2.1** Worktree per (repo, base_commit) for all selected tasks. *Done when:* all exist and the script is idempotent.
- [ ] **P5.2.2** Build synop-tree snapshots for every task commit via incremental chaining sorted by commit date (policy = eager). Log total USD. *Done when:* every task has a `ready` snapshot. Total cost recorded.
- [ ] **P5.2.3** Assertion pass: snapshot SHA == `base_commit` for every task, and no gold-patch content in any summary. *Done when:* the check script passes.
- [ ] **P5.2.4** RAG baseline index: raw-code chunk embeddings for the same commits (same embedder). *Done when:* `code_search` returns results for every task commit.
- [ ] **P5.2.5** Stale snapshots for ablation A3 (N commits older, debounced, no refresh). *Done when:* built for test tasks.

### P5.3 Agent harness (§13.4)
- [ ] **P5.3.1** `eval/agent/loop.py`: Messages API loop with tool dispatch, `max_turns`, token caps, stop on `submit_answer`. *Done when:* a scripted fake model test passes.
- [ ] **P5.3.2** `tools_baseline.py`: `list_dir`, `grep` (rg, ≤ 50 matches), `read_file` (≤ 200 lines), all sandboxed to the worktree. *Done when:* the unit tests, including traversal attempts, pass.
- [ ] **P5.3.3** `submit_answer` tool schema (≤ 5 files ranked, ≤ 10 functions, rationale). *Done when:* the schema validation test passes.
- [ ] **P5.3.4** `rag_tool.py`: `code_search(query, k)` with the same output budget as synop-tree `search`. *Done when:* the unit test passes.
- [ ] **P5.3.5** `mcp_bridge.py`: spawn the synop-tree stdio server pinned via env, `list_tools`, convert schemas → Anthropic tools, route calls, close cleanly. *Done when:* the integration test drives 3 synop-tree tools through the bridge.
- [ ] **P5.3.6** `eval/conditions.yaml` (C0, C1, C2, A1, A2, A3) + loader. *Done when:* each condition yields the expected tool list (test).
- [ ] **P5.3.7** Shared system prompt + task prompt templates (identical across conditions). *Done when:* reviewed for fairness by the reviewer subagent.
- [ ] **P5.3.8** JSONL transcript logging (messages, tool calls, tokens, latency). *Done when:* one transcript is inspected by hand.
- [ ] **P5.3.9** Resume (skip finished task×cond×seed) + per-run budget guard. *Done when:* kill and rerun skips finished triples.
- [ ] **P5.3.10** Bounded concurrency across tasks with a shared rate limiter. *Done when:* a 10-task run completes without 429 storms.
- [ ] **P5.3.11** Run config snapshot (`config.json`: model IDs, prompt versions, dataset revision, git SHA of synop-tree). *Done when:* written for every run.

### P5.4 Scoring and stats (§13.5–13.6)
- [ ] **P5.4.1** `score.py`: hit@1/3/5, recall@k, all-gold@5, MRR, function hit@5, tokens, USD, turns, tool calls, wall time. *Done when:* the unit tests on hand-made answers pass.
- [ ] **P5.4.2** `stats.py`: paired bootstrap (10k) CIs on differences vs C0. *Done when:* tested on synthetic data with a known effect.
- [ ] **P5.4.3** McNemar on hit@5. *Done when:* tested on a synthetic table.
- [ ] **P5.4.4** Stratified breakdowns (repo, mentions_gold_file, #gold files). *Done when:* the report shows them.
- [ ] **P5.4.5** Indexing economics: amortized index USD/task + break-even. *Done when:* in the report.
- [ ] **P5.4.6** `report.py` → `eval/reports/<run_id>.md` with tables + plots. *Done when:* generated for the pilot.

### P5.5 Runs
- [ ] **P5.5.1** Write and **freeze** `docs/eval_plan.md` (primary metrics, conditions, split, analysis, stopping rules). *Done when:* committed **before** any test-split run.
- [ ] **P5.5.2** Pilot: 10 dev tasks × C0/C1/C2. Fix harness bugs. Measure USD/task. *Done when:* the pilot report exists and the full-run cost projection is within budget.
- [ ] **P5.5.3** Dev iteration: tool descriptions / system prompt on the dev split only (≤ 3 iterations). *Done when:* the final versions are tagged.
- [ ] **P5.5.4** Main run: 100 test × C0/C1/C2, Sonnet-class agent. *Done when:* complete. Report generated.
- [ ] **P5.5.5** Weak-agent run: 100 test × C0/C1/C2, Haiku-class agent (H3). *Done when:* complete.
- [ ] **P5.5.6** Variance run: 30 test tasks × 3 seeds for C0 and C2. *Done when:* the noise estimate is in the report.
- [ ] **P5.5.7** Ablations A1, A2, A3 on test tasks (Sonnet-class). *Done when:* complete.
- [ ] **P5.5.8** Fresh-set run (C0 vs C2). *Done when:* reported separately.
- [ ] **P5.5.9** Realism check: 20 tasks via Claude Agent SDK with vs without synop-tree (tools restricted explicitly). *Done when:* the summary table is in the report.
- [ ] **P5.5.10** Error analysis: read 20 failures per condition and categorize (wrong area, ran out of turns, misled by summary, etc.). *Done when:* the taxonomy + counts are in the report.
- [ ] **P5.5.11** Final results write-up `docs/results/eval.md` (H1–H4 verdicts with CIs, limitations). *Done when:* committed.

---

## Phase 6: Ship (≈16 h)
**Exit:** public repo tagged v0.1.0 with README, results, demo and write-up. Resume/LinkedIn material drafted from measured numbers only.

### P6.1 Repo polish
- [ ] **P6.1.1** README: what/why (1 paragraph), the note that it's a new project inspired by the 2025 group project, architecture diagram, quickstart (`make db-up`, `synop index`, `claude mcp add …`), tool reference, results table, limitations. *Done when:* a fresh clone works by following the quickstart.
- [ ] **P6.1.2** Architecture diagram as an image (export from §5.1 or redraw). *Done when:* embedded in README.
- [ ] **P6.1.3** `docs/` cleanup: ADRs complete, notes tidy, results linked from README. *Done when:* the links all resolve.
- [ ] **P6.1.4** Test/CI pass: coverage ≥ 80% on core modules, CI badge green. *Done when:* the badge is green.
- [ ] **P6.1.5** `CHANGELOG.md` + tag `v0.1.0` + GitHub release notes. *Done when:* the release is published.
- [ ] **P6.1.6** ★ Publish to PyPI. *Done when:* `uvx synop-tree --help` works.
- [ ] **P6.1.7** Security pass with the reviewer subagent (secrets, traversal, auth, SQL). *Done when:* findings fixed or documented.

### P6.2 Demo and write-up
- [ ] **P6.2.1** Record a 60–90 s demo: Claude Code localizing an issue with synop-tree vs without. *Done when:* the GIF/video is linked in README.
- [ ] **P6.2.2** Blog/write-up draft: problem, design, eval, results (including negative ones), lessons on MCP tool design. *Done when:* the draft is complete.
- [ ] **P6.2.3** Edit pass + publish (personal site / dev.to / Medium). *Done when:* the URL is live.
- [ ] **P6.2.4** Portfolio site entry. *Done when:* live.

### P6.3 Career material (from measured results only)
- [ ] **P6.3.1** Draft 2–3 resume bullets using real numbers from `docs/results/eval.md`. *Done when:* Nilakshi approves every bullet.
- [ ] **P6.3.2** LinkedIn post draft. *Done when:* approved.
- [ ] **P6.3.3** 3 STAR stories from the learning log (e.g. cascade cost, tool-output design, eval leakage control). *Done when:* written in `docs/notes/interview-stories.md`.
- [ ] **P6.3.4** 5-minute verbal walkthrough of the architecture, practiced out loud. *Done when:* recorded once and reviewed.
- [ ] **P6.3.5** Final retro: what I'd do differently, and the next stretch item. *Done when:* `docs/notes/retro-final.md` is committed.
- [ ] **P6.3.6** ★ Pick the first stretch item (§22) and add its tasks here. *Done when:* the tasks are added.

---

## Decision log
| Date (PT) | ID | Decision | Why |
|---|---|---|---|
| 2026-11-17 | — | Scope = hierarchical repo context for agents over MCP, eval on SWE-bench localization | Original summarization framing is solved. This is the open problem |
| 2026-11-17 | P0.1.2 | Project name: **synop-tree** (CLI `synop`, import `synop_tree`) | Free on PyPI + npm. RepoAtlas was taken (repoatlas.com) |
| | P2.6.4 | Phase-2 repos: | |
| | P5.1.5 | Eval repos + task count: | |

## Blockers
| Since (PT) | Task | Blocker | Next action |
|---|---|---|---|
| | | | |

## Parking lot (ideas that came up mid-task, not yet scheduled)
-
