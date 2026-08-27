# Gap Patterns: Identifying Unstated Requirements

This reference documents common patterns that signal missing or implicit requirements in a Business Requirements Document (BRD). Use this to identify **Inferred** NFRs and to structure questions for stakeholders.

## Pattern 1: Multi-Region or Distributed Architecture Implied but Not Stated

**Indicator:** BRD mentions users in multiple geographies, global customers, or regulatory presence in multiple countries without discussing replication, failover, or distributed storage.

**Typical inferred NFRs:**
- Disaster Recovery / Business Continuity (geographically distributed backup)
- Latency (inter-region synchronization)
- Availability (failover requirements)

**Stakeholder questions to ask:**
- "Are users in multiple geographic regions? If yes, what is the acceptable data replication latency?"
- "If a data center becomes unavailable, what is the acceptable downtime?"

---

## Pattern 2: Regulatory or Compliance Domain Mentioned Without Explicit Compliance Requirements

**Indicator:** BRD is for healthcare, finance, legal, or other regulated domain but contains no explicit compliance requirements (HIPAA, GDPR, SOC2, PCI-DSS, etc.).

**Typical inferred NFRs:**
- Compliance / Regulatory (domain-specific rules)
- Data Privacy (PII handling)
- Audit trails and retention policies
- Security (encryption, access controls)

**Stakeholder questions to ask:**
- "What regulations or standards must the system comply with (HIPAA, GDPR, SOC2, etc.)?"
- "Are there data residency requirements (e.g., data must stay in EU for GDPR)?"
- "How long must audit logs be retained?"

---

## Pattern 3: External Integration or API Required but No Integration Details

**Indicator:** BRD mentions "integration with payment provider," "third-party CRM," "SSO support," or similar without specifying protocol, response time, fallback behavior, or SLA expectations.

**Typical inferred NFRs:**
- Interoperability (API contract, format)
- Resilience (handling third-party failures)
- Latency (acceptable wait times)
- Availability (dependency on third-party SLA)

**Stakeholder questions to ask:**
- "If the external service (payment provider, CRM, etc.) is unavailable, what should the system do?"
- "What is the acceptable delay for operations depending on this integration?"
- "Are there SLA or uptime expectations from the third party that affect our system design?"

---

## Pattern 4: Performance Mentioned Without Scale Context

**Indicator:** BRD states "system shall be fast" or "responsive" without defining target response times, throughput, or the load at which those targets apply.

**Typical inferred NFRs:**
- Performance (unclear target speeds)
- Scalability (unclear growth expectations)
- Latency (network vs. processing unclear)

**Stakeholder questions to ask:**
- "What is the target response time for user-facing operations (e.g., search, checkout)?"
- "How many concurrent users must the system support at launch? At year 1? At year 3?"
- "What is the acceptable throughput (transactions/second, queries/minute)?"

---

## Pattern 5: Data Volume or Growth Trajectory Never Mentioned

**Indicator:** BRD focuses on features without stating initial data volume, growth rate, or long-term storage strategy.

**Typical inferred NFRs:**
- Scalability (data growth)
- Capacity / Resource Efficiency (storage, archival)
- Disaster Recovery (backup strategy)

**Stakeholder questions to ask:**
- "How much data will the system store at launch? What is the expected growth rate (e.g., 2x per year)?"
- "How long must historical data be retained? Are there archival or purge policies?"

---

## Pattern 6: User or Operational Load Not Defined

**Indicator:** BRD describes features without defining number of users, concurrent sessions, or peak load times.

**Typical inferred NFRs:**
- Scalability (concurrent users)
- Performance (load-dependent response time)
- Capacity / Resource Efficiency (infrastructure sizing)

**Stakeholder questions to ask:**
- "How many active users do you expect at launch? What is the target in 6 months, 1 year?"
- "What is the peak concurrent user count during normal business hours?"
- "Are there predictable peak times (e.g., monthly reporting runs, year-end closing)?"

---

