# Agentic-AI Fitness: Evaluation Reference

This reference evaluates whether a domain is suitable for agentic-AI (autonomous agents, multi-step tool use, LLM-driven decisions) based on three independent dimensions. Each verdict combines findings from all three dimensions using explicit rules.

---

## Dimension 1: Non-Determinism Tolerance

**Question:** Does the domain tolerate non-deterministic (variable output) AI decisions, or does it require 100% reproducible, auditable behavior?

### Fit (Non-Determinism OK)

- **Examples:** Recommendation systems, creative content generation, exploratory data analysis, customer support chatbots (where minor variation is fine)
- **Evidence markers:**
  - No Reliability / Resilience Hard Constraint requiring exact same output every time
  - No Compliance / Regulatory Hard Constraint forbidding variance (e.g., "must produce identical report on re-run")
  - No AI Safety / Autonomy Control Hard Constraint requiring deterministic execution
  - Domain expects variation (e.g., "different recommendations for same user" is acceptable)

### Partial-Fit (Non-Determinism Accepted with Guardrails)

- **Examples:** Financial fraud detection, medical decision support (with human review), content moderation (with escalation paths)
- **Evidence markers:**
  - Compliance / Regulatory Hard Constraint exists but allows variation if logged/audited
  - Reliability Hard Constraint requires *repeatability* (same input → can re-run and validate) but not *determinism* (exact output)
  - AI Safety / Autonomy Control allows non-determinism if human-in-loop confirmed (dimension 3)

### Not-Fit (Determinism Required)

- **Examples:** Legal document generation for regulatory filing, core financial transaction processing, cryptographic key derivation
- **Evidence markers:**
  - Strict Compliance / Regulatory Hard Constraint: "every output must match approved template exactly" or "variance violates audit trail"
  - Reliability / Resilience Hard Constraint: "re-running same input must yield identical bytes or transaction fails"
  - AI Safety / Autonomy Control Hard Constraint: "no LLM-generated variance allowed"

---

## Dimension 2: Autonomous Multi-Step Tool Use Need

**Question:** Does the domain require long-running autonomous agents (agents execute a sequence of tools without human orchestration per step), or is request-response or human-orchestrated workflows sufficient?

### Fit (Autonomous Loops Enabled)

- **Examples:** Data pipeline orchestration, autonomous customer service (e.g., "book meeting, check calendar, suggest times, send invite"), complex search/research (multi-query, cross-reference, synthesis)
- **Evidence markers:**
  - Scalability Hard Constraint: "handle 10x increase in requests without proportional staff increase" (autonomous loops required)
  - Availability Hard Constraint: "24/7 service, including off-hours" (implies no human orchestration possible)
  - Autonomy Control Hard Constraint states: "autonomous loops required" or "multi-step execution without human-per-step approval"
  - Domain expects agent to chain multiple calls without explicit user instruction each time (e.g., "fix this bug" → agent runs tests, reads logs, writes code, re-runs tests, submits PR)

### Partial-Fit (Hybrid Orchestration)

- **Examples:** Data enrichment (human provides seed, agent queries 3–5 APIs and merges), report generation (human selects scope, agent fetches data + writes), incident response (human classifies severity, agent runs checks + suggests fixes)
- **Evidence markers:**
  - Scalability Hard Constraint exists but human review step acceptable (e.g., "handle 5x without staff; we'll do spot-checks")
  - Availability Hard Constraint allows batching / delayed response (human orchestrates hourly, not per-request)
  - AI Safety / Autonomy Control Hard Constraint: "agent can sequence tools but must ask before committing" (human-in-loop per major step, not per tool)

### Not-Fit (Human-Orchestrated Only)

- **Examples:** Legal review, medical diagnosis, high-stakes financial decisions, security incident response
- **Evidence markers:**
  - Compliance / Regulatory Hard Constraint: "every decision must include human sign-off"
  - AI Safety / Autonomy Control Hard Constraint: "no autonomous loops; human must approve before any action"
  - Reliability Hard Constraint: "failure = business loss; requires human judgment per decision"
  - Domain inherently requires sequential human approval (e.g., "user must decide next step based on results")

---

## Dimension 3: Human-in-Loop Requirement

**Question:** Are human approvals/oversight required in the decision/execution flow, and at what frequency?

### Fit (No Human-in-Loop Required)

- **Examples:** Batch data processing, content recommendations, search ranking, log aggregation/alerting
- **Evidence markers:**
  - No Compliance / Regulatory Hard Constraint requiring human approval
  - No Safety / Autonomy Control Hard Constraint requiring human oversight
  - No Explainability Hard Constraint requiring human-readable decision trail
  - Domain permits autonomous operation (e.g., "system can decide and act without approval")

### Partial-Fit (Human Review Acceptable Post-Decision)

- **Examples:** Customer service escalation (agent handles, human reviews transcript), report generation (auto-generated, human spot-checks), code review automation (bot suggests, human approves)
- **Evidence markers:**
  - Compliance / Regulatory Hard Constraint: "human review OK as audit / after-action validation" (not gate-before-execution)
  - Explainability Hard Constraint: "must provide reasoning; human validates it matches domain logic"
  - Safety / Autonomy Control: "agent can propose; human reviews and confirms" (e.g., before database write)

