# Architecture Decision Skill

**Decides architecture style and agentic-AI fitness from normalized requirements, produces ADRs, gated behind a mandatory confirmation checkpoint.**

A focused skill for consuming requirements analysis and NFR prioritization (from `/req-nfr-analysis`), evaluating two key architectural decisions (style: monolith/modular-monolith/microservices/event-driven/serverless; agentic-AI fitness per capability), and producing MADR-formatted Architecture Decision Records with a mandatory checkpoint before lock-in. "Not applicable" is a valid verdict when no agentic capability is evidenced.

## Overview

This skill takes a normalized requirements set (BRD + req-nfr-analysis outputs) and produces two focused ADRs: one for architecture style (deployment topology) and one for agentic-AI fitness (per explicitly automated capability). Both ADRs are presented at `pending` status — the skill does not auto-confirm; you review, adjust if needed, and explicitly confirm before the decisions are locked.

## What It Does

The skill executes exactly four sequential steps:

1. **Read the Hard Constraints** — Extract only Hard Constraint (HC) NFRs from the NFR table plus scope boundaries and success criteria from the BRD. Ignore Deferred/Not-Evidenced rows.
2. **Style ADR** — Evaluate architecture style (monolith / modular monolith / microservices / event-driven / serverless, or a named split). Checklist: independent scaling needs? Single team/deploy cadence? Explicit "avoid over-engineering" signal? Bursty/event-triggered work?
3. **Agentic-AI ADR** — Evaluate per capability that's explicitly automated/AI in the functional requirements or flagged upstream as an unsupported claim. Checklist: multi-step autonomous reasoning? Tolerant of non-determinism? Needs a human-confirmation gate? If none qualify: "Not applicable — no agentic capability in confirmed requirements," naming any gap if the BRD implied otherwise.
4. **Present at Pending** — Show both ADRs with status `pending`. Wait for explicit confirmation. Update status to `confirmed` (or revise and re-present).

Output is always `architecture-decisions.md` with two ADRs: Architecture Style and Agentic-AI Fitness.

## Key Design Principles

- **Two decisions only** — Architecture style and agentic-AI fitness per capability. No component-level patterns, stack selection, or detailed design.
- **Hard constraints drive the decision** — Only HC NFRs and explicit scope boundaries inform the choice. Inferred or deferred NFRs are noted but don't override.
- **"Not applicable" is correct** — If the BRD's title claims "AI-driven" but no actual agentic capability exists in the FRs or use cases, the verdict is "Not applicable," and the gap is named.
- **No forced verdict** — Unresolved contradictions or unsupported claims from upstream block the decision. The skill surfaces them and doesn't pick a side.
- **Checkpoint enforced** — Nothing is final until the user confirms. Status remains `pending` until explicitly updated.

## Input

A completed requirements analysis, typically:

- **BRD.md** — Domain, personas, use cases, scope boundaries, self-check findings
- **req-nfr-analysis.md** — Normalized functional requirements, NFR table (10 categories), structural findings, open questions

The analysis must identify:
- Which NFRs are Hard Constraints (HC)
- Whether any agentic/AI capabilities are claimed (in title/domain) or evidenced (in FRs/use cases)
- Any unresolved contradictions or unsupported claims

## Output: `architecture-decisions.md`

```markdown
# Architecture Decisions: [System Name]

## Architecture Style

**Decision:** Modular Monolith

**Why:**
- Single team (3 developers), weekly deploy cadence
- No independent scaling needs per NFR (no hot-spot identified)
- Performance HC (100k concurrent) solvable within one process boundary + caching
- "Avoid over-engineering" signal in scope

**Alternatives:**
- Microservices: Would add network latency, eventual consistency burden, operational complexity (3-person team cannot support 4+ services in production)
- Event-Driven: Adds learning curve, overkill for single-cadence deployments; deferred to Phase 2 if async messaging becomes critical

**Status:** Pending

---

## Agentic-AI Fitness

**Decision:** Not Applicable

**Why:**
- BRD title: "AI-driven expense reconciliation"
- Functional requirements: User uploads receipt → system validates → human auditor approves
- No multi-step autonomous reasoning, no tolerance of non-determinism
- Framing claim flagged in req-nfr-analysis: unsupported (no auto-reconciliation UC)

**Gap:**
If "AI-driven" is intended, Phase 2 should clarify: which decisions are autonomous vs. human-approved? Currently, all decision-making is human-in-the-loop.

**Status:** Pending
```

