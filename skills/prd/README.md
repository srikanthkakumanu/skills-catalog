# PRD Assembler Skill

**Assembles a Product Requirements Document by pulling confirmed sections from all five upstream files. No new judgment calls — pure assembly only.**

A mechanical skill for synthesizing a final Product Requirements Document (PRD) from completed upstream outputs (BRD, req-nfr-analysis, architecture-decisions, detailed-design, tech-stack). The skill pulls exactly what the section manifest specifies from each file, includes only `status: confirmed` items from gated phases, aggregates all unresolved items into one deduplicated Open Items section, and flags any missing dependencies. No architecture decisions, stack choices, or requirement judgments — it assembles what's already decided.

## Overview

This skill takes the five completed upstream documents and assembles them into a unified `PRD.md` following a fixed section manifest. It's an assembler, not a decision engine: every fact in the PRD traces directly to one of the upstream files. If something is unresolved (pending status, open question, structural finding, unaddressed NFR), it appears in Open Items, not in the main sections. If a file is missing, the skill notes which PRD sections are affected and assembles what's available.

**Key principle:** If it's not confirmed upstream, it doesn't get folded into the PRD as if decided. It gets flagged as open.

## What It Does

The skill executes exactly four sequential steps:

1. **Check File Availability** — Verify which of the five upstream files are present. Note any missing files and which PRD sections they affect.
2. **Walk the Section Manifest** — Pull exactly the content specified in the manifest from each file:
   - Overview & Scope from BRD.md
   - Personas from BRD.md
   - Functional Requirements from req-nfr-analysis.md
   - NFR Summary from req-nfr-analysis.md (Hard-Constraint rows only)
   - Architecture Decision from architecture-decisions.md (only if confirmed)
   - Agentic-AI Fitness from architecture-decisions.md (only if confirmed)
   - Design from detailed-design.md
   - Tech Stack from tech-stack.md (confirmed rows only)
3. **Aggregate Open Items** — Collect every unresolved item from all five files (pending statuses, open questions, structural findings, unaddressed NFRs) into one deduplicated section. Build this last so nothing already resolved gets duplicated.
4. **Produce PRD.md** — Output the assembled document with all sections in manifest order, plus the Open Items section at the end.

Output is always `PRD.md`. A PRD with a non-empty Open Items section is valid and complete — it's not this skill's job to resolve them.

## Key Design Principles

- **Assembler, not decider** — No new judgment calls. Every fact traces to upstream.
- **Confirmed items only** — `status: pending` items from architecture-decisions and tech-stack are listed in Open Items, never folded into main sections.
- **Manifest-driven** — Follow the section manifest exactly. Don't pull "whatever seems relevant."
- **Deduplication** — Open Items are collected once, never repeated from multiple sources.
- **Graceful degradation** — Missing files don't break the whole PRD. Assemble what's available and flag what's missing.

## Input

Five completed upstream documents (all optional, but each provides content for specific PRD sections):

- **BRD.md** (Phase 1) — Domain, personas, use cases, scope boundaries, self-check findings
- **req-nfr-analysis.md** (Phase 2) — Normalized FRs, NFR table (10 categories), structural findings, open questions
- **architecture-decisions.md** (Phase 3) — Architecture Style ADR, Agentic-AI Fitness ADR (both should be confirmed), Open Items
- **detailed-design.md** (Phase 4) — Bounded contexts, patterns, data architecture, API contracts, security model, NFR traceability, Open Items
- **tech-stack.md** (Phase 5) — Technology stack table (all confirmed), under-constrained flags, Open Items

All documents should have `status: confirmed` for their key decisions. Pending items are flagged in Open Items, not assembled as decided.

## Output: `PRD.md`