## Pattern 7: Failure Mode or Error Scenario Never Discussed

**Indicator:** BRD describes the happy path without addressing what happens when things go wrong (network failure, disk full, external service down, etc.).

**Typical inferred NFRs:**
- Resilience / Fault Tolerance (recovery behavior)
- Reliability (error handling)
- Disaster Recovery (catastrophic failure)

**Stakeholder questions to ask:**
- "If [external service / database / network] fails, what should the system do? Fail fast, retry, queue for later, or something else?"
- "Are there data loss scenarios that are unacceptable?"
- "How should the system behave if it encounters a resource limit (disk full, memory exhausted)?"

---

## Pattern 8: Audit, Logging, or Observability Never Mentioned

**Indicator:** BRD has no requirements around logging, monitoring, alerting, or debugging capabilities.

**Typical inferred NFRs:**
- Observability (logging, metrics, traces)
- Maintainability (debugging support)
- Compliance (audit trails, if regulated)

**Stakeholder questions to ask:**
- "What operational metrics should the system expose (response time, error rate, throughput)?"
- "What events must be logged for debugging or audit purposes?"
- "How should the team be alerted if the system encounters errors or SLA violations?"

---

## Pattern 9: AI, ML, or Autonomous System Without Guardrails or Explainability

**Indicator:** BRD describes an AI/ML agent or autonomous system making decisions without mentioning approval workflows, thresholds for human escalation, decision explanations, or override mechanisms.

**Typical inferred NFRs:**
- AI Safety / Autonomy Control (approval workflows, guardrails, kill-switches)
- Explainability / Transparency (decision rationale)
- Compliance (if automated decisions affect users)

**Stakeholder questions to ask:**
- "Can the AI/agent make decisions autonomously, or do some decisions require human approval?"
- "What is the confidence threshold below which the system should escalate to a human?"
- "Can users understand why the system made a particular decision or recommendation?"
- "How can the system be stopped or overridden in an emergency?"

---

## Pattern 10: Cross-Browser, Cross-Platform, or Device Support Not Defined

**Indicator:** BRD describes a web or mobile app without specifying supported browsers, devices, operating systems, or accessibility requirements.

**Typical inferred NFRs:**
- Portability (OS/browser support)
- Usability / Accessibility (screen readers, keyboard navigation)
- Capacity / Resource Efficiency (mobile device constraints)

**Stakeholder questions to ask:**
- "Which browsers and versions must the system support (Chrome, Firefox, Safari, Edge, IE)?"
- "Must the system work on mobile devices? If yes, which OS and screen sizes?"
- "Must the system comply with accessibility standards (WCAG, ADA)?"

---

## Pattern 11: User Personas or Accessibility Needs Not Explored

**Indicator:** BRD describes features for a generic "user" without acknowledging different personas, abilities, or usage contexts.

**Typical inferred NFRs:**
- Usability / Accessibility (context-specific needs)
- Maintainability (documentation for different skill levels)
- Interoperability (support for assistive technology)

**Stakeholder questions to ask:**
- "Who are the primary user personas? Do any have accessibility needs or constraints?"
- "Are there different user roles with different feature access or UI needs?"
- "Should the system support keyboard-only navigation or screen readers?"

---

## Pattern 12: Maintenance Windows, Updates, or Downtime Never Discussed

**Indicator:** BRD has no mention of how the system will be maintained, updated, deployed, or rolled back.

**Typical inferred NFRs:**
- Maintainability (deployment processes, testing)
- Availability (acceptable downtime)
- Resilience (rollback procedures)

**Stakeholder questions to ask:**
- "Are there scheduled maintenance windows? If yes, how often and for how long?"
- "Can the system be updated without downtime (zero-downtime deployment)?"
- "What is the rollback procedure if an update causes problems?"

---

## Pattern 13: Data Export, Migration, or Portability Never Mentioned

**Indicator:** BRD describes data storage without mentioning user data export, migration scenarios, or lock-in prevention.

