# Standard Business Requirements Document (BRD) Schema

This specification defines the mandatory structure, formatting standards, and content rules for Business Requirements Documents produced under the `brd` Agent Skill. All generated BRDs must strictly adhere to this 7-section structure and maintain pure business/functional scope in accordance with BABOK Guide v3 and IEEE 29148:2018 standards.

---

## Document Metadata Header

Every BRD markdown file must begin with the following metadata header table:

```markdown
# Business Requirements Document: [Product / Initiative Name]

| Document Attribute | Specification Value |
| :--- | :--- |
| **Document Version** | `1.0.0` (or semantic version) |
| **Status** | `Draft` \| `In Review` \| `Approved` \| `Baselined` |
| **Scope Level** | `Prototype` \| `MVP` \| `Full` |
| **Author / Lead AI-PO** | Principal Requirements Engineer (`brd` skill) |
| **Business Sponsor / Owner** | [Target Business Unit / Executive Sponsor] |
| **Last Updated** | [YYYY-MM-DD] |
| **Standard Compliance** | BABOK v3, IEEE 29148:2018 |
| **Scope Boundary** | Pure Functional & Business Scope (Zero Technical Leakage) |
```

---

## 1. Executive Summary & Business Intent

### 1.1 Problem Statement & Market Opportunity
- **Current State Deficiencies**: Concrete pain points, manual overhead, operational delays, or market gaps experienced by the business and users.
- **Root Cause Analysis**: Underlying drivers necessitating this business initiative.
- **Target State Vision**: Clear articulation of what success looks like from a purely business and user enablement perspective.

### 1.2 Strategic Alignment & Business Objectives
- Alignment with overarching corporate goals, quarterly OKRs, and market positioning.
- Target value propositions and revenue, efficiency, or satisfaction drivers.

### 1.3 Key Performance Indicators (KPIs) & Success Metrics
A structured table quantifying measurable outcomes:

| Metric Identifier | Metric Name | Baseline Value | Target Milestone (MVP) | Target Milestone (Mature) | Measurement Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `KPI-001` | [e.g., Onboarding Cycle Time] | [e.g., 45 minutes] | [e.g., < 5 minutes] | [e.g., < 90 seconds] | [e.g., Timestamp delta from start to completion] |
| `KPI-002` | [e.g., Manual Verification Rate] | [e.g., 85%] | [e.g., < 20%] | [e.g., < 2%] | [e.g., Escalation log volume / total events] |

---

## 2. Stakeholder, Persona & Actor Ecosystem

### 2.1 Persona Matrix
Every actor interacting directly or indirectly with the business capability must be documented with explicit roles, jobs-to-be-done (JTBD), and business access levels.

| Persona ID | Persona Name | Role Classification | Business JTBD (Core Jobs To Be Done) | Primary Pain Points | Authority / Business Privilege |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PER-001` | [e.g., Direct End User] | Primary External | [Core goal user wants to accomplish] | [Current blockers and friction] | [e.g., Standard Self-Service] |
| `PER-002` | [e.g., Operations Specialist] | Internal Ops | [Back-office processing & exception review] | [Fragmented data, manual reconciliations] | [e.g., Operational Review & Action] |
| `PER-003` | [e.g., Tier-2 Support Agent] | Customer Support | [Diagnose user inquiries & unblock stuck states] | [Lack of customer interaction visibility] | [e.g., Impersonation & Escalation] |
| `PER-004` | [e.g., Risk & Compliance Officer]| Governance & Risk | [Enforce regulatory rules and audit compliance] | [Incomplete audit trails, manual reporting] | [e.g., Audit Read-Only & Policy Enforcement] |
| `PER-005` | [e.g., Platform Administrator] | Internal Administration | [Manage system tenants, policies, and rosters] | [Decentralized management tools] | [e.g., Global Organizational Admin] |

### 2.2 Persona Interaction Dynamics
- Interaction flow and handoff triggers across distinct actors.
- RACI (Responsible, Accountable, Consulted, Informed) mapping across high-level business capabilities.

---

## 3. Functional Domain Taxonomy & Boundaries

### 3.1 Domain Decomposition (L1 Capabilities & L2 Business Modules)
Hierarchical decomposition of the business domain into loosely coupled, highly cohesive capability clusters:

```text
Domain: [Core Business Ecosystem]
├── L1 Capability 1: [e.g., Identity & Access Governance]
│   ├── L2 Module 1.1: [e.g., User Onboarding & Identity Verification]
│   └── L2 Module 1.2: [e.g., Organizational Role & Entitlement Management]
├── L1 Capability 2: [e.g., Transaction & Workflow Lifecycle]
│   ├── L2 Module 2.1: [e.g., Intake & Request Validation]
│   ├── L2 Module 2.2: [e.g., Automated Execution & Settlement Engine]
│   └── L2 Module 2.3: [e.g., Dispute & Exception Remediation]
└── L1 Capability 3: [e.g., Compliance & Reporting Analytics]
    ├── L3 Module 3.1: [e.g., Immutable Audit Event Capture]
    └── L3 Module 3.2: [e.g., Regulatory Disclosure Generation]
