# synop-tree

Hierarchical repo context for coding agents, served over MCP.

synop-tree builds a tree of LLM-written summaries for a codebase (function → class → file → directory → repo), keeps it fresh incrementally on every commit, and serves it to coding agents like Claude Code through an MCP server. It ships with a controlled evaluation on SWE-bench Verified bug localization.

**Status:** early development. Design: [`docs/PROJECT.md`](docs/PROJECT.md) · Progress: [`docs/TRACKER.md`](docs/TRACKER.md)

## License
MIT
