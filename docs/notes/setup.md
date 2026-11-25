# Dev machine setup (P0.1.1)

Checked: 2026-11-24 23:33 PST · macOS 26.5 (Apple silicon)

| Tool | Required | Installed | Path |
|---|---|---|---|
| uv | any recent | 0.13.10 | `~/.local/bin/uv` |
| Python | 3.12 | 3.12.5 | `/opt/homebrew/opt/python@3.12/bin/python3.12` (what `uv python find 3.12` picks) |
| git | ≥ 2.40 | 2.46.1 | `/opt/homebrew/bin/git` |
| Node | ≥ 20 (for `npx` MCP Inspector) | 20.19.0 | |
| npx | (ships with Node) | 10.8.2 | |
| ripgrep | any | 14.1.1 | |
| Docker Desktop | any | Docker 29.9.3, Compose v5.7.0 | `/usr/local/bin/docker` |
| Claude Code CLI | any | 2.1.332 | `~/.local/bin/claude` |
| Claude Code VS Code extension | any | 2.1.330 | |
| gh (extra) | n/a | 2.102.0 | |

## Gotchas
- **Old git on PATH:** `/usr/local/bin/git` is 2.15.0 and `/usr/bin/git` is Apple's. The Homebrew 2.46.1 wins only because `/opt/homebrew/bin` comes first in PATH. Keep that order.
- **Several Python 3.12 installs** (Homebrew, python.org framework, `/usr/local/bin`). Doesn't matter as long as everything runs through `uv run`.
- **Docker daemon** must be running (open Docker Desktop) before `make db-up` (P0.1.10). `docker info` fails until then.

## Re-check
```bash
uv --version; uv python find 3.12; git --version; node --version; npx --version
rg --version | head -1; docker --version; docker compose version; claude --version
```
