---
description: Draft an ADR in docs/adr/ for a decision
---
Draft an Architecture Decision Record for: $ARGUMENTS

1. Look at `docs/adr/` and pick the next number `NNN` (zero-padded, 3 digits). If the decision updates an existing ADR, edit that file instead and say so.
2. Read the docs/PROJECT.md sections the decision touches (the §6 table is the ADR summary) and any related ADRs.
3. Write `docs/adr/NNN-<short-kebab-title>.md` with these sections:
   - `# ADR-NNN: <Title>`
   - `Status:` Proposed | Accepted | Superseded by ADR-XXX · `Date:` today (PT) · `Tracker:` related task IDs
   - `## Context`: the problem and the constraints that force a decision.
   - `## Decision`: what we do, in one or two sentences, then details.
   - `## Alternatives considered`: each option with why it lost *for now*.
   - `## Consequences`: what gets easier, what gets harder, what we must watch, and when to revisit.
4. Keep it under ~40 lines. Mark facts you couldn't verify with `TODO(verify)`. Don't invent benchmark numbers.
5. If the decision changes the design, update the §6 table row in docs/PROJECT.md in the same change.
6. Show me the draft. Don't commit.
