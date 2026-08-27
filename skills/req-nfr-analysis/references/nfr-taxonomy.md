# NFR Taxonomy (19 Categories)

This taxonomy defines the 19 non-functional requirement categories used in Phase 1 requirements analysis. Each category is distinct; requirements that blend multiple concerns should be decomposed and tagged separately.

## 1. Performance

**Definition:** How fast the system processes operations and delivers results under normal operating conditions.

**Scope:** Response times, throughput, processing speed, query execution time, transaction speed.

**Examples:**
- "Search shall return results within 500ms"
- "API shall process 1,000 requests per second"
- "File upload shall complete within 30 seconds"

**Does NOT include:** Scalability (handling load growth), Latency (network delay), Reliability (correctness over time).

---

## 2. Latency

**Definition:** Network delay, propagation time, and round-trip communication overhead.

**Scope:** End-to-end delay in distributed systems, network hop time, message queue processing time, inter-service call delays.

**Examples:**
- "Message delivery latency shall not exceed 100ms across global regions"
- "DNS lookups shall complete within 50ms"
- "Replication latency across data centers shall not exceed 2 seconds"

**Does NOT include:** Performance (processing speed), Availability (uptime).

---

## 3. Scalability

**Definition:** System's ability to handle growing load, users, or data volume by increasing resources (horizontal or vertical scaling).

**Scope:** Growth capacity, linear scaling, load handling, multi-tenancy, resource elasticity.

**Examples:**
- "System shall scale to support 100,000 concurrent users"
- "Database shall handle 10x current data volume without performance degradation"
- "Add new servers to increase capacity by 20% per server added"

**Does NOT include:** Performance (absolute speed), Availability (uptime during scale).

---

## 4. Availability

**Definition:** Percentage of time the system is accessible and operational (uptime); typically expressed as "nines" (99.9%, 99.95%, etc.).

**Scope:** Uptime SLA, scheduled maintenance windows, expected downtime.

**Examples:**
- "System shall maintain 99.95% availability (52.6 minutes downtime per year)"
- "System shall be available 24/7/365 with no scheduled maintenance windows"
- "Target 99.9% availability during business hours (weekdays 8am–6pm)"

**Does NOT include:** Reliability (correctness), Resilience (fault handling).

---

## 5. Reliability

**Definition:** Consistency, correctness, and trust that the system will perform its stated function without failures or data loss.

**Scope:** Error rates, data integrity, correctness guarantees, ACID properties, consistency models.

**Examples:**
- "System shall process transactions with zero data loss"
- "All database writes shall be durable and recoverable"
- "Error rate shall not exceed 0.01% of all requests"

**Does NOT include:** Availability (uptime), Resilience (recovery from failures).

---

## 6. Resilience / Fault Tolerance

**Definition:** System's ability to detect, recover from, and continue operation after failures; graceful degradation and self-healing.

**Scope:** Failure detection, automatic recovery, fallback mechanisms, circuit breakers, fault isolation, retry logic.

**Examples:**
- "System shall detect node failure within 5 seconds and failover to replica"
- "Loss of a single service shall not cause system-wide outage"
- "System shall retry failed requests with exponential backoff"

**Does NOT include:** Availability (uptime %), Reliability (correctness).

---

## 7. Security

**Definition:** Protection against unauthorized access, data breaches, injection attacks, and malicious modifications to the system or data.

**Scope:** Authentication, authorization, encryption, threat mitigation, vulnerability prevention, security controls, compliance with security standards (OAuth, TLS, OWASP).

**Examples:**
- "All data shall be encrypted in transit using TLS 1.3"
- "Only authenticated users shall access user data"
- "API endpoints shall implement rate limiting to prevent brute force attacks"
- "System shall validate all user input to prevent SQL injection"

**Does NOT include:** Data Privacy (PII handling), Compliance (regulatory requirements).

---

## 8. Compliance / Regulatory

**Definition:** Adherence to laws, regulations, and standards specific to the domain or jurisdiction (HIPAA, GDPR, SOC2, etc.).