```markdown
# Product Requirements Document: [System Name]

## Overview & Scope

[Condensed from BRD.md Domain and Scope sections]

**System:** [Name and purpose]
**Scope Boundaries:**
| Module | In-Scope | Out-of-Scope | Reason |
|--------|----------|---|---|
| [module] | [items] | [items] | [reason] |

## Personas

| ID | Name | Role | Top JTBD | Top Pain |
|---|---|---|---|---|
| PER-01 | [Name] | [Role] | [JTBD] | [Pain] |
| ... | ... | ... | ... | ... |

## Functional Requirements

| ID | Requirement | Source |
|---|---|---|
| FR1 | [requirement] | [UC-###] |
| ... | ... | ... |

## NFR Summary

| # | Category | Status | Evidence | Priority |
|---|----------|--------|----------|----------|
| 1 | [Category] | E | [evidence] | HC |
| ... | ... | ... | ... | ... |

*Note: 3 Nice-to-Have and 1 Not-evidenced rows omitted; see req-nfr-analysis.md for complete table.*

## Architecture Decision

**Architecture Style:** Modular Monolith (Status: Confirmed)

**Rationale:** [from architecture-decisions.md]

## Agentic-AI Fitness

**Verdict:** Partial Fit (Status: Confirmed)

**Reasoning:** [from architecture-decisions.md]

## Design

### Bounded Contexts
- **Expense Submission:** Accept and validate receipt uploads
- **Policy Engine:** Evaluate expenses against corporate policy
- **Approvals:** Route expenses to approvers, track state
- **Audit Log:** Record all decisions for compliance

### API Contracts
- Submission → Policy: `POST /policies/evaluate`
- Policy → Approvals: Event `ExpensePolicyPass`
- Approvals: `GET /approvals/{id}` / `POST /approvals/{id}/approve`

### Security Model
- OAuth 2.0 for external users; mTLS for internal services
- Approvers see only their assigned expenses (RBAC by department)
- Agentic decisions (policy eval) logged; approval routing is gated

### NFR Traceability

| HC NFR | Category | Requirement | Addressed By | Design Decision |
|--------|----------|-------------|---|---|
| #1 | Performance | <500ms p95 | **Addressed** | Read-cache-aside (Policy Engine) |
| ... | ... | ... | ... | ... |

## Tech Stack

| Context | Stack | Source/Rationale | Status |
|---------|-------|--|--|
| Expense Submission | Python 3.11 + FastAPI + PostgreSQL 15 | Catalog: `stacks/python-fastapi-postgres-async.md` | Confirmed |
| Policy Engine | Python 3.11 + FastAPI + PostgreSQL 15 + Redis | Catalog: `stacks/python-fastapi-postgres-cached.md` | Confirmed |
| ... | ... | ... | ... |

## Open Items

- **Architectural** (from architecture-decisions.md): None
- **Design** (from detailed-design.md): None
- **Tech Stack** (from tech-stack.md): None
- **Requirements** (from req-nfr-analysis.md):
  - Disaster Recovery (NFR #15): RTO/RPO not specified by stakeholder
  - AI Safety (NFR #18): Which decisions require human approval?
- **Self-Check Findings** (from BRD.md):
  - Unsupported Claim: Domain claims "AI-driven" but no auto-reconciliation use case

```

PRD structure:
- All sections in manifest order
- Confirmed items only (pending items → Open Items)
- Full traceability table for NFRs
- One deduplicated Open Items section at the end
- Notes on omitted rows (e.g., "X rows omitted")

A PRD with a non-empty Open Items section is complete — it's not this skill's job to resolve them.

## How It Works

### Step 1: Check File Availability

Before starting, verify which of the five upstream files are present:

```
✓ BRD.md
✓ req-nfr-analysis.md
✓ architecture-decisions.md
✓ detailed-design.md
✓ tech-stack.md
```

If any are missing, note which PRD sections they affect:
- Missing BRD.md: no Overview, Personas, or BRD self-check items
- Missing req-nfr-analysis.md: no Functional Requirements or NFR Summary
- Missing architecture-decisions.md: no Architecture Decision or Agentic-AI Fitness
- Missing detailed-design.md: no Design section (no Bounded Contexts, API Contracts, Security Model, NFR Traceability)
- Missing tech-stack.md: no Tech Stack section

Assemble what's available and explicitly name the missing files.

### Step 2: Walk the Section Manifest

Follow this exact order and rules:

**1. Overview & Scope** (from BRD.md → Domain, Scope)
- Condense the domain narrative to 1–2 sentences
- Include the Scope table as-is (no edits)

**2. Personas** (from BRD.md → Personas table)
- Include the full personas table
- Don't add or remove rows

**3. Functional Requirements** (from req-nfr-analysis.md → Functional Requirements table)
- Include the full FR table
- Don't add or remove rows

**4. NFR Summary** (from req-nfr-analysis.md → NFR Table)
- Include only Hard-Constraint (HC) rows
- Note how many Nice-to-Have (NTH) and Not-evidenced (NE) rows are omitted
- Example: "Note: 3 Nice-to-Have and 1 Not-evidenced rows omitted; see req-nfr-analysis.md for complete table."

**5. Architecture Decision** (from architecture-decisions.md → Architecture Style ADR)
- Only if `status: confirmed`
- If `status: pending`, do NOT include here; add to Open Items instead
- Include Decision, Why, and Status fields