```

### 3.2 Business In-Scope vs. Out-of-Scope Guardrails

| Scope Area | In-Scope (Business Obligations) | Out-of-Scope (Strict Boundaries) | Strategic Rationale |
| :--- | :--- | :--- | :--- |
| **Functional Bounds** | [Explicit capabilities included] | [Explicit features excluded] | [Why this line is drawn for business clarity] |
| **Audience Bounds** | [Target customer segments] | [Excluded market tiers/locales] | [Market focus and risk management] |
| **Operational Bounds**| [Business processes covered] | [Processes handled by external systems] | [Avoid overlapping operational ownership] |

---

## 4. Comprehensive Business Use Case Catalog

Every use case must follow a strict, standardized specification template.

### Specification Template for Use Cases:

```markdown
### UC-[XXX]: [Descriptive Action-Oriented Title]

| Attribute | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-[XXX]` (e.g., `UC-101`) |
| **L1 / L2 Domain** | [L1 Capability Name] -> [L2 Module Name] |
| **Primary Actor** | `PER-[XXX]` ([Persona Name]) |
| **Secondary Actors** | `PER-[YYY]`, `PER-[ZZZ]` |
| **Business Priority** | `Must Have` \| `Should Have` \| `Could Have` \| `Won't Have` |
| **Trigger** | [Business event or actor action initiating the workflow] |
| **Pre-Conditions** | 1. [Condition 1 that must hold true before initiation]<br>2. [Condition 2] |
| **Post-Conditions** | 1. [Guaranteed business outcome upon successful completion]<br>2. [Updated state of business entities] |

#### A. Nominal Business Flow (Happy Path)
1. **Initiation**: The [Primary Actor] navigates to [Business Workflow Entrypoint] and provides [Required Business Information].
2. **Validation**: The system validates [Business Rule 1] and verifies [Pre-requisite Entitlement].
3. **Execution**: The system performs [Core Business Transformation] and records [Business Transaction Record].
4. **Notification & Confirmation**: The system confirms completion to the [Primary Actor] and dispatches [Business Notice] to [Secondary Actors].

#### B. Alternate & Exception Flows
- **E1: [Exception Condition Name, e.g., Incomplete Verification Information]**
  - *Trigger*: User submits invalid or incomplete verification documents.
  - *Business Behavior*: The system halts progression, flags missing mandatory fields, and preserves draft state for 72 hours.
- **E2: [Exception Condition Name, e.g., Elevated Risk Flag Triggered]**
  - *Trigger*: Transaction score exceeds standard risk tolerance threshold.
  - *Business Behavior*: The system places transaction into pending review, transitions state to `Under Manual Review`, and alerts `PER-004` (Risk Officer).

#### C. Formal Given-When-Then Acceptance Criteria