**Scope:** Legal requirements, audit trails, regulatory reporting, certification requirements, policy adherence.

**Examples:**
- "System shall comply with HIPAA regulations for healthcare data handling"
- "Financial transactions must comply with PCI DSS for payment card data"
- "System shall maintain audit trails for regulatory reporting"

**Does NOT include:** Security (technical controls), Data Privacy (PII specifics).

---

## 9. Data Privacy

**Definition:** Protection and responsible handling of personally identifiable information (PII), sensitive user data, and user consent for data usage.

**Scope:** PII handling, data retention policies, user consent/opt-out, anonymization, right to deletion, data classification.

**Examples:**
- "System shall delete user data within 30 days of account termination"
- "Users shall be able to download or delete their personal data"
- "System shall anonymize logs after 90 days"
- "User consent shall be required before tracking behavior"

**Does NOT include:** Security (technical controls), Compliance (regulatory enforcement).

---

## 10. Maintainability

**Definition:** Ease of understanding, modifying, fixing, and extending the system over time.

**Scope:** Code documentation, modularity, test coverage, code style consistency, abstraction quality, debugging ease.

**Examples:**
- "Code shall maintain 80% or greater test coverage"
- "System shall follow documented architectural patterns"
- "All public APIs shall be documented"
- "Code review required for all changes"

**Does NOT include:** Usability (end-user experience), Portability (running on different platforms).

---

## 11. Usability / Accessibility

**Definition:** Ease and intuitiveness of use for end users; accessibility for users with disabilities (WCAG compliance).

**Scope:** User interface clarity, learnability, accessibility standards (screen readers, keyboard navigation, color contrast), mobile responsiveness, documentation quality.

**Examples:**
- "UI shall be compliant with WCAG 2.1 AA accessibility standards"
- "System shall be fully navigable using keyboard alone"
- "Mobile UI shall be responsive and usable on devices 320px or wider"
- "Error messages shall be clear and actionable to end users"

**Does NOT include:** Usability research or UX design decisions (reserved for design phase), Performance.

---

## 12. Interoperability

**Definition:** Ability to exchange data and integrate seamlessly with external systems, APIs, and third-party services.

**Scope:** API contracts, data format standards, protocol compatibility, integration points, plugin architecture.

**Examples:**
- "System shall expose REST API following OpenAPI 3.0 specification"
- "System shall support SSO integration via SAML 2.0"
- "Shall export data in CSV, JSON, and XML formats"

**Does NOT include:** Portability (running on different platforms), Security (authentication).

---

## 13. Portability

**Definition:** Ability to run on multiple platforms, operating systems, or runtime environments with minimal modification.

**Scope:** Cross-platform support, container support, deployment flexibility, dependency isolation.

**Examples:**
- "System shall run on Linux, macOS, and Windows"
- "Application shall run in Docker containers and Kubernetes"
- "Shall support Python 3.8, 3.9, and 3.10"

**Does NOT include:** Interoperability (external integrations), Scalability (handling growth).

---

## 14. Observability

**Definition:** Ability to understand system state, diagnose problems, and monitor health through logs, metrics, and traces; debugging and operational visibility.

**Scope:** Logging, structured logging, metrics collection, distributed tracing, alerting, dashboards, debugging tools, runtime inspection.

**Examples:**
- "System shall emit structured JSON logs with request correlation IDs"
- "All critical operations shall be traced end-to-end"
- "System shall expose Prometheus metrics for CPU, memory, and request rate"
- "Alerts shall be triggered when error rate exceeds 1%"

**Does NOT include:** Security logging (security-specific), Compliance (audit trails), Performance monitoring (performance-specific).

---

## 15. Disaster Recovery / Business Continuity

**Definition:** Procedures and capabilities to recover from catastrophic failures, data loss, or major incidents and resume operations with minimal data loss and downtime.

**Scope:** Backup strategies, recovery time objective (RTO), recovery point objective (RPO), geographically distributed redundancy, disaster recovery drills.

