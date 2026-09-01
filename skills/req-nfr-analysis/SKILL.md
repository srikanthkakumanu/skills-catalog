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

## Core Directives

1. **Pure Requirements Analysis** — No architecture or tech recommendations
2. **Five-Step Sequential Execution** — Steps 1–5 in order; none skipped or merged
3. **Complete NFR Coverage** — All 19 categories in every output, even "Not evidenced"
4. **Progressive Reference Loading** — Inline category names; reference taxonomy/patterns for details
5. **Scope Boundary Control** — Calibrate depth: quick (minimal essential set, deferred categories), standard (all 19 + applicable questions), thorough (production-grade rigor, cross-NFR dependencies)
6. **Gap Resolution** — `--ask-gaps` asks stakeholders and resolves into NFR table; omit for static questions

---

## Overview

Analyzes completed BRDs to extract, normalize, and prioritize functional and non-functional requirements. Serves as the bridge between requirements definition and architecture/design phases. **Does not recommend architecture, patterns, or tech stacks.**

## When to Use

- BRD provided and needs normalization or NFR extraction
- User asks for "requirement analysis" or declares BRD "done"
- Incomplete BRD needs structured gap identification

## Execution Steps (Sequential—None Skipped or Merged)

### Step 1: Extract Functional Requirements

Walk systematically through use cases, acceptance criteria, and requirement rows.

**Rules:**
- One normalized imperative statement per requirement
- Format: "System shall X" with source reference (e.g., UC-3.2, AC-5.1)
- Functional only—separate from NFR language (split "persist data with 99.95% durability" into functional requirement + NFR tag)

**Output:** Table: ID, Requirement, Source

### Step 2: Tag Every NFR Across 19 Categories

For every requirement, determine NFR classification across 18 named categories (see `references/nfr-taxonomy.md`) plus "Other/Uncategorized."

**Tags:**
- **Explicit** — Stated clearly in BRD
- **Inferred** — Implied but not stated (cite gap pattern from `references/gap-patterns.md`)
- **Not evidenced** — Absent
- **Deferred (Quick Scope)** — Identified but outside minimal essential set (quick scope only)

**Rules:**
- Never invent thresholds; mark "99.95% availability" as Inferred if unstated
- Use "Other/Uncategorized" only for genuinely uncategorizable requirements (not a shortcut between close categories); one-line justification required
- **Evidence field is a short phrase, not a sentence** — cap at ~12–15 words / one clause (e.g., `"UC-2: multi-region implied — deferred"`, not a full sentence). Cite the source tersely; don't restate reasoning in prose.
- **Quick scope:** Mark production-grade-hardening categories (HA, scaling, DR) outside minimal essential set as `Deferred (Quick Scope)` with evidence
- **Thorough scope:** All 19 resolve to Explicit/Inferred/Not evidenced; never defer

**Output:** Table: #, Category, Status, Evidence, Priority — always 19 rows

### Step 3: Prioritize Each NFR

Classify all 19 categories as **Hard Constraint** or **Nice-to-Have.**

**Definitions:**
- **Hard Constraint** — System doesn't work, fails a KPI, or violates compliance without it; includes load-bearing Inferred NFRs
- **Nice-to-Have** — Improves experience but system works without it

**Rules:**
- Spell out reasoning for each priority decision
- If priority is unclear, route to Open Questions instead of guessing
- **Quick scope:** `Deferred (Quick Scope)` rows get Priority `—`. Only prioritize minimal essential set.
- **Thorough scope:** Disaster Recovery, Compliance, Security are near-always Hard Constraint at production rigor

### Step 4: Ask for Real Gaps

Identify patterns in the BRD suggesting missing requirements. Consult `references/gap-patterns.md` (18 patterns) and build specific gap questions.

**Rules:**
- Only questions for patterns that actually apply
- Tied to specific BRD sections
- Not leading; ask what's genuinely missing

**Scope-specific filtering:**
- **Quick scope:** Generate questions only for minimal essential set. Skip `Deferred (Quick Scope)` categories (don't ask production-grade questions about explicitly deferred items).
- **Thorough scope:** Every `Inferred` or `Not evidenced` category gets a question (complete coverage). Call out cross-NFR dependencies (e.g., multi-region Availability implies specific Disaster Recovery RTO/RPO).
- **Standard scope:** Applicable gap questions; no deferral concept.

**Default (no `--ask-gaps`):** Route questions to "Open Questions for Stakeholder" section (Step 5). Do not ask user directly.

**With `--ask-gaps`:** Ask batched questions in one concise round. For each answer:
- Status → `Explicit (user-confirmed)`
- Evidence → one-line paraphrase (not verbatim)
- Priority → re-apply Step 3 rule
- Update Step 2 NFR table; remove from Open Questions
- If answer is ambiguous/partial, keep in Open Questions rather than forcing resolution

### Step 5: Produce Structured Output

Generate single file: `req-nfr-analysis.md` with three sections in order:

1. **Normalized Functional Requirements** — Table: ID, Requirement, Source
2. **NFR List** — Table: #, Category, Status, Evidence, Priority (always 19 rows; Evidence kept to a short phrase, not a full sentence)
3. **Open Questions for Stakeholder** — Bulleted list tied to NFR rows or gap patterns

With `--ask-gaps`: Section 2 includes `Explicit (user-confirmed)` rows; Section 3 contains only unresolved items (may be empty).

## Deliverable

Single markdown file: `req-nfr-analysis.md` with three self-contained sections (see Step 5).

## Out of Scope

- Architecture recommendations, patterns, or technology stack suggestions
- Design decisions or trade-off analysis (Phase 2+)
- Inventing missing information (always ask stakeholders; except quick scope suppresses production-grade questions for deferred categories—they're still identified and written to output as `Deferred (Quick Scope)`, just without a stakeholder question)

## Success Criteria

- ✅ All 19 NFR categories present in output (even "Not evidenced")
- ✅ Every Inferred NFR cites gap pattern from `gap-patterns.md`
- ✅ No invented thresholds or silent assumptions
- ✅ Functional requirements are functional (no NFR language mixed in)
- ✅ Priorities grounded in BRD or routed to stakeholder questions
- ✅ Evidence citations are short phrases (~12–15 words), not full sentences
- ✅ With `--ask-gaps`: Resolved NFRs show `Explicit (user-confirmed)` with evidence traceable to user answer
- ✅ Quick scope: `Deferred (Quick Scope)` distinct from `Not evidenced`; all identified NFRs written to output; no production-grade questions for deferred categories
- ✅ Thorough scope: Never uses `Deferred (Quick Scope)`; production-grade targets across all 19; cross-NFR dependencies surfaced