```gherkin
Feature: UC-[XXX] - [Descriptive Title]

  Scenario: Nominal execution of [Business Goal]
    Given [User has valid credentials and account is in active standing]
    And [All pre-requisite business inputs meet threshold criteria]
    When [User submits the transaction request]
    Then [The system transitions transaction status to "Completed"]
    And [An immutable audit record is logged with actor identifier and timestamp]
    And [A confirmation notification is delivered to the user's primary channel]

  Scenario: Handling exception when [Business Rule Violation occurs]
    Given [User initiates the workflow with out-of-bounds parameters]
    When [Validation is evaluated against corporate policy rules]
    Then [The system rejects the transaction with human-readable error rationale]
    And [The state remains unchanged with zero persistent side-effects]
```
```

---

## 5. MVP Scoping & Phased Rollout Matrix

### 5.1 MoSCoW Feature Allocation Table

| Requirement ID | Capability Description | Persona Beneficiary | MoSCoW Tier | Target Milestone | Business Value Score (1-10) | Complexity / Risk (Low/Med/High) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `REQ-101` | [Core capability description] | `PER-001` | **Must Have** | Phase 1 (MVP) | 10 | Low |
| `REQ-102` | [Critical operational workflow] | `PER-002` | **Must Have** | Phase 1 (MVP) | 9 | Medium |
| `REQ-103` | [Advanced analytics dashboard] | `PER-005` | **Should Have** | Phase 2 (Enhancement) | 7 | Medium |
| `REQ-104` | [Automated proactive suggestions] | `PER-001` | **Could Have** | Phase 3 (Future) | 5 | High |
| `REQ-105` | [Legacy paper intake ingestion] | `PER-002` | **Won't Have** | Out of Scope | 2 | High |

### 5.2 Phase 1 MVP Kickstart Release Guardrails
- **MVP Go/No-Go Acceptance Criteria**: Non-negotiable business outcomes required for launch readiness.
- **Operational Readiness Checklist**: Staff training, customer support playbooks, compliance approvals.

---

## 6. Business Constraints & Governance Guardrails

### 6.1 Regulatory, Privacy & Legal Constraints
- Applicable compliance standards (e.g., GDPR, CCPA, SOC2 Type II, HIPAA, PCI-DSS, ISO 27001).
- Data residency, retention, right-to-be-forgotten, and consent requirements.

### 6.2 Business Operational Constraints
- Maximum acceptable business downtime during operational maintenance windows.
- Escalation timeframes and Service Level Agreements (SLAs) for human reviews and support resolution.

### 6.3 Risk Management & Mitigation Matrix

| Risk ID | Identified Business Risk | Severity / Impact | Probability | Mitigation Strategy | Contingency Plan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RSK-001` | [e.g., Regulatory policy shift prior to launch] | High | Medium | [Continuous alignment with compliance team] | [Modular policy engine rules] |
| `RSK-002` | [e.g., User adoption friction in back-office] | Medium | High | [Early co-design sessions & pilot testing] | [Fallback manual override process] |

---

## 7. Refinement & Validation Changelog

### 7.1 Traceability & Persona Coverage Validation
- **Persona Completeness Check**: Verified that 100% of defined personas in Section 2 are mapped to at least one active use case in Section 4.
- **Acceptance Criteria Verification**: Verified that all use cases contain complete, non-empty Given-When-Then criteria.
- **Pure Functional Scope Verification**: Verified zero leakage of technical infrastructure (databases, API URLs, framework names, programming languages).

### 7.2 Version Changelog

| Revision | Date | Author / AI Agent | Summary of Changes / Evolution | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| `0.1.0` | [YYYY-MM-DD] | AI-PO (`brd` skill) | Initial draft elicited from raw business concept via CoT/ToT | Working Group |
| `1.0.0` | [YYYY-MM-DD] | AI-PO (`brd` skill) | Baselined pure functional requirements following ReAct critique | Product Committee |
