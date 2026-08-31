# Architecture Decisions

Systematically evaluate **architecture style** (monolith, modular monolith, microservices, event-driven, serverless) and **agentic-AI fitness** (fit, partial-fit, not-fit) using normalized requirements and NFR analysis, with mandatory checkpoint before lock-in. Produces MADR-formatted Architecture Decision Records (ADRs) with full rationale and alternatives considered.

---

## When to Use

Invoke this skill when:

- Your normalized and NFR requirement analysis is ready and you need architecture decisions
- You're asking "should this be a monolith or microservices?" or similar
- You need to evaluate whether agentic-AI (autonomous agents, multi-step tool use) fits your domain
- You finished requirements analysis and need to move into design phase
- You need documented architectural rationale (ADR format) for stakeholder alignment

---

## Overview

This skill consumes the output of normalized requirements and NFR analysis and evaluates two interdependent decisions:

1. **Architecture Style** — which of 5 candidates (monolith, modular monolith, microservices, event-driven, serverless) best fits your system, justified by exactly 4 drivers: team size, deployment cadence, scaling shape, and data consistency requirements. Fashion, trends, and "best practice by authority" are explicitly disallowed as justification.
2. **Agentic-AI Fitness** — whether your domain tolerates autonomous agents and multi-step tool use, evaluated across 3 independent dimensions:

   - **Non-Determinism Tolerance:** Does the domain allow variable outputs from the same input?
   - **Autonomous Multi-Step Tool Use:** Do you need long-running agent loops, or is orchestrated/request-response sufficient?
   - **Human-in-Loop Requirements:** Must humans approve before execution, or is post-decision review acceptable?

Both decisions are **checkpoint-gated** before output — you must confirm them in conversation. This is not an auto-decision; everything downstream depends on getting these right.

---

## Scope Boundaries

| Dimension                               | Quick                          | Standard                         | Thorough                                                     |
| :-------------------------------------- | :----------------------------- | :------------------------------- | :----------------------------------------------------------- |
| **Architecture Alternatives**     | 1 alternative considered       | 2 alternatives + rationale table | 3 alternatives + weighted scoring matrix                     |
| **Agentic-AI Analysis**           | 2–3 sentences per dimension   | 1 paragraph per dimension        | Detailed per-dimension + style↔AI cross-dependency analysis |
| **Org Context Questions**         | Asked if missing (direct)      | Asked if missing (direct)        | Asked if missing (direct)                                    |
| **Depth**                         | Suitable for exploratory phase | Default; production-ready        | Deep analysis for complex/high-stakes decisions              |
| **Token Budget (Reasoning Tier)** | ~800                           | ~1200                            | ~1800                                                        |

---

## Model Selection & Cost Optimization

| Phase                                       | Model Tier                 | Use                                                                       | Recommended Models        |
| :------------------------------------------ | :------------------------- | :------------------------------------------------------------------------ | :------------------------ |
| **Steps 1–3: Analysis & Evaluation** | Reasoning Tier             | Deep decision-tree analysis, multi-criteria scoring, dependency reasoning | Sonnet, Pro, GPT-4o       |
| **Step 4: Checkpoint**                | Reasoning Tier (continued) | Conversational presentation, user interaction                             | Same as above             |
| **Step 5: ADR Output**                | Lightweight Tier           | Markdown formatting, table structuring, reference citation                | Haiku, Flash, GPT-4o-mini |

---

## Context Window Management

This skill progressively loads architecture reference material on-demand:

- **SKILL.md** inlines only the 5 style names and 3 agentic-AI dimensions; full criteria referenced from `references/`
- **references/architecture-styles.md** — fully detailed per-style definition, driver signals, and failure modes
- **references/agentic-ai-fitness.md** — per-dimension evaluation, verdict combination rules, and style↔AI cross-dependencies
- Only load references as needed during Step 2–3 analysis (no upfront reading)

---

## Execution Example (Standard Scope)

### Input: `req-nfr-analysis.md`

Suppose you provide:

```
## NFR List

| # | Category | Status | Evidence | Priority |
| --- | --- | --- | --- | --- |
| 3 | Scalability | Explicit | Must handle 10x user growth in 18 months | Hard Constraint |
| 5 | Availability | Explicit | 99.5% SLA required | Hard Constraint |
| 9 | Reliability / Resilience | Explicit | RTO 1 hour, RPO 15 min | Hard Constraint |
| 14 | Data Privacy | Explicit | GDPR compliance required | Hard Constraint |
| 18 | Explainability / Transparency | Inferred | Audit trail required for all business decisions | Inferred (from Privacy) |
| 19 | AI Safety / Autonomy Control | Not evidenced | — | — |
```

And context: Team size = 12, Deployment cadence = 1x/week, Scaling shape = "heterogeneous (core API 5x, search 20x, data pipeline 50x)", Data consistency = "eventual OK, but order/payment transactions require strict ACID".

### Step 1 Output (Decision Inputs Recap)

**Architecture Style Drivers:**

- Team: 12 people (modular monolith / microservices range)
- Cadence: 1x/week (monolith–modular acceptable; microservices feasible with coordination)
- Scaling: Heterogeneous (search scales 4x faster than API; pipeline scales 10x faster; microservices beneficial)
- Consistency: Mixed (order/payment strict; recommendations eventual; federation needed)

**Agentic-AI Drivers:**

- Explainability: Inferred from Privacy — audit trails required (Dimension 3 = partial-fit, human review logs needed)
- Autonomy Control: Not stated (assume low priority unless user clarifies)

### Step 2 Output (Architecture Style Evaluation)

**Recommendation: Microservices**

| Driver                            | Microservices                                                                       | Modular Monolith                                                       | Serverless                                               |
| :-------------------------------- | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------- | :------------------------------------------------------- |
| **Team (12)**               | ✅ Supports independent ownership                                                   | ✅ Single team works                                                   | ⚠️ Ops overhead, still single team                     |
| **Cadence (1x/week)**       | ✅ Async deployment (each service deploys independently)                            | ✅ Acceptable (single coordinator)                                     | ⚠️ Overkill for weekly cadence                         |
| **Scaling (heterogeneous)** | ✅ Search service scales 4x independently; pipeline 10x; API 2x—no monolith bloat  | ⚠️ Single deployment = all scale together; search DBA contention     | ⚠️ Scaling efficiency good, but search cold-start risk |
| **Consistency (mixed)**     | ✅ Order/Payment in one service (ACID); Recommendations via eventual-consistent API | ⚠️ Single shared DB = transaction complexity for strict requirements | ✅ Cloud DB ACID native, but vendor lock-in              |

**Alternatives Considered:**

- **Modular Monolith (rejected):** Satisfies team/cadence, but heterogeneous scaling = shared DB contention when search indexes hit hot-spot; eventual-consistency reconciliation complex in single codebase; loses scaling benefit.
- **Serverless (rejected):** Strong fit for scaling/consistency (cloud ACID), but overkill for 1x/week cadence; cold-start latency risk for search queries (>5 sec response unacceptable for search UX per implied Latency constraint); team doesn't need ops-managed pricing complexity.

### Step 3 Output (Agentic-AI Fitness Evaluation)

**Dimension 1: Non-Determinism Tolerance** — GDPR + Explainability inferred constraint = must audit all decisions. Non-determinism allowed if logged. **Partial-fit**

**Dimension 2: Autonomous Multi-Step Tool Use** — Scalability (10x growth) suggests automation help, but no use case states "autonomous agent required." Could hire and train; not a driver. **Not-fit** (no stated need)

**Dimension 3: Human-in-Loop** — Explainability + audit trail = human must review decisions. "Human review logs" acceptable post-execution. **Partial-fit**