**6. Agentic-AI Fitness** (from architecture-decisions.md → Agentic-AI Fitness ADR)
- Only if `status: confirmed`
- If `status: pending`, do NOT include here; add to Open Items instead
- Include "Not applicable" verdicts as-is; don't drop them

**7. Design** (from detailed-design.md → sections)
- Pull: Bounded Contexts, Pattern Selection, Data Architecture, API Contracts, Security Model
- Condense to one line per item
- Include NFR Traceability table in full

**8. Tech Stack** (from tech-stack.md → stack table)
- Include only `status: confirmed` rows
- Do NOT include `status: pending` rows; add to Open Items instead
- Flag any `under-constrained` rows explicitly

### Step 3: Aggregate Open Items (Last)

After all main sections, collect every unresolved item from all five files:

**From BRD.md self-check findings:**
- Any flagged contradictions, framing gaps, orphaned scope items

**From req-nfr-analysis.md:**
- All rows from "Open Questions" section
- Any unaddressed NFRs

**From architecture-decisions.md:**
- Any `status: pending` ADRs (style or agentic-AI)
- Any items in the "Open Items" section

**From detailed-design.md:**
- Any under-constrained contexts
- Any items in the "Open Items" section

**From tech-stack.md:**
- Any `status: pending` contexts
- Any `under-constrained` flags
- Any items in the "Open Items" section

**Deduplicate:** If the same item appears in multiple files (e.g., an open question from req-nfr-analysis also noted in architecture-decisions), list it only once under the most specific source.

### Step 4: Produce PRD.md

Output the assembled document with:
- All main sections in manifest order
- Open Items section at the end
- A note at the top if any upstream files are missing

## When to Use

Invoke this skill when:

- You have completed all five upstream phases (BRD, req-nfr-analysis, architecture-decisions, detailed-design, tech-stack)
- All key decisions (architecture, tech stack) are confirmed
- You need a unified PRD that assembles the entire product spec
- You want a single source of truth before handing off to implementation teams
- You need to identify all unresolved items before kicking off development

**Do NOT use this skill for:**

- Making new architecture or tech stack decisions (those are earlier phases)
- Resolving open items (that's a stakeholder decision)
- Changing requirement priorities or scope (those are upstream)
- Writing test strategy or deployment plans (separate concerns)

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes
./install.sh --skill prd

# Or: install to a specific runtime
./install.sh --skill prd --target claude
```

### Invocation

Use natural language or a slash command:

```text
/prd Assemble the PRD from all five completed documents

assemble prd from our completed phases

/prd Generate the final PRD with all confirmed decisions
```

The skill reads the five upstream documents and produces `PRD.md` with all sections in manifest order plus Open Items.

## Files

- **SKILL.md** — Persona directives and 4-step execution protocol
- **README.md** — This file; user-facing reference documentation

## Out of Scope

- **New architecture, stack, or requirement decisions** — Those belong in earlier phases
- **Overriding pending status** — Pending items stay in Open Items, not assembled as decided
- **Test strategy or deployment planning** — Separate concerns addressed after PRD

## Pipeline Context

This skill is **Phase 6** of the complete BRD → Requirements → Architecture → Design → Stack → PRD pipeline:

- **Phase 1 (brd):** Product concept → BRD
- **Phase 2 (req-nfr-analysis):** BRD → normalized requirements
- **Phase 3 (architecture-decisions):** Requirements → confirmed architecture
- **Phase 4 (detailed-design):** Architecture → detailed design
- **Phase 5 (tech-stack):** Design → technology choices per context
- **Phase 6 (prd - this skill):** All five files → unified PRD (pure assembly)
- **Phase 7 (future):** PRD → implementation plan, code structure, deployment

This skill is the bridge between product decisions and engineering implementation.

## Version History

**v1.0** (2026-09-02):

- Initial skill definition: 4-step assembly process, section manifest, open items aggregation
- Frontmatter: `name`, `description`, `license`, `compatibility` (no `models`, `scopes`, `context_optimization`)
- Assembly only: no new decisions, no overriding pending status
- Graceful degradation: missing files noted, not fatal

---

## Questions?

For details on the section manifest or how to handle missing files, see **SKILL.md**. For upstream file formats and what's confirmed, see the README.md files for each phase: [`brd`](../brd/README.md), [`req-nfr-analysis`](../req-nfr-analysis/README.md), [`architecture-decisions`](../architecture-decisions/README.md), [`detailed-design`](../detailed-design/README.md), [`tech-stack`](../tech-stack/README.md).
