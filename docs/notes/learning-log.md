# Learning log

One entry per task where something was non-obvious. Newest first. Dates in PT.

```markdown
## YYYY-MM-DD · <Task ID>: <short title>
**Learned:** what I now understand that I didn't before.
**Surprised me:** what behaved differently than expected, and why.
**Next time:** what I'd do differently (optional).
```

---

## 2026-11-24 · P0.1.1–P0.2.7: Phase 0 setup
**Learned:**
- `uv init --package` gives a `uv_build` backend pinned to the uv minor version (`>=0.13.10,<0.14.0`), so upgrading uv past a minor version means bumping `[build-system]` too.
- Subagents in `.claude/agents/` and hooks are loaded when a Claude Code session starts. A new agent can't be used in the session that created it, but a hook edited mid-session fired right away.
- pydantic-settings: init kwargs beat env vars, and env vars beat `.env`. Keeping secrets (`Secrets`, env-only) apart from `config.yaml` (strict, `extra="forbid"`) avoids `extra="forbid"` choking on unrelated `.env` keys.

**Surprised me:**
- The GitHub repo was still empty even though P0.1.3 was ticked. The checkbox said "pushed" and it wasn't, so verify done-when conditions instead of trusting the tick.
- Ruff 0.17 formats Python code blocks *inside Markdown*. It wanted to rewrite PROJECT.md, so `*.md` is excluded from `ruff format`.
- Three Python 3.12 installs and an old git 2.15 in `/usr/local/bin`. Which binary you get depends on PATH order; `uv run` hides this for Python.

**Next time:** check done-when conditions against reality (`git ls-remote`, `gh run list`) before ticking.