Each ADR includes:
- **Decision** — The style choice or agentic-AI verdict (including "Not Applicable")
- **Why** — Rationale tied to HC NFRs and scope
- **Alternatives** — Other considered options and why they were rejected
- **Status** — `pending` (awaiting confirmation) or `confirmed` (locked)

## How It Works

### Step 1: Read the Hard Constraints

Review the req-nfr-analysis NFR table. Extract only rows marked **HC (Hard Constraint)**. Also note:
- Scope boundaries (in-scope modules, clear out-of-scope)
- Success criteria or KPIs from the BRD
- Any unresolved contradictions or unsupported claims flagged upstream

Ignore:
- NE (Not Evidenced) rows — they don't drive architecture decisions
- NTH (Nice-to-Have) rows — lower priority
- Inferred (I) rows — unless marked HC

### Step 2: Style ADR

Evaluate the candidate architecture styles against the HC constraints and operational context:

**Monolith**
- Pros: Simple deployment, low latency (shared memory), single codebase, low operational overhead
- Cons: Single failure domain, harder to scale independent components, tech-stack is unified
- Fits when: Single team, single deploy cadence, no independent scaling hotspots, no clear domain boundaries

**Modular Monolith**
- Pros: Monolith deployment model, module/package boundaries for cohesion, clear dependency rules
- Cons: Still one failure domain, still unified tech stack, requires discipline on module boundaries
- Fits when: Single team, but clear internal module boundaries; prep for potential future split

**Microservices**
- Pros: Independent scaling, independent deployment, team autonomy per service, polyglot stack possible
- Cons: High operational complexity, network latency, eventual consistency burden, distributed tracing/debugging
- Fits when: Multiple teams, independent scaling needs per service, asynchronous communication expected, acceptance of operational complexity

**Event-Driven**
- Pros: Decoupled services, natural async processing, scales bursty workloads
- Cons: Adds eventual consistency, hard to debug, requires event store or message broker
- Fits when: Bursty or async work (e.g., batch jobs, triggers), explicit event model in domain

**Serverless**
- Pros: No infrastructure to manage, pay-per-execution, auto-scaling
- Cons: Cold starts, vendor lock-in, hard to manage state, limited runtime environments
- Fits when: Event-triggered workloads, stateless functions, acceptable cold-start latency, cost sensitivity

**Checklist for decision:**
- Are there independent scaling needs? (different services need different scaling profiles)
- Single team / single deploy cadence, or multiple teams / independent deployments?
- Explicit "avoid over-engineering" in scope, or prepare for multi-team scale?
- Bursty/event-triggered work, or steady request/response flows?

### Step 3: Agentic-AI ADR

Evaluate agentic-AI fitness **per capability** that's either:
1. Explicitly marked as automated/AI in the functional requirements (e.g., "System shall auto-reconcile expenses using ML")
2. Claimed in the title/domain but flagged as unsupported in req-nfr-analysis (e.g., title says "AI-driven" but no FRs deliver it)

**For each candidate capability, ask:**

- **Multi-step autonomous reasoning?** Does the system make a series of dependent decisions without human intervention? (E.g., risk assessment → approval → payment, all auto.)
- **Tolerant of non-determinism?** Can the system handle "good enough" outcomes, or does it need 100% accuracy?
- **Needs a human-confirmation gate?** Should a human approve the AI decision before it's acted upon?

**If none of these apply: "Not Applicable"** — no agentic capability exists, even if the BRD's title implies one. Name the gap if relevant.

**If yes:** Decide:
- **Fit** — Agentic approach is suitable
- **Partial Fit** — Agentic for some decisions, human-in-the-loop for others
- **Not Fit** — Would require too much uncertainty tolerance or lacks sufficient autonomy needs

**Example verdicts:**

