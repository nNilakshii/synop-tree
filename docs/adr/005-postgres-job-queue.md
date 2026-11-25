# ADR-005: Postgres-backed job queue

Status: Accepted · Date: 2026-11-17 (PT, PROJECT.md v1.0) · Tracker: P0.2.7

> Stub generated from the PROJECT.md §6 table. Expand with `/adr` when this decision is revisited.

## Context
TODO: the problem and constraints that forced this decision.

## Decision
Postgres-backed job queue (`FOR UPDATE SKIP LOCKED` + leases)

## Why
Fewer moving parts. The learning focus is MCP, not brokers

## Alternatives considered
Rejected for now: Redis/arq, Kafka (revisit only if throughput demands)

## Consequences
TODO: what gets easier, what gets harder, when to revisit.
