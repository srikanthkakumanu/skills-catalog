---
name: architecture-decisions
description: Architecture decisioning skill that evaluates architecture styles (monolith, modular monolith, microservices, event-driven, serverless) and agentic-AI fitness (fit/partial-fit/not-fit) using hard constraints from normalized functional requirements and Non-Functional requirement Analysis i.e Requirements and NFR Analysis as input, surfaces 1-2 alternatives at checkpoint, and produces MADR-formatted ADRs for both decisions with documented rationale. Mandatory checkpoint before lock-in—not an auto-decision.
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
  default: "standard"
---
# Architecture Decisions

## Core Directives (Reference These)

| #           | Directive                           | Key Rule                                                                                                                                                                                   |
| :---------- | :---------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | Input-Driven Decisioning            | Every claim traces to a specific NFR row/evidence or functional requirement ID from normalized requirements and NFR analysis; never invent unstated requirements                           |
| **2** | Five-Step Execution Protocol        | Execute steps 1–5 sequentially; none skipped or merged                                                                                                                                    |
| **3** | Mandatory Checkpoint Before Lock-In | Both decisions are checkpoint-gated together; never write Status: Accepted without explicit user confirmation                                                                              |
| **4** | Strict Context Window Optimization  | Progressive reference loading; inline only style/dimension names, reference architecture-styles.md/agentic-ai-fitness.md for full criteria                                                 |
| **5** | Strict Scope Boundary Control       | Calibrate depth to scope: quick (1 alternative + informal reasoning), standard (2 alternatives + rationale table), thorough (weighted scoring matrix + cross-decision dependency analysis) |
| **6** | No Fashion-Driven Selection         | Style choice justified only by team size, deployment cadence, scaling shape, data consistency; "microservices by default" or trend rationale explicitly disallowed                         |

---

## Overview

This skill systematically evaluates two interdependent architecture decisions for a system using normalized requirements and prioritized non-functional requirements as input. It produces two Architecture Decision Records (ADRs) in MADR-inspired format, with recommended decision plus 1–2 genuine alternatives and their rejection rationale—all gated by a mandatory checkpoint before lock-in, since everything downstream depends on these choices.

**Important:** This skill does **not** select technology stacks, vendors, frameworks, or component-level design—those are reserved for downstream implementation phases.

## When to Use

Invoke this skill when:

- normalized requirements and prioritized non-functional requirements is available and ready for architecture consumption
- User asks "should this be a monolith or microservices?" or similar architecture style question
- User asks whether agentic-AI (autonomous agents / multi-step tool use) fits this domain
- User finished  normalized requirements and Non-functional requirement analysis and asks "what's next?" in the architecture pipeline
- An architecture decision needs documented rationale + alternatives considered (ADR format)

## Execution Steps (Sequential—None Skipped or Merged)

### Step 1: Ingest Requirements & NFR Input

Parse the Normalized Requirements and NFR analsysis (example:`req-nfr-analysis.md`) file:

- Extract the **Normalized Functional Requirements** table (ID, Requirement, Source)
- Extract the **NFR List** table (#, Category, Status, Evidence, Priority) — all 19 rows
- Identify Hard Constraint NFRs only (Priority = "Hard Constraint")
- Pull the NFR rows relevant to each decision:
  - **Architecture style drivers:** Scalability, Availability, Reliability/Resilience, Maintainability, Capacity/Resource Efficiency, Data Privacy, Compliance/Regulatory, Observability, Interoperability, Portability
  - **Agentic-AI fitness drivers:** AI Safety/Autonomy Control, Explainability/Transparency, Security, Compliance/Regulatory, Reliability/Resilience
- Extract org context facts (team size, deployment cadence, scaling shape, data consistency requirements). These are typically known but not formalized as NFRs. If any genuinely absent:
  - Ask the user directly in one short round rather than assuming
  - Keep the question specific and narrow (never broad "tell us about your org")
- Produce a visible **"Decision Inputs"** recap (2-3 bullet list per decision) so rationale stays auditable downstream

Output: Decision Inputs recap in conversation

### Step 2: Evaluate Architecture Style

Score the 5 candidate styles (monolith, modular monolith, microservices, event-driven, serverless) against **only** these 4 drivers: team size, deployment cadence, scaling shape, data consistency requirements.

- Never introduce trend, fashion, or "best practice by authority" as a driver
- For each style, document:
  - How it maps to the 4 drivers (favorable signals + unfavorable signals)
  - Which Hard Constraint NFRs it satisfies or stresses
- Identify the top recommendation + 1–2 genuine alternatives (never straw men)
- For each alternative not chosen, explicitly state why it lost on the 4 drivers (not a vague "considered it")
- **Scope-gated (per Directive 5):**
  - **Quick scope:** 1 alternative + informal reasoning (one paragraph per alternative)
  - **Standard scope:** 2 alternatives + rationale table (Driver | Recommended | Alternative 1 | Alternative 2)
  - **Thorough scope:** 3 styles scored in a weighted scoring matrix (driver weight × score per style); document cross-decision impacts (e.g., "serverless + agentic AI = cold-start risk for long-running autonomy")

Output: Scored styles + recommendation + alternatives analysis (presented at Step 4 checkpoint, not yet written to file)

### Step 3: Evaluate Agentic-AI Fitness

Reason over these 3 dimensions individually (never a bare yes/no verdict):

1. **Non-Determinism Tolerance**: Does the domain tolerate non-deterministic AI decisions (vs. require 100% reproducibility)? Evidence: any Reliability, Compliance, Regulatory, or AI Safety/Autonomy Control Hard Constraints that demand determinism?
2. **Autonomous Multi-Step Tool Use Need**: Does the domain need autonomous agents (vs. simple request-response or human-orchestrated steps)? Evidence: any Scalability, Availability, or Autonomy Control Hard Constraints that imply autonomous loops?
3. **Human-in-Loop Requirement**: Must humans supervise or approve AI decisions? Evidence: Compliance, Regulatory, Explainability, or Safety/Autonomy Control Hard Constraints?

Combine into verdict: **fit** (all 3 dimensions enabled), **partial-fit** (1–2 dimensions enabled with workarounds), or **not-fit** (≥1 hard blocker across any dimension).

- **Scope-gated (per Directive 5):**
  - **Quick scope:** 2–3 sentence reasoning per dimension + verdict (informal)
  - **Standard scope:** 1 paragraph per dimension + verdict with blocker citations
  - **Thorough scope:** Detailed analysis per dimension + cross-dependency with Step 2 style (e.g., "serverless prohibits long-running tool loops" for autonomous use case) + explicit verdict-combination rules applied

Output: 3-dimension reasoning + verdict (presented at Step 4 checkpoint)

### Step 4: 🔔 CHECKPOINT—Present Decisions for Confirmation

Before writing any output file, present both decisions to the user in conversation:

**Style Decision:**

- Recommended style + driver justification (2–3 sentences)
- Alternatives considered + why each lost (per scope)
- Explicitly ask: "Does this align with your architecture vision? Confirm, redirect, or ask for deeper analysis."

**Agentic-AI Fitness:**

- Verdict (fit/partial-fit/not-fit) + one-sentence blocker/enabler if applicable
- 3-dimension reasoning (per scope depth)
- Explicitly ask: "Does this verdict match your domain needs? Any concerns or corrections?"

This is a **hard gate at every scope** (quick, standard, thorough). Never skip or auto-approve.

If the user confirms both, proceed to Step 5.
If the user redirects (e.g., "we actually need 5-minute deployment cadence" or "autonomous loops are a hard requirement"), re-run Step 2 or Step 3 with the new constraint as evidence and re-present at checkpoint.
If the user requests deeper analysis, add scope or extend Step 2/3 reasoning and re-present.

### Step 5: Produce Structured Output (ADRs)

Only after checkpoint confirmation, write `architecture-decisions.md` with two ADRs in MADR-inspired format:

**Format per ADR:**

- **Title:** ADR-NNN: Architecture Style (or Agentic-AI Fitness)
- **Status:** Accepted (+ today's date)
- **Context and Problem Statement:** 1–2 sentences on the domain / system being designed
- **Decision Drivers:** 4 bullets (team size, deployment cadence, scaling shape, data consistency for style; or 3 dimensions for agentic-AI)
- **Considered Options:** Table or bullets with 2–3 options, each with brief justification for why considered; one row/bullet marked ✅ (chosen)
- **Decision Outcome:** 1 sentence stating the chosen option
- **Consequences:** Positive consequences (2–3 bullets) + negative consequences / trade-offs (2–3 bullets)

**Two ADRs in fixed order:**

1. **ADR-001: Architecture Style** — monolith / modular monolith / microservices / event-driven / serverless
2. **ADR-002: Agentic-AI Fitness** — fit / partial-fit / not-fit + dimension reasoning

No new rationale introduced at output time beyond what was checkpoint-confirmed; trace all claims back to Step 1 inputs.

## Deliverable

Output a markdown file named `architecture-decisions.md` containing the two ADRs above in MADR format, with full traceability to normalized requirements and NFR analysis Hard Constraints.

## Out of Scope

- Technology stack, vendor, or framework selection
- Detailed service decomposition or component-level design
- Implementation roadmaps or sprint planning
- Auto-approve or skip-checkpoint modes
- Any rationale disconnected from Hard Constraint NFRs or org facts (team size, cadence, scaling, consistency)

## Success Criteria

- Every claim in both ADRs cites a specific NFR row ID or functional requirement from req-nfr-analysis.md
- Checkpoint always occurs before file write; user confirmation is explicit and in-conversation
- Both alternatives in Standard/Thorough scopes show rejection reasoning (not just named)
- Agentic-AI verdict always breaks down all 3 dimensions individually (never a bare verdict)
- No fashion-driven or trend-based style justification present
- Thorough scope surfaces the style ↔ agentic-AI cross-dependency (e.g., "serverless + long-running autonomy = feasible but high cold-start risk")