**Examples:**
- "System shall back up data hourly to a geographically separate data center"
- "Recovery time objective (RTO) shall not exceed 4 hours after total data center failure"
- "Recovery point objective (RPO) shall not exceed 1 hour of data loss"
- "Disaster recovery plan shall be tested quarterly"

**Does NOT include:** Availability (normal uptime %), Resilience (normal failure handling).

---

## 16. Capacity / Resource Efficiency

**Definition:** Optimal use of computational resources (CPU, memory, storage, network) to minimize cost and environmental impact while meeting performance targets.

**Scope:** Resource utilization targets, memory efficiency, storage optimization, network bandwidth usage, power efficiency, cost efficiency.

**Examples:**
- "System shall run efficiently on standard cloud instances with 2 CPU cores and 4GB RAM"
- "Storage usage shall not exceed 100GB for 1 million user records"
- "Network bandwidth usage shall not exceed 1 Mbps per concurrent user"
- "System shall reduce carbon footprint by 20% through efficient resource use"

**Does NOT include:** Performance (speed), Scalability (growth), Cost (business decision).

---

## 17. Explainability / Transparency

**Definition:** Ability to explain system decisions, especially for AI/ML-driven systems, to end users and stakeholders in a comprehensible manner matching the stated persona's knowledge level.

**Scope:** Model interpretability, decision rationale exposure, confidence scoring, feature attribution, audit trails for automated decisions, human-understandable outputs.

**Examples:**
- "AI recommendations shall include a human-readable explanation of why an item was recommended"
- "Loan denial decisions shall provide specific reasons understandable to applicants"
- "System shall expose feature importance scores for all model predictions"
- "Automated decisions shall include a link to an appeals process"

**Does NOT include:** Security (protecting decision logic), Compliance (regulatory reporting).

---

## 18. AI Safety / Autonomy Control

**Definition:** Limits on what an agent or autonomous system may do without human approval; blast-radius bounds, override/kill-switch mechanisms, escalation behavior when operating at boundaries or with high uncertainty.

**Scope:** Approval workflows, human-in-the-loop thresholds, confidence bounds, override capabilities, rollback procedures, escalation paths, guardrails.

**Examples:**
- "Agent shall not execute system commands exceeding severity level 2 without human approval"
- "Agent shall pause and escalate to human if confidence score drops below 70%"
- "All financial transactions over $10,000 require human approval before execution"
- "System shall halt all operations immediately upon receiving kill-switch signal from authorized operator"

**Does NOT include:** Explainability (understanding decisions), Security (access control).

---

## 19. Other / Uncategorized

**Definition:** NFRs that do not fit the 18 named categories; used sparingly and only with justification.

**Scope:** Domain-specific, emerging, or hybrid concerns that cross multiple standard categories.

**Guidance:** If a requirement seems to belong here, first check whether it is truly a composite of multiple categories listed above. A requirement that blends Performance and Availability, for example, should be decomposed into two separate rows in the 19-category table rather than forced into "Other."

**Examples:**
- Environmental sustainability requirements that span resource efficiency and organizational policy
- Emerging concerns not yet standardized in traditional NFR frameworks

**When to use:** Only when a requirement is genuinely uncategorizable; one-line justification required. Never as a shortcut between two close categories.

---

## Usage Notes

1. **Decompose blended concerns:** If a requirement mentions multiple NFR categories (e.g., "System shall scale to 100,000 users with 99.95% availability"), create separate rows for Scalability and Availability.

2. **Inferred vs. Explicit:** A requirement may be Inferred (implied but not explicitly stated) in one or more categories. Always cite the gap pattern that led to the inference (see `gap-patterns.md`).

3. **All 19 rows every time:** The output table must always include all 19 rows, even if a category shows "Not evidenced." This ensures completeness and makes gaps visible.

4. **Priority justification:** Each NFR must be prioritized as Hard Constraint or Nice-to-Have with reasoning grounded in the BRD or explicitly routed to stakeholder questions.
