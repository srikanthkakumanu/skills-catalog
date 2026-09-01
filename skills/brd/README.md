# BRD Skill

**Produces a compact, self-checked Business Requirements Document (BRD.md) in one pass.**

A lightweight skill for extracting domain, personas, use cases (happy/negative paths + acceptance criteria), scope boundaries, and self-checks for framing claims, contradictions, and coverage gaps — with zero technical leakage (WHAT and WHO, never HOW).

## Overview

This skill takes a product concept or high-level requirement and produces a focused, verifiable `BRD.md` that serves as the single source of truth for product, engineering, and stakeholder alignment. It enforces pure functional scope (no architecture, no tech stack) and mandates a self-check before output to catch unsupported framing, contradictory flows, and orphaned scope items.

## What It Does

The skill executes exactly five sequential steps:

1. **Domain** — Define one system name and 2–4 top-level modules/capabilities.
2. **Personas** — Create a table: ID, name, role, top job-to-be-done (JTBD), top pain point. Typically 1–2 personas (more only if the concept clearly requires it).
3. **Use Cases** — One per persona-critical flow: ID, actor, happy path (≤3 steps), exceptions (1-line: trigger → behavior), acceptance criteria (Gherkin, ≤3 lines).
4. **Scope** — Boundary table: module | in-scope | out-of-scope | 1-line reason.
5. **Self-Check** (mandatory) — Three validation checks:
   - **Framing**: Does the title/domain imply a capability that no use case delivers? Flag if yes.
   - **Contradiction**: Do any two flows or rules silently conflict? Flag both, name each.
   - **Coverage**: Does every in-scope row trace to at least one use case? Flag orphans.

Output is **always** a `BRD.md` with a Self-Check Findings section; "None" is a valid result when checks pass.

## Key Design Principles

- **Functional only** — No technical leakage (no databases, API contracts, frameworks, infrastructure). Business entities and workflows only.
- **Every in-scope item verified** — No silent assertions. If an in-scope module isn't referenced by a use case, it's flagged.
- **Every capability named is claimed** — If the domain names "AI" or "automated," at least one use case must deliver it, or it's flagged.
- **No contradictions pass silently** — If two flows conflict (e.g., "must support offline" + "real-time sync"), both are flagged.
- **Lean by default** — 3-step happy paths max, 1-line exception triggers, 3-line Gherkin max per scenario. No filler.

## Input

A product concept, one-liner, or high-level requirement; can be:

- A single sentence ("Build a feedback collection system")
- A paragraph of business context
- Existing stakeholder notes or strategic goals
- An image, sketch, or rough idea

## Output: `BRD.md`

```
# Business Requirements Document: [Domain Name]

## Domain
- **Name**: [System name]
- **Modules**:
  - [Module 1 name, purpose]
  - [Module 2 name, purpose]
  - ...

## Personas

| ID     | Name | Role | Top JTBD | Top Pain |
|--------|------|------|----------|----------|
| PER-01 | Alice| Buyer | Get refunds fast | Manual reconciliation takes hours |
| PER-02 | Bob  | Auditor | Verify spend compliance | No audit trail |

## Use Cases

### UC-101: Refund Request
**Actor**: PER-01 (Alice)

**Happy Path**:
1. Alice submits receipt and amount
2. System validates against policy
3. Alice receives confirmation

**Exceptions**:
- Receipt missing → reject, prompt for upload

**Acceptance Criteria**:
```gherkin
Given Alice has a valid receipt
When she submits a refund request
Then she sees confirmation within 5 seconds
```

### UC-102: Audit Report

[Similar structure]

## Scope

| Module     | In-Scope                   | Out-of-Scope                  | Reason              |
| ---------- | -------------------------- | ----------------------------- | ------------------- |
| Submission | Receipt upload, validation | Image OCR, ML classification  | OCR phase 2         |
| Refunds    | Direct transfer, policies  | Multi-currency, payments API  | Payment partner TBD |
| Audit      | View logs, export CSV      | Role-based advanced analytics | Roadmap phase 2     |

## Self-Check Findings

| Type     | Description                                                                      | Reference                              |
| -------- | -------------------------------------------------------------------------------- | -------------------------------------- |
| Coverage | Module "Audit" has no use case — out-of-scope or missing?                       | UC-102 doesn't cover audit exports     |
| Framing  | Domain claims "automated reconciliation" but UC-101/102 are manual review flows. | Rephrase or add auto-reconciliation UC |

```