### Not-Fit (Human Approval Required Before Execution)

- **Examples:** Financial transactions > threshold, medical procedure orders, legal document submission, infrastructure changes
- **Evidence markers:**
  - Compliance / Regulatory Hard Constraint: "human must approve before action" or "audit trail must show human decision"
  - Safety / Autonomy Control Hard Constraint: "agent proposes, human decides" (every decision gated by human)
  - Reliability Hard Constraint: "human review required to prevent data loss or business impact"

---

## Verdict Combination Rules

The three dimensions are **independent** but must be combined to reach a final verdict: **fit**, **partial-fit**, or **not-fit**.

### Rule 1: Hard Blocker

**If any single Hard Constraint violates one or more dimensions, verdict = not-fit.**

Examples:

- Compliance requires human approval (Dimension 3 = not-fit) + non-determinism forbidden (Dimension 1 = not-fit) = **not-fit** overall
- Safety/Autonomy forbids autonomous loops (Dimension 2 = not-fit) = **not-fit** overall
- Regulatory requires determinism (Dimension 1 = not-fit) = **not-fit** overall

### Rule 2: All Three Enabled

**If all three dimensions are fit = verdict is fit.**

Examples:

- Dimension 1: non-determinism OK (no strict compliance)
- Dimension 2: autonomous loops required (scaling constraint)
- Dimension 3: no human-in-loop needed (no safety constraint)
- **Verdict = fit**

### Rule 3: Two Enabled, One Partial

**If two dimensions are fit + one is partial-fit = verdict is partial-fit.**

Examples:

- Dimension 1: non-determinism OK
- Dimension 2: autonomous loops required
- Dimension 3: human review post-decision acceptable (partial-fit)
- **Verdict = partial-fit** (human-review overhead is manageable)

### Rule 4: One or More Partial, One or More Not-Fit

**If any dimension is not-fit, verdict = not-fit. Partial-fit only offsets other partial-fits, not not-fits.**

Examples:

- Dimension 1: determinism required (not-fit)
- Dimension 2: autonomous loops partial-fit (could hybrid-orchestrate)
- Dimension 3: no human-in-loop (fit)
- **Verdict = not-fit** (Dimension 1 is blocker)
- Dimension 1: non-determinism partial-fit (allowed with audit)
- Dimension 2: autonomous loops partial-fit (batched orchestration OK)
- Dimension 3: human review acceptable (partial-fit)
- **Verdict = partial-fit** (all partial-fit, no not-fits)

---

## Architecture Style Cross-Dependency (Thorough Scope Only)

If the recommended architecture style from Architecture Syles Step 2 constrains agentic-AI feasibility, note it explicitly in the Consequences section of ADR-002.

### Serverless ↔ Autonomous Tool Use

**Constraint:** Serverless function cold-starts (0.5–5 seconds per invocation) create latency for multi-step agent loops. If an agent must chain 10 tool calls (10 invocations × avg 2-second start = 20s overhead), wall-clock time becomes prohibitive for real-time interactions.

**Implication:** If Dimension 2 = fit and serverless is recommended → partial-fit or not-fit agentic-AI; add mitigation (provisioned concurrency, lightweight runtimes).

### Monolith / Modular Monolith ↔ Autonomous Tool Use

**Enabler:** Single deployable unit + shared database = synchronous tool calls zero-latency; ideal for long-running agent loops.

**Implication:** If Dimension 2 = fit and monolith/modular-monolith recommended → fit agentic-AI (no architectural friction).

### Microservices ↔ Autonomous Tool Use

**Enabler/Constraint:** Independent services enable parallel tool execution (agent calls Search service + DB service + Email service concurrently), but network latency adds per-call. For short loops (2–3 tools) acceptable; for long loops (20+ tools) cumulative latency grows.

**Implication:** If Dimension 2 = fit and microservices recommended → partial-fit agentic-AI (network latency acceptable if loop count moderate).

### Event-Driven ↔ Autonomous Tool Use

**Constraint:** Event-driven architecture introduces asynchrony (agent publishes event, waits for subscriber to respond). True autonomous loops difficult; more suited to choreography/sagas (human or orchestrator drives sequence).

**Implication:** If Dimension 2 = fit and event-driven recommended → partial-fit agentic-AI (hybrid orchestration required; agent can't truly loop autonomously).

---

## Example Application

Given a system with:

- **Hard Constraints:**
  - Compliance (Regulatory): "human review must be logged before any external API call" (Dimension 3 = partial-fit)
  - Scalability: "handle 10x growth without proportional headcount" (Dimension 2 = fit, autonomous required)
  - Reliability (Resilience): "failures must be logged with full context; any variation must be audit-traced" (Dimension 1 = partial-fit)

**Verdict application:**

- Dimension 1: Partial-fit (non-determinism allowed if logged)
- Dimension 2: Fit (autonomous loops required for scalability)
- Dimension 3: Partial-fit (human review post-decision acceptable)
- **Rule 3 applies:** 2 fit/partial + 0 not-fit = **partial-fit**

**Interpretation:** Agentic-AI feasible with guardrails: autonomous loops allowed, but every step must log reasoning for audit; human spot-checks post-execution to validate agent judgment. Hybrid orchestration (agent proposes sequence, human batches approvals hourly) acceptable.
