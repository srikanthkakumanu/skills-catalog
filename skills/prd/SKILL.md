---
name: prd
description: Assembles a Product Requirements Document purely by pulling fixed sections from BRD.md, req-nfr-analysis.md, architecture-decisions.md, detailed-design.md, and tech-stack.md per a section manifest. Makes no architecture, stack, or requirement judgments of its own — every upstream item must already be confirmed, or it's flagged, not decided here.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "lightweight tier throughout — this skill only extracts, filters by status, and deduplicates; it never needs reasoning-tier judgment"
---
# PRD Assembler Skill

## Directives
1. Assembler only — no new judgment calls. Every fact in the PRD traces to one of the five upstream files.
2. Only `status: confirmed` items are included from `architecture-decisions.md` and `tech-stack.md`. A `pending` item is never assembled as if decided — it's listed in Open Items instead.
3. Follow the section manifest below exactly — pull the named source, not "whatever seems relevant."
4. Aggregate every upstream file's unresolved items (Open Questions, Structural Findings, unaddressed NFRs, under-constrained stacks, any pending status) into one deduplicated Open Items section — never repeat the same item under multiple sources.
5. A missing required upstream file blocks only the sections that depend on it — assemble what's available, and name the missing file explicitly rather than omitting the section silently.
6. Out of pipeline scope by prior decision: no test strategy, no deployment plan.
7. **Cost control** — this entire skill is lightweight-tier work: extraction, status filtering, and deduplication, never original judgment. If a step ever seems to need reasoning-tier weighing of options, that step belongs in an upstream skill, not here — don't do it, flag it instead.
8. **Context** — read each upstream file once, pull only the manifested section per row below; don't reload a file already read earlier in the same run.

## Section Manifest

| PRD Section | Source file → section | Rule |
|---|---|---|
| Overview & Scope | `BRD.md` → Domain, Scope | condensed; keep in/out-of-scope table as-is |
| Personas | `BRD.md` → Personas | full table |
| Functional Requirements | `req-nfr-analysis.md` → Functional Requirements | full table |
| NFR Summary | `req-nfr-analysis.md` → NFR Table | Hard-Constraint rows only by default; note count of Nice-to-Have/Not-evidenced rows omitted |
| Architecture Decision | `architecture-decisions.md` → Architecture Style | only if `status: confirmed`; else list under Open Items |
| Agentic-AI Fitness | `architecture-decisions.md` → Agentic-AI Fitness | only if `status: confirmed`; include a "not applicable" verdict as-is, don't drop it |
| Design | `detailed-design.md` → Bounded Contexts, Pattern Selection, Data Architecture, API Contracts, Security Model | condensed to one line per item; keep NFR Traceability table in full |
| Tech Stack | `tech-stack.md` → stack table | confirmed rows only; `under-constrained` rows flagged, not silently included |
| Open Items | all five files | deduplicated list — every pending status, open question, structural finding, and unaddressed NFR, once each |

## Process
1. Check which of the five files are present. Missing files: note which PRD sections are affected.
2. Walk the manifest top to bottom, pulling exactly the listed content per rule.
3. Build Open Items last, after the other sections, so nothing already resolved gets duplicated into it.
4. Produce `PRD.md`.

## Output: `PRD.md`
Sections in manifest order, plus a final `## Open Items` list. A PRD with a non-empty Open Items section is a valid, complete assembly — it is not this skill's job to resolve them.

## Out of Scope
- Any new architecture, stack, requirement, or design decision.
- Overriding an upstream `pending` status to include it anyway.
- Test strategy, deployment plan, CI/CD.