Every section except "Self-Check Findings" can be empty only if genuinely not applicable; Self-Check Findings is always present (empty → "None").

## How It Works

### The Five-Step Process

**Step 1: Domain**
- Ask: What is the system called? What are 2–4 major things it does (modules)?
- Output: One name, 2–4 bullet points. E.g., "Expense Reconciliation: Submission, Validation, Audit, Reporting"

**Step 2: Personas**
- Ask: Who are the 1–2 critical users? For each: role, one key job they need, one pain they face.
- Output: Structured table (ID, Name, Role, Top JTBD, Top Pain). 1–2 rows unless concept clearly needs more (multi-tenant, B2B/B2C mix, etc.).

**Step 3: Use Cases**
- Ask: For each persona, what are their critical flows? What's the happy path (≤3 steps)? What exceptions matter (≤1 line each)?
- Output: One UC per persona-critical flow. ID, Actor, Happy Path, Exception Paths, Gherkin acceptance criteria (Given-When-Then, ≤3 lines).
- **Lean**: 3-step max; don't add steps for system internals ("system validates" is one step, not three sub-checks).

**Step 4: Scope**
- Ask: For each module named in Domain, is it in-scope for this effort? Why or why not?
- Output: Boundary table (module | in/out | reason). Clarifies what's cut or deferred and why.

**Step 5: Self-Check (Mandatory Before Output)**
- **Framing check**: Does the title/domain name a capability (e.g., "automated," "integrated," "AI-driven") that no use case actually delivers? If yes, flag it with the implied capability and the gap.
- **Contradiction check**: Do any two flows, rules, or acceptance criteria conflict? E.g., "must support offline" but "real-time sync required." Flag both with their sources.
- **Coverage check**: Does every in-scope row in the Scope table appear in at least one use case (name, flow, or acceptance criterion)? Flag orphans (modules with no UCs covering them).
- Output: Findings table (Type | Description | Reference). Always include; empty → "None" row.

## When to Use

Invoke this skill when:
- A product concept or high-level requirement is ready to be formalized into a functional specification
- You need a shared source of truth for product, engineering, QA, and leadership
- You want to catch framing inconsistencies and scope gaps before architecture or design
- Stakeholders ask "what are we actually building?" and need a crisp, written answer

**Do NOT use this skill for:**
- Architecture, tech stack, deployment, or implementation planning
- Detailed design or UI/UX flows
- Fixing self-check findings — flag them, don't resolve silently; stakeholders decide what to do
- Resolving "nice-to-have" vs. "must-have" prioritization (that's a separate product decision)

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill brd

# Install via file copy (if symlinks don't work)
./install.sh --skill brd --mode copy

# Install to a specific runtime
./install.sh --skill brd --target claude

# Force-reinstall (overwrites existing)
./install.sh --skill brd --force

# Full reinstall via copy
./install.sh --skill brd --force --mode copy
```

For general installation details, system requirements, and troubleshooting, see the [**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/brd Create an automated expense reconciliation workflow

generate brd for employee feedback collection

/brd Define a new customer onboarding process

create business requirements for a mobile app
```

The skill reads the concept and produces `BRD.md` with domain, personas, use cases, scope boundaries, and self-check findings.

## Files

- **SKILL.md** — Persona directives and cognitive execution protocol
- **README.md** — This file; user-facing reference documentation

## Out of Scope

- **Architecture or tech stack decisions** — No "use Kubernetes," "pick PostgreSQL," or "API contract design." Pure business scope only.
- **Resolving self-check findings** — If the self-check flags a framing gap or contradiction, the skill flags it; fixing it is a stakeholder/product decision, not part of this skill's output.
- **Detailed test plans, deployment plans, or rollout strategies** — Those are downstream artifacts.
- **Prioritization (MoSCoW, phased roadmap, release planning)** — Scope boundaries and in/out decisions are part of the BRD; release sequencing is not.
