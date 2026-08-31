---
name: req-nfr-analysis
description: Requirements analysis skill that normalizes functional or business requirements, extracts and tags every requirement across 19 NFR categories (18 named plus "Other"), flags inferred NFRs the BRD implies but never states, and prioritizes each NFR as hard constraint vs nice-to-have for downstream architecture/design phases. Consumes BRD output, produces requirements-to-architecture input with complete gap analysis and stakeholder questions.
license: Apache-2.0
compatibility: Antigravity 2.x, Claude Code, OpenAI Codex
models:
  reasoning_tier:
    gemini: gemini-2.5-pro / gemini-3.7-flash
    claude: claude-3-7-sonnet / claude-3-5-sonnet
    codex: gpt-4o / o3-mini
  lightweight_tier:
    gemini: gemini-2.5-flash / gemini-2.0-flash-lite
    claude: claude-3-5-haiku
    codex: gpt-4o-mini
context_optimization:
  progressive_loading: true
  chunked_synthesis: false
  subagent_delegation: false
  state_saving_split: false
scopes:
  supported: ["quick", "standard", "thorough"]
  default: "quick"
flags:
  ask_gaps:
    invocation: "--ask-gaps"
    default: false
    description: >
      When set, Step 4 gap questions are asked directly to the user in the conversation
      and answers are resolved into the NFR table (Section 2) instead of only being
      listed as Open Questions.
---
# Phase 1: Requirements & NFR Analysis

## Core Directives (Reference These)

| #           | Directive                          | Key Rule                                                                                                                                                                                                                                                                |
| :---------- | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | Pure Requirements Analysis         | Extract functional requirements systematically; no architecture or tech recommendations                                                                                                                                                                                 |
| **2** | Five-Step Execution Protocol       | Execute steps 1–5 sequentially; none skipped or merged                                                                                                                                                                                                                 |
| **3** | Complete NFR Coverage              | All 19 categories in every output, even "Not evidenced" rows                                                                                                                                                                                                            |
| **4** | Strict Context Window Optimization | Progressive reference loading; inline only category names, reference taxonomy/patterns for details                                                                                                                                                                      |
| **5** | Strict Scope Boundary Control      | Calibrate depth to scope: quick (minimal essential set, no production-grade-hardening questions for deferred categories), standard (all 19 NFRs + applicable questions), thorough (production-grade rigor across all 19, complete gap coverage, cross-NFR dependencies) |
| **6** | Gap Resolution Invocation          | `--ask-gaps` turns Step 4 from "list questions" into "ask, wait, resolve into NFR table"; omit flag for default static-question behavior                                                                                                                              |

Note: **Directive 4: Strict Context Window Optimization** and **Directive 5: Strict Scope Boundary Control** guide progressive loading and scope calibration respectively; see their rows above for full details.

---

## Overview

This skill systematically analyzes a completed Business Requirements Document (BRD) to extract, normalize, and prioritize functional and non-functional requirements. It serves as the bridge between requirements definition and architecture/design phases.

**Important:** This skill **does not** recommend an architecture, pattern, or tech stack—that is out of scope and reserved for downstream phases that consume this output.

## When to Use

Invoke this skill when:

- A BRD is provided and needs normalization or NFR extraction
- User explicitly asks for "requirement analysis" or "requirements analysis"
- User is ready to move from requirements into architecture/design
- User declares BRD "done" and asks "what's next?" in a requirements→architecture pipeline
- An incomplete BRD needs structured gap identification

## Execution Steps (Sequential—None Skipped or Merged)

### Step 1: Extract Functional Requirements

Walk systematically through every use case, acceptance criterion, and requirement row in the provided BRD. For each one:

- Write one normalized line per requirement
- Use short imperative statements with source references (e.g., "UC-3.2: System shall validate user credentials against LDAP", source: UC-3)
- Keep purely functional—do not mix in NFR language even if the BRD phrases a single sentence as both
- Separate "System shall persist data" (functional) from "System shall persist data with 99.95% durability" (durability is Reliability/Resilience NFR)

Output: A table with columns: **ID, Requirement, Source**

### Step 2: Tag Every NFR Across 19 Categories

For every requirement (including inferred ones), determine its NFR classification:

- Classify across the 18 named categories listed in `references/nfr-taxonomy.md` (Performance, Latency, Scalability, Availability, Reliability, Resilience/Fault Tolerance, Security, Compliance/Regulatory, Data Privacy, Maintainability, Usability/Accessibility, Interoperability, Portability, Observability, Disaster Recovery/Business Continuity, Capacity/Resource Efficiency, Explainability/Transparency, AI Safety/Autonomy Control)
- Tag each as one of: **Explicit** (stated clearly in BRD), **Inferred** (implied but never stated—see gap-patterns in references), **Not evidenced** (absent), or **Deferred (Quick Scope)** (identified as applicable to the system but falls outside quick scope's minimal essential set; quick scope only, never used at standard or thorough)
- If a requirement is clearly NFR-shaped but does not fit the 18 categories, assign it to the 19th category **"Other/Uncategorized"** with a one-line justification of why it doesn't fit elsewhere (never as a shortcut between two close categories)
- Never upgrade an Inferred NFR to Explicit by inventing a plausible number or threshold
- **Scope-specific tagging:**
  - **Quick scope:** Walk all 19 categories; mark those outside the minimal essential set (one container per app/microservice, one DB, one AI agent per need — no redundancy, HA, or scaling) as `Deferred (Quick Scope)`. Evidence explains what was identified and why it's deferred (e.g., "UC-2 implies multi-region reads, but quick scope assumes single-instance deployment — deferred").
  - **Thorough scope:** Walk all 19 categories with **production-grade rigor** — assume multi-instance/redundant/HA deployment posture, and expect real targets (SLA %, latency budget, RTO/RPO, compliance framework) where the domain calls for one. Never use `Deferred (Quick Scope)` at thorough; every category resolves to `Explicit`, `Inferred`, or `Not evidenced`.

Output: A table with columns: **#, Category, Status (Explicit/Inferred/Not evidenced/Deferred (Quick Scope)), Evidence (cite BRD section), Priority** — always 19 rows, one per category

### Step 3: Prioritize Each NFR

For every NFR (all 19 categories), classify as either **Hard Constraint** or **Nice-to-Have**:

- Hard Constraint = system does not functionally work or fails a stated KPI without it; includes load-bearing Inferred NFRs
- Nice-to-Have = improves experience/performance but system works without it; includes anything BRD explicitly defers
- Spell out the reasoning rule for each decision
- Where priority is genuinely unclear, route to "Open Questions" section instead of guessing
- Document assumptions transparently
- **Scope-specific rules:**
  - **Quick scope:** `Deferred (Quick Scope)` rows get Priority `—` (same as `Not evidenced` rows). Only prioritize categories in the minimal essential set.
  - **Thorough scope:** Categories like Disaster Recovery, Compliance, and Security are near-always Hard Constraint at production-grade rigor (consistent with the load-bearing Inferred NFRs rule), reflecting that a production system cannot ship without them even if the BRD is silent.

### Step 4: Ask for Real Gaps (Not Assumptions)

Identify patterns in the BRD that suggest missing requirements or context. Consult `references/gap-patterns.md` for the specific tells—do not assume or invent.

Build a short, specific batch of questions:

- Only for patterns that actually apply to this BRD
- Tied to specific sections or context
- Not leading—ask what is genuinely missing

**Scope-specific gap question filtering:**

- **Quick scope:** Generate questions only for NFR categories inside the minimal essential set. Categories marked `Deferred (Quick Scope)` do not get gap questions — there's nothing to ask about something explicitly scoped out (asking production-grade-hardening questions would defeat quick scope's "build it quickly" objective).
- **Thorough scope:** Every `Inferred` or `Not evidenced` category at production-grade rigor generates a gap question (complete coverage). Call out cross-NFR dependencies explicitly: where one category's production-grade target implies a requirement in another (e.g., a multi-region Availability SLA implies specific Disaster Recovery RTO/RPO), note that dependency in the question or evidence.
- **Standard scope:** Keep existing behavior — applicable gap questions, no deferral concept.

**Default behavior (no `--ask-gaps` flag):** Route applicable questions into the "Open Questions for Stakeholder" output section (Step 5). Do not ask the user directly; do not block on a response.

**With `--ask-gaps`:** Ask the batched questions to the user directly in the conversation, in one concise round. For each answer received:

- Derive the NFR classification concisely: Status → `Explicit (user-confirmed)`, Evidence → one-line paraphrase of the user's answer (not a verbatim transcript), Priority → re-apply the Step 3 Hard Constraint / Nice-to-Have rule to the answer
- Update that row directly in the Section 2 NFR table; remove it from Open Questions
- If an answer is ambiguous, partial, or introduces a new gap, keep (or re-add) that item in Open Questions rather than forcing a resolution
- Never invent an answer the user didn't give

### Step 5: Produce Structured Output

Generate a single `req-nfr-analysis.md` file with exactly three sections in this order:

1. **Normalized Functional Requirements** — Table: ID, Requirement, Source (all requirements from Step 1)
2. **NFR List** — Table: #, Category, Status, Evidence, Priority (all 19 rows every time, even "Not evidenced"; with `--ask-gaps`, includes `Explicit (user-confirmed)` rows resolved from user answers)
3. **Open Questions for Stakeholder** — Bulleted list, each tied to a specific NFR category row or gap pattern. With `--ask-gaps`, contains only items that remain unresolved after the user's answers (may be empty); without the flag, contains every applicable gap question as today

## Deliverable

Output a markdown file named `req-nfr-analysis.md` with the three sections above. Each section is self-contained and can be reviewed independently.

## Out of Scope

- Architecture recommendations or pattern selection
- Technology stack suggestions
- Design decisions or trade-off analysis (reserved for next phase)
- Assumption of missing information—always ask instead, except that quick scope does not raise production-grade-hardening questions (HA, scaling, DR targets, etc.) for NFR categories outside its minimal essential set; those categories are still identified and written to the output file as `Deferred (Quick Scope)`, just without an accompanying stakeholder question

## Success Criteria

- All 19 NFR categories are present in the output, even if "Not evidenced"
- Every Inferred NFR includes a clear citation of the gap pattern it comes from
- No invented thresholds or assumptions are silently included
- Functional requirements are truly functional (no NFR language mixed in)
- Priorities are grounded in BRD content or explicitly routed to stakeholder questions
- With `--ask-gaps`, every resolved NFR shows `Explicit (user-confirmed)` status with evidence traceable to the user's actual answer—never an invented value—and unresolved items remain in Open Questions
- **Quick-scope success:** Output correctly distinguishes `Deferred (Quick Scope)` from `Not evidenced`, still writes every identified NFR to the output file, and never asks production-grade-hardening questions about deferred categories
- **Thorough-scope success:** Output never uses `Deferred (Quick Scope)`, applies production-grade targets across all 19 categories, and surfaces cross-NFR dependencies where they exist