- ✅ **Fit**: "Expense categorization is multi-step (extract category → validate against policy → suggest) and tolerant of ~95% accuracy. Agentic approach: LLM model fine-tuned on historical data."
- ⚠️ **Partial Fit**: "Auto-reconciliation is 70% of cases (clear matches); flagged cases require human review. Agentic: similarity matching for clear pairs; human gate for ambiguous."
- ❌ **Not Applicable**: "No agentic capability. All decisions are binary (approve/reject) based on policy rules. Framing claim 'AI-driven' is unsupported by FRs."

### Step 4: Present at Pending, Wait for Confirmation

Display both ADRs with `status: pending`. Do not lock them. Wait for user review and confirmation.

- If user says "confirmed" or similar: update both statuses to `confirmed` and finalize
- If user says "revise" or identifies an issue: revise the ADR and re-present at `pending`
- If an upstream unresolved contradiction or unsupported claim blocks the decision: surface it and ask for guidance before deciding

## When to Use

Invoke this skill when:

- You have a completed BRD and normalized requirements (req-nfr-analysis output)
- You need to settle on architecture style (deployment topology) before detailed design
- You need to evaluate whether agentic/AI capabilities are viable and how to implement them
- Stakeholders ask "what does this look like in production?" and you need a reasoned answer

**Do NOT use this skill for:**

- Tech stack selection (database, framework, language — those are Phase 3+)
- Component-level or detailed design (those are downstream)
- Test/deploy/CI-CD planning (separate concern)
- Resolving contradictions or filling BRD gaps (those are upstream in req-nfr-analysis)

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill architecture-decisions

# Install via file copy
./install.sh --skill architecture-decisions --mode copy

# Install to a specific runtime
./install.sh --skill architecture-decisions --target claude

# Force-reinstall
./install.sh --skill architecture-decisions --force

# Full reinstall via copy
./install.sh --skill architecture-decisions --force --mode copy
```

For general installation details and troubleshooting, see the [**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/architecture-decisions Decide architecture style and agentic-AI fitness

evaluate architecture for our system

/architecture-decisions We have a BRD and NFR analysis; what architecture style should we pick?

architecture decision
```

The skill reads the requirements analysis and produces `architecture-decisions.md` with both ADRs at `pending` status, waiting for your confirmation.

## Files

- **SKILL.md** — Persona directives and 4-step execution protocol
- **README.md** — This file; user-facing reference documentation

## Out of Scope

- **Tech stack, component design, patterns, data/API/security detail** — Those are Phase 3+ decisions (detailed design, implementation planning).
- **Test and deployment strategies** — Separate concern; addressed after architecture is locked.
- **Resolving upstream contradictions or filling BRD gaps** — Those belong in req-nfr-analysis. Architecture decisions assume a clean, analyzed requirements set.

## Pipeline Context

This skill is **Phase 2** of the BRD → Requirements → Architecture → PRD pipeline:

- **Phase 1 (req-nfr-analysis):** Normalize requirements, extract and prioritize NFRs, identify gaps
- **Phase 2 (this skill):** Decide architecture style and agentic-AI fitness; produce ADRs with checkpoint gate
- **Phase 3 (future):** Detailed design (tech stack, component structure, API contracts, deployment plan)

Each phase's output feeds into the next.

## Version History

**v2.0** (2026-09-02):

- Simplified from complex multi-scope evaluation (quick/standard/thorough) to straightforward 4-step process
- Frontmatter reduced (no `models`, `context_optimization`)
- Focused on two core decisions: architecture style + agentic-AI fitness per capability
- Mandatory checkpoint remains (status: pending/confirmed)
- Clearer emphasis on "Not Applicable" as a valid agentic-AI verdict
- "Not Applicable" is correct when no agentic capability is evidenced, even if claimed in title

**v1.x** (prior):
- Multi-scope (quick/standard/thorough) with detailed evaluation matrices, model tiering, context management overhead.

---

## Questions?

For details on how contradictions or unsupported claims block architecture decisions, see **SKILL.md**. For how to structure ADRs, see the Output example above. For upstream requirements questions, see the [`req-nfr-analysis` README](../req-nfr-analysis/README.md) (Phase 1).
