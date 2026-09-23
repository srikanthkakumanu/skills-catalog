# Spring Boot 4 · Spring Modulith

A modular monolith: module boundaries enforced within one deployable, without microservices
operational cost. Only fits when the architecture style ADR actually calls for a monolith.

## Fits
- **Team/deploy shape:** single team, single deploy cadence — the checklist `architecture-decisions`
  already runs (independent scaling? single team/cadence? avoid-over-engineering signal? bursty
  work?) should have landed on monolith or modular monolith, not microservices
- **Structural need:** enforced module boundaries and reliable in-process module events, without
  splitting into separate services

## Does NOT fit
- Architecture style ADR confirms microservices with independent per-context scaling — this
  playbook doesn't fit regardless of any other constraint; that ADR already ruled out a single
  deployable
- A trivial, unrelated change to an existing endpoint — don't restructure into modules for
  something this doesn't touch

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| Structure | Spring Modulith 2.x matched to the exact Boot 4 minor (not a Boot 3 Modulith 1.x BOM) |
| Cross-module communication | Public module API or a durable module event — never reach into another module's internal package |
| Event durability | Persistent publication tracking — `ApplicationModuleListener` alone does not guarantee delivery |

## Prerequisites
- Module verification (dependency-rule and cycle checks) run as part of the test suite, not left implicit
- Events published as immutable contracts, never an entity with lazy associations

## Tradeoffs
- Easier migration path to real microservices later if module boundaries are honest from the
  start; harder to retrofit if boundaries were never enforced

## Implementation detail
`implementation-guide` (Phase 7) — spring-modulith, multi-tenancy.