**Typical inferred NFRs:**
- Portability (data portability, export formats)
- Interoperability (data migration from legacy systems)
- Data Privacy (right to data export, required by GDPR)

**Stakeholder questions to ask:**
- "Must users be able to export their data? If yes, in which formats (CSV, JSON, API)?"
- "Is there a plan to migrate data from legacy systems? What are the migration windows and data consistency requirements?"
- "Are there SaaS lock-in concerns that should be addressed?"

---

## Pattern 14: Cost, Billing, or Resource Constraints Never Defined

**Indicator:** BRD focuses on features without discussing budget, licensing, infrastructure costs, or resource limitations.

**Typical inferred NFRs:**
- Capacity / Resource Efficiency (cost optimization)
- Maintainability (build vs. buy decisions)
- Interoperability (third-party tool selection)

**Stakeholder questions to ask:**
- "Are there budget constraints or cost targets that should guide architectural decisions?"
- "Should the system optimize for low operational cost, performance, or a balance?"

---

## Pattern 15: User Privacy or Data Retention Never Addressed

**Indicator:** BRD collects or uses user data without discussing retention policies, anonymization, or user consent.

**Typical inferred NFRs:**
- Data Privacy (retention, deletion, consent)
- Compliance (regulatory obligations)
- Security (data protection)

**Stakeholder questions to ask:**
- "How long should user data be retained after account deletion or inactivity?"
- "Must users opt in or opt out of data collection or tracking?"
- "Are there regulations (GDPR, CCPA) that define minimum data handling requirements?"

---

## Pattern 16: Testing, Quality Assurance, or Release Strategy Not Defined

**Indicator:** BRD has no mention of how the system will be tested, validated, or released.

**Typical inferred NFRs:**
- Maintainability (test coverage, QA processes)
- Reliability (testing strategies for correctness)
- Observability (production monitoring)

**Stakeholder questions to ask:**
- "What level of test coverage is required (unit, integration, end-to-end)?"
- "What is the release strategy (continuous, weekly, monthly)?"
- "Are there canary deployments, feature flags, or rollback requirements?"

---

## Pattern 17: Integration with Existing Systems or Legacy Code Not Explored

**Indicator:** BRD is a new system in an existing product ecosystem without discussing dependencies, compatibility, or integration points.

**Typical inferred NFRs:**
- Interoperability (APIs, data formats, protocols)
- Maintainability (code style, architecture alignment)
- Resilience (handling legacy system failures)

**Stakeholder questions to ask:**
- "Must this system integrate with existing systems? If yes, what are the integration points and protocols?"
- "Are there architectural patterns or technology choices from existing systems that should be reused?"

---

## Pattern 18: Security or Attack Surface Not Addressed

**Indicator:** BRD focuses on functional features without discussing threat model, authentication, authorization, or attack scenarios.

**Typical inferred NFRs:**
- Security (authentication, encryption, attack prevention)
- Compliance (security controls required by regulation)

**Stakeholder questions to ask:**
- "Who are the potential attackers (external, internal, competitors)? What are their likely attack vectors?"
- "Must the system be compliant with specific security standards (ISO 27001, NIST, OWASP)?"
- "What is the data classification (public, internal, confidential, restricted)? What protection levels are required?"

---

## How to Use This Reference

1. **Review the BRD** systematically against each of the 18 patterns above.
2. **Flag which patterns apply** to your BRD.
3. **For each applicable pattern**, prepare a short, specific question for the stakeholder (see examples under each pattern).
4. **Ask only patterns that apply**—do not pose leading or hypothetical questions.
5. **Document inferred NFRs** with a reference to the specific gap pattern (e.g., "Inferred from Pattern 1: Multi-Region Architecture").

---

## Priority of Gap Patterns

Not all gaps are equally important. In Phase 1, focus on gaps that would significantly affect architecture or technology selection (Patterns 1, 2, 4, 5, 6, 7, 9, 14, 18). Defer minor clarifications to later phases if time is constrained.