**Verdict: Not-fit** (Dimension 2 blocker; no autonomous loops needed or justified; audit trails don't require agents)

**Interpretation:** Agentic-AI not a good fit for this domain. Emphasis on explainability/audit means you need full traceability of business logic, which agents obscure. Focus on deterministic business rules + audit logs instead.

### Step 4: 🔔 CHECKPOINT

**Present to User:**

*Architecture Style: Recommended **Microservices** because:*

- *Your team (12) can own separate services (Order/Payment service, Search service, Data Pipeline service)*
- *1x/week cadence allows coordinated deployment without constant orchestration*
- *Heterogeneous scaling (search 20x vs. core 5x) justifies independent services*
- *Mixed consistency (ACID for orders, eventual for recommendations) maps to service boundaries*

*Alternatives:*

- *Modular Monolith: Simpler deployment, but shared DB contention when search hot-spots; loses scaling benefit*
- *Serverless: Great scaling efficiency, but overkill for weekly cadence; search cold-start latency risk*

**Confirm or redirect? Any concerns?**

*Agentic-AI Fitness: **Not-fit** because:*

- *Non-Determinism Tolerance (partial-fit): GDPR audit trails allow logged variance*
- *Autonomous Multi-Step Tool Use (not-fit): No use case for autonomous agents; no stated scalability pressure requiring agent automation*
- *Human-in-Loop (partial-fit): Explainability requires human review of business decisions*

*Verdict: Not-fit overall. Recommendation: Focus on deterministic business rules + comprehensive audit logging. Agents add complexity without clear benefit.*

**Does this match your domain reality? Any corrections?**

*User confirms both ✅*

### Step 5 Output: `architecture-decisions.md`

```markdown
# Architecture Decision Records

## ADR-001: Architecture Style

**Status:** Accepted (2026-08-31)

**Context and Problem Statement:**
Our system serves 12 million users with heterogeneous scaling demands (search queries 20x user growth, core API 5x, data pipeline 50x). Order/payment transactions require strict ACID guarantees; recommendation data can tolerate eventual consistency. We have 12 engineers across 2–3 teams. We deploy updates weekly.

**Decision Drivers:**
1. Team size (12) supports multiple independent service teams without excessive coordination
2. Deployment cadence (1x/week) permits each service to deploy asynchronously without blocking others
3. Scaling heterogeneity (search 4x faster than core) requires per-service scaling independent of monolith constraints
4. Data consistency (mixed strict + eventual) maps cleanly to service boundaries with federated databases

**Considered Options:**

| Option | Justification | Status |
| :--- | :--- | :--- |
| **Microservices** ✅ | Aligns with all 4 drivers: team autonomy, async deployment, per-service scaling, federated consistency model | **Chosen** |
| Modular Monolith | Satisfies team/cadence, but shared DB prevents heterogeneous scaling; search hot-spot contention; single deployment gates all teams | Rejected |
| Serverless | Excellent scaling & consistency, but cold-start latency unacceptable for search UX; overkill for 1x/week cadence | Rejected |

**Decision Outcome:**
Adopt **Microservices** architecture with service boundaries aligned to domains: Order/Payment Service (ACID, strict), Search Service (independent scaling, eventual consistency), Data Pipeline Service (independent batch processing, eventual consistency).

**Consequences:**

*Positive:*
- Each team (Order, Search, Data) owns end-to-end delivery; parallel deployment velocity
- Search scaling (20x) no longer constrained by core API (5x) growth; pure cost-efficiency
- ACID boundaries localized to Order/Payment; eventual consistency complexity relegated to cross-service integration

*Negative:*
- Service-to-service API contracts required; async coordination overhead
- Distributed tracing & debugging across 3+ services; ops complexity increases
- Data consistency between services (e.g., search index updates) requires choreography or eventual-consistency reconciliation (not instant)

---

## ADR-002: Agentic-AI Fitness

**Status:** Accepted (2026-08-31)

**Context and Problem Statement:**
Evaluating whether autonomous agents and LLM-driven multi-step tool use fit this system's business logic and regulatory constraints.

**Decision Drivers:**

1. **Non-Determinism Tolerance:** GDPR compliance + explainability requirement permit non-deterministic AI if all decisions are logged and auditable. (Partial-fit)
2. **Autonomous Multi-Step Tool Use:** No stated use case requires autonomous agent loops. Scaling pressure (10x growth) solvable via infrastructure, not agents. (Not-fit)
3. **Human-in-Loop Requirement:** Explainability & audit-trail mandates human review of all business decisions. (Partial-fit)

**Considered Options:**

| Option | Justification | Status |
| :--- | :--- | :--- |
| **No Agentic-AI** ✅ | Deterministic business rules + comprehensive audit logging satisfy compliance without agent complexity overhead | **Chosen** |
| Autonomous Agents (Low Autonomy) | Could theoretically automate exploratory recommendation ranking, but audit trail obscures agent reasoning; deterministic ranking rules clearer | Rejected |
| Human-Orchestrated Agent Workflow | Agents + per-step human approval possible but adds latency; deterministic rules + human spot-checks simpler & cheaper | Rejected |

**Decision Outcome:**
**Not-fit.** Implement the system with deterministic business logic and comprehensive audit logging. Do not introduce autonomous agents or LLM-driven decision-making at this phase.

**Consequences:**

*Positive:*
- Full determinism & auditability: every recommendation trace back to clear business rule
- Simpler compliance: no LLM hallucination risk; regulators understand deterministic logic
- Faster iteration: no agent prompt-tuning; rules versioning straightforward

*Negative:*
- Cannot leverage LLM for adaptive/contextual ranking (agents could personalize better)
- Manual rule maintenance as scaling increases; rule complexity grows with business logic
- Lost opportunity for autonomous customer-support escalation (would require agents)
```

---

## Pipeline Context

This skill is next phase of the BRD → Requirements → Architecture pipeline:

- `brd` skill (Business Requirements Document) + `req-nfr-analysis` skill (Requirements & NFR Analysis) — normalize and prioritize requirements
- **this skill:** Architecture & Design Decisions — evaluate architecture style & agentic-AI fitness, checkpoint-gated, ADR-formatted
- **future:** PRD Refinement / Specification — detail user stories, API contracts, test plans, based on Architecture and Design decisions

Each phase's output feeds the next. ADRs become the "architecture constraints" section of Next Phase PRD.

---

## 🚀 Installation & Activation

### Quick Install (All Agents)

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all agents (Antigravity, Claude Code, Codex)
./install.sh --skill architecture-decisions --target all

# Or with short flags
./install.sh -s architecture-decisions -t all
```

### Forceful Installation (Recommended for Updates)

Use `--force` to overwrite an existing installation and pick up the latest version:

```bash
./install.sh --skill architecture-decisions --target all --force --mode copy
```

#### Installation Mode Comparison

| Mode              | Command                      | Use Case                                        | Auto-Updates |
| ----------------- | ---------------------------- | ----------------------------------------------- | ------------ |
| **Copy**    | `--mode copy`              | Independent copies (recommended for production) | ❌ No        |
| **Symlink** | `--mode symlink` (default) | Link to catalog source                          | ✅ Yes       |

### Installation Flags Reference

| Flag                      | Purpose                                 | Example                                                     |
| ------------------------- | --------------------------------------- | ----------------------------------------------------------- |
| `-s, --skill <NAME>`    | Which skill to install                  | `-s architecture-decisions` or `-s all`                 |
| `-t, --target <TARGET>` | Agent(s) to install to                  | `-t all`, `-t claude`, `-t antigravity`, `-t codex` |
| `-f, --force`           | **Forcefully overwrite existing** | Forces reinstall even if already present                    |
| `-m, --mode <MODE>`     | Installation method                     | `-m copy` or `-m symlink`                               |
| `-h, --help`            | Show help message                       | `--help`                                                  |

### Verify Installation Success

```bash
# Check all agents have the skill installed
echo "=== Antigravity ===" && ls -la ~/.antigravity/skills/architecture-decisions/SKILL.md && echo "✓ Installed"
echo "=== Claude Code ===" && ls -la ~/.claude/skills/architecture-decisions/SKILL.md && echo "✓ Installed"
echo "=== Codex ===" && ls -la ~/.codex/skills/architecture-decisions/SKILL.md && echo "✓ Installed"
```

### Targeted Installation Examples

```bash
# Install only to Claude Code (copy mode)
./install.sh --skill architecture-decisions --target claude --mode copy

# Install specific skill with default settings
./install.sh -s architecture-decisions

# View installation help
./install.sh --help
```

### Safety Notes

- **`--force` flag:** Removes existing installations and replaces with latest version (safe for updates)
- **Symlink mode:** Updates in catalog automatically propagate to all agents (but breaks if catalog moves)
- **Copy mode:** Independent installations don't auto-update (safer if you modify locally)
- **Recommendation:** Use `--force --mode copy` for production environments

### Activation Triggers by Scope

Invoke the skill within your AI agent runtime with your desired scope depth:

#### 1. Quick Scope Invocation

```text
/architecture-decisions --scope quick
```

or

```text
should this be a monolith or microservices? (quick evaluation)
```

Quick scope evaluates 1 architecture alternative and provides 2–3 sentences per agentic-AI dimension. Suitable for exploratory phase with limited token budget (~800).

#### 2. Standard Scope Invocation (Default)

```text
/architecture-decisions --scope standard
```

or

```text
/architecture-decisions I finished requirements analysis. What's next for architecture?
```

or

```text
Generate architecture decision records for our system
```

Standard scope evaluates 2 architecture alternatives with rationale table and 1 paragraph per agentic-AI dimension. Production-ready with ~1200 token budget.

#### 3. Thorough Scope Invocation

```text
/architecture-decisions --scope thorough
```

or

```text
Is agentic-AI a good fit for our platform? (thorough analysis)
```

or

```text
Evaluate architecture with detailed cross-dependency analysis
```

Thorough scope evaluates 3 alternatives with weighted scoring matrix and detailed per-dimension analysis plus style↔AI cross-dependency analysis. For complex/high-stakes decisions with ~1800 token budget.

#### 4. Interactive Checkpoint Confirmation

```text
/architecture-decisions --ask-checkpoint Confirm architecture decisions
```

Explicitly re-enters checkpoint phase for user confirmation before ADR output generation. Useful when confidence is uncertain or stakeholder alignment is needed before final output.

---

## Success Criteria

Before the skill outputs `architecture-decisions.md`, the user should:

- [ ] Confirm the recommended architecture style in the checkpoint conversation
- [ ] Confirm the agentic-AI fitness verdict (including all 3-dimension reasoning)
- [ ] Have both ADRs tracing back to specific Hard Constraint NFRs from normalized requirements and NFR analysis
- [ ] See 1–2 genuine alternatives considered (not strawmen) with explicit rejection reasons
- [ ] Understand the cross-dependency between architecture style and agentic-AI feasibility (thorough scope only)

---

## Troubleshooting

**Q: "The skill is recommending microservices, but we're a 3-person startup. That feels wrong."**

A: This is a sign the org context is missing. Step 1 will ask: "Is team size really 3?" and "Do you truly need heterogeneous scaling?" If yes to both, monolith is recommended instead. The skill never auto-recommends based on fashion—only on the 4 drivers (team size, cadence, scaling, consistency).

**Q: "Agentic-AI came back as 'not-fit,' but we want to use agents anyway."**

A: The verdict is based on Hard Constraints from normalized and NFR requirements analysis. If a constraint changed or was misstated, re-run with corrected inputs. If you want to explore agentic-AI despite the verdict, that's a business decision (not a technical one). The ADR documents why it's a trade-off, not a recommendation against it.

**Q: "How do I choose between the alternatives if I'm still unsure?"**

A: Use the Consequences section of ADR-001 to weigh trade-offs. Microservices example: Does your team have ops expertise for service-to-service debugging? If not, modular monolith may be safer. Does your scaling shape truly heterogeneous, or was that an estimate? If not, monolith may save cost. The ADR surfaces these trade-offs; you make the final call based on risk tolerance and constraints not captured in normalized requirements and NFR analysis.

---

## Questions?

For details on architecture style criteria, see `references/architecture-styles.md`.

For agentic-AI dimension definitions and verdict combination rules, see `references/agentic-ai-fitness.md`.
