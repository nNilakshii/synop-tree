# MCP 2026-07-28: notes (P0.3.1, read 2026-11-24)

1. **Stateless core:** every request carries everything needed. `initialize`/`initialized` and `Mcp-Session-Id` are removed; old-era clients fall back to the legacy handshake.
2. **Per-request `_meta`:** `io.modelcontextprotocol/protocolVersion` + `/clientCapabilities` (required), `/clientInfo` (should), `/logLevel` (optional). Missing → -32602 / HTTP 400.
3. **`server/discover`:** servers MUST implement it (versions, capabilities, `instructions`, `ttlMs`/`cacheScope`); clients may skip it.
4. **Streamable HTTP:** one POST per message; headers `MCP-Protocol-Version`, `Mcp-Method`, and `Mcp-Name` for tools/call, resources/read, prompts/get. No GET stream, no SSE resumability.
5. **HTTP security:** MUST validate `Origin` (403 if invalid: DNS rebinding); SHOULD bind 127.0.0.1; SHOULD authenticate.
6. **stdio:** stdout carries only newline-delimited MCP messages; stderr is free for logs. That's why `mcp_server/` never prints.
7. **Tools:** result = `content[]` + optional `structuredContent` (+ the same JSON as a text block) + `isError`. Execution errors → `isError: true` so the model can self-correct; protocol errors → JSON-RPC error.
8. **Resources:** URIs per RFC 3986, templates per RFC 6570; servers MUST validate URIs and sanitize paths. Not found → -32602 (old -32002 retired).
9. **Prompts:** named templates with string arguments → list of `user`/`assistant` messages.
10. **Pagination:** cursors are opaque to clients; missing `nextCursor` = end. Invalid cursor → -32602. Fits our HMAC'd cursor (§12.2).
11. **Deprecated (SEP-2577, ≥ 12 months notice):** Roots, Sampling, Logging. Use tool params, direct LLM APIs, stderr/OTel. HTTP+SSE deprecated since 2025-03-26.
12. **Server→client requests** (elicitation, sampling) became MRTR: `input_required` results + client-round-tripped `requestState`. So "stateless" ≠ no state at all.
13. **Extensions** are opt-in on both sides via `capabilities.extensions`; Tasks (`io.modelcontextprotocol/tasks`) moved out of core into one (stretch for `request_reindex`).
