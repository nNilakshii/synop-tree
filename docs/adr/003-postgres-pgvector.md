# ADR-003: Postgres 16 + pgvector

Status: Accepted · Date: 2026-11-17 (PT, PROJECT.md v1.0) · Tracker: P0.2.7

> Stub generated from the PROJECT.md §6 table. Expand with `/adr` when this decision is revisited.

## Context
TODO: the problem and constraints that forced this decision.

## Decision
Postgres 16 + pgvector (Docker `pgvector/pgvector:pg16`)

## Why
One store for relational, vector, FTS and queue; I know Postgres from BidSync

## Alternatives considered
Rejected for now: SQLite (weak concurrency), separate vector DB (extra moving part)

## Consequences
TODO: what gets easier, what gets harder, when to revisit.
