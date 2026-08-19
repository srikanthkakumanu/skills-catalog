#!/usr/bin/env python3
"""
Unit tests for validate_brd.py supporting scope levels (prototype, mvp, full).
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SAMPLE_VALID_BRD = """# Business Requirements Document: Automated Expense Reconciliation

| Document Attribute | Specification Value |
| :--- | :--- |
| **Document Version** | `1.0.0` |
| **Status** | `Approved` |
| **Scope Level** | `MVP` |
| **Author / Lead AI-PO** | Principal Requirements Engineer (`brd` skill) |
| **Business Sponsor** | Finance Operations Group |
| **Last Updated** | 2026-08-16 |
| **Standard Compliance** | BABOK v3, IEEE 29148:2018 |
| **Scope Boundary** | Pure Functional & Business Scope (Zero Technical Leakage) |

## 1. Executive Summary & Business Intent

### 1.1 Problem Statement & Market Opportunity
Manual expense auditing creates severe processing bottlenecks and delays employee reimbursements by an average of 14 business days.

### 1.2 Strategic Alignment & Business Objectives
Streamline financial review workflows, reduce audit cycle times, and enforce automated expense policy compliance.

### 1.3 Key Performance Indicators (KPIs) & Success Metrics

| Metric Identifier | Metric Name | Baseline Value | Target Milestone (MVP) | Target Milestone (Mature) | Measurement Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `KPI-001` | Reimbursement Cycle Time | 14 Days | < 48 Hours | < 2 Hours | Timestamp delta from submission to approval |
| `KPI-002` | Audit Discrepancy Rate | 18% | < 5% | < 0.5% | Disputed expense submissions / Total submissions |

## 2. Stakeholder, Persona & Actor Ecosystem

### 2.1 Persona Matrix

| Persona ID | Persona Name | Role Classification | Business JTBD | Primary Pain Points | Authority Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PER-001` | Employee Claimant | Primary External | Submit expense claims quickly with digital receipts | Slow reimbursement and unclear rejection reasons | Standard Employee |
| `PER-002` | Expense Auditor | Internal Ops | Review flagged claims and reconcile line items | High volume of repetitive manual verification | Operational Reviewer |
| `PER-003` | Finance Supervisor | Governance & Risk | Approve high-value expense exceptions and oversee budgets | Inadequate audit trail and policy visibility | Management Approver |

## 3. Functional Domain Taxonomy & Boundaries

### 3.1 Domain Decomposition
```text
Domain: Expense Lifecycle
├── L1 Capability 1: Claim Intake & Verification
│   └── L2 Module 1.1: Receipt Ingestion & Data Extraction
└── L1 Capability 2: Audit & Approval Workflow
    └── L2 Module 2.1: Policy Rule Evaluation & Approval Routing
```

### 3.2 Business In-Scope vs. Out-of-Scope Guardrails

| Capability Area | Phase 1 MVP (In-Scope) | Future Releases (Out-of-Scope) | Strategic Rationale |
| :--- | :--- | :--- | :--- |
| Receipt Upload | JPG, PNG, PDF receipts up to 25MB | Multi-currency real-time FX hedging | Maintain focus on core domestic expense flows |
| Policy Rules | Automated per-diem and spending cap limits | ML-driven fraud prediction scoring | Core deterministic business rules sufficient for MVP |

## 4. Comprehensive Business Use Case Catalog

### UC-101: Submit Digital Expense Claim
- **Primary Persona**: `PER-001` (Employee Claimant)
- **Preconditions**: Claimant has valid active employment status.
- **Postconditions**: Expense claim is stored in `SUBMITTED` state and routed for validation.

#### Nominal Business Flow
1. Claimant creates a new expense claim draft.
2. Claimant uploads receipt item and inputs category, merchant, amount, and date.
3. Claimant submits claim for policy verification.

#### Alternate & Exception Flows
- **E1: Incomplete Claim Data**: System rejects submission and prompts claimant for missing fields.

#### Acceptance Criteria (Gherkin Format)
```gherkin
Scenario: Successful expense claim submission
  Given an authenticated Employee Claimant "PER-001"
  When they submit an expense claim with valid receipt and amount under threshold
  Then the claim state transitions to "PENDING_AUDIT"
  And an acknowledgement notification is dispatched to "PER-001"
```

### UC-102: Audit Flagged Expense Claim
- **Primary Persona**: `PER-002` (Expense Auditor)
- **Supporting Persona**: `PER-003` (Finance Supervisor)
- **Preconditions**: Claim has been flagged for manual auditor review.
- **Postconditions**: Claim is approved, rejected with reason, or escalated to `PER-003`.

#### Nominal Business Flow
1. Auditor opens audit queue and selects flagged claim.
2. Auditor verifies receipt details against submitted line items.
3. Auditor approves claim for reimbursement dispatch.

#### Alternate & Exception Flows
- **E1: Policy Violation**: Auditor rejects claim with mandatory justification comments.
- **E2: High-Value Exception**: Auditor escalates claim to Finance Supervisor `PER-003`.

#### Acceptance Criteria (Gherkin Format)
```gherkin
Scenario: Auditor approves compliant claim
  Given an Expense Auditor "PER-002" reviewing a flagged claim
  When they confirm receipt items match policy rules and submit approval
  Then the claim state changes to "APPROVED"
```

## 5. MVP Scoping & Phased Rollout Matrix

### 5.1 MoSCoW Feature Allocation Table

| MoSCoW Level | Functional Capability | Target Release Milestone | Business Value Impact |
| :--- | :--- | :--- | :--- |
| **Must Have** | Digital claim creation & receipt upload (`UC-101`) | Phase 1 MVP | Eliminates paper receipts |
| **Must Have** | Policy validation & auditor approval workflow (`UC-102`) | Phase 1 MVP | Protects company expense policy |
| **Should Have**| Bulk receipt batch upload | Phase 2 | Improves high-volume traveler efficiency |
| **Could Have** | Integrated corporate travel booking sync | Phase 3 | Convenience integration |
| **Won't Have**  | Cryptocurrency corporate reimbursement | Out of Scope | Not compliant with financial policy |

### 5.2 Phase 1 MVP Kickstart Release Guardrails
- **Scope Boundary**: Restricted to single-currency claims under standard employee policies.
- **Operational Rollout**: Limited initial pilot to 500 internal employees before global organization rollout.

## 6. Business Constraints & Governance Guardrails

### 6.1 Regulatory, Privacy & Legal Constraints
- All expense data and receipt records must be archived for 7 fiscal years to comply with statutory financial auditing regulations.
- Personally Identifiable Information (PII) must be masked in compliance with data privacy standards.

### 6.2 Business Operational Constraints & SLAs
- **Standard Claim Processing SLA**: 95% of compliant claims processed within 48 business hours.
- **High-Priority Escalation SLA**: 100% of escalated exception claims resolved within 24 business hours.

### 6.3 Risk Management & Mitigation Matrix

| Risk Identifier | Risk Description | Likelihood | Impact | Business Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| `RSK-001` | Duplicate claim submission across different expense periods | Medium | High | Automated hash check and receipt timestamp duplicate detection rule |
| `RSK-002` | Delays in manager approval causing SLA breaches | Medium | Medium | Automated escalation alerts dispatched after 24 hours of inactivity |

## 7. Refinement & Validation Changelog

### 7.1 Traceability & Persona Coverage Audit
- `PER-001` (Employee Claimant) -> Mapped to `UC-101`
- `PER-002` (Expense Auditor) -> Mapped to `UC-102`
- `PER-003` (Finance Supervisor) -> Mapped to `UC-102` (E2 escalation flow)

### 7.2 Version Changelog

| Version | Release Date | Author / AI-PO | Summary of Changes |
| :--- | :--- | :--- | :--- |
| `1.0.0` | 2026-08-16 | Principal Requirements Engineer | Initial baseline of pure business requirements document for Phase 1 MVP |
"""


SAMPLE_PROTOTYPE_BRD = SAMPLE_VALID_BRD.replace("| **Scope Level** | `MVP` |", "| **Scope Level** | `Prototype` |")

SAMPLE_SIMPLE_BRD = """# Business Requirements Document: Quick Expense Tracking

| Document Attribute | Specification Value |
| :--- | :--- |
| **Document Version** | `1.0.0` |
| **Status** | `Draft` |
| **Scope Level** | `Simple` |
| **Author / Lead AI-PO** | Principal Requirements Engineer (`brd` skill) |
| **Business Sponsor** | Finance Team |
| **Last Updated** | 2026-08-20 |
| **Standard Compliance** | BABOK v3, IEEE 29148:2018 (Lightweight Mode) |
| **Scope Boundary** | Pure Functional & Business Scope (Zero Technical Leakage) |

## 1. Domain & Module Taxonomy

```text
Domain: Expense Management
├── Module 1: Claim Submission
│   └── Submodule 1.1: Receipt Upload
└── Module 2: Approval
    └── Submodule 2.1: Review & Confirm
```

## 2. Personas

| Persona ID | Persona Name | Role | Jobs-To-Be-Done | Pain Points | Authority Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PER-001` | Employee | Primary | Submit expense claims | Slow reimbursement | Standard |
| `PER-002` | Manager | Reviewer | Approve claims | Manual review effort | Management |

## 3. Use Case Catalog

### UC-101: Submit Expense Claim

| Attribute | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-101` |
| **Primary Actor** | `PER-001` (Employee) |
| **Module** | Claim Submission → Receipt Upload |

#### Workflow
1. Employee navigates to expense portal
2. Employee uploads receipt
3. System processes and stores receipt
4. System confirms receipt acceptance

#### Happy Path
1. Employee logs in with valid credentials
2. Employee selects "New Claim"
3. Employee uploads valid receipt (JPG/PNG, <25MB)
4. System extracts receipt metadata
5. Employee confirms details and submits
6. System displays confirmation message

#### Exception Paths
- **E1: Invalid File Format** — System rejects non-image files and prompts for JPG/PNG
- **E2: Oversized File** — System rejects files >25MB and displays message

#### Acceptance Criteria

```gherkin
Feature: UC-101 - Submit Expense Claim

  Scenario: Employee successfully submits claim
    Given an authenticated employee "PER-001"
    When they upload a valid receipt image
    Then the system stores the receipt
    And a confirmation message is displayed

  Scenario: Employee attempts invalid file
    Given an authenticated employee "PER-001"
    When they upload a PDF instead of JPG/PNG
    Then the system rejects the upload
    And an error message is shown
```

### UC-102: Approve Expense Claim

| Attribute | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-102` |
| **Primary Actor** | `PER-002` (Manager) |
| **Module** | Approval → Review & Confirm |

#### Workflow
1. Manager views submitted claims
2. Manager reviews claim details
3. Manager approves or rejects
4. System records decision

#### Happy Path
1. Manager logs in
2. Manager navigates to approval queue
3. Manager reviews claim amount and receipt
4. Manager clicks "Approve"
5. System updates claim status and notifies employee

#### Exception Paths
- **E1: Incomplete Details** — Manager cannot approve; system prompts for comment

#### Acceptance Criteria

```gherkin
Feature: UC-102 - Approve Expense Claim

  Scenario: Manager approves compliant claim
    Given a manager "PER-002" viewing pending claims
    When they click approve on a valid claim
    Then the claim status becomes "APPROVED"
    And the employee is notified
```

## 4. Mapping Matrix

| Domain / Module | Persona ID | Persona Name | Primary Use Case | Coverage Note |
| :--- | :--- | :--- | :--- | :--- |
| Claim Submission | `PER-001` | Employee | `UC-101` | Submission workflow |
| Approval | `PER-002` | Manager | `UC-102` | Review & approval |
"""


class TestBRDValidator(unittest.TestCase):
    def setUp(self):
        self.script_path = Path(__file__).parent.parent / "skills" / "brd" / "scripts" / "validate_brd.py"

    def test_valid_brd_passes_strict(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_VALID_BRD)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Validator failed: {result.stdout} {result.stderr}")
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "PASSED")
            self.assertEqual(data["scope"]["effective_scope"], "mvp")
        finally:
            Path(temp_path).unlink()

    def test_prototype_scope_validation(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_PROTOTYPE_BRD)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--scope", "prototype", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Validator failed: {result.stdout} {result.stderr}")
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "PASSED")
            self.assertEqual(data["scope"]["effective_scope"], "prototype")
        finally:
            Path(temp_path).unlink()

    def test_full_scope_validation(self):
        full_brd = SAMPLE_VALID_BRD.replace("| **Scope Level** | `MVP` |", "| **Scope Level** | `Full` |")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(full_brd)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--scope", "full", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Validator failed: {result.stdout} {result.stderr}")
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "PASSED")
            self.assertEqual(data["scope"]["effective_scope"], "full")
        finally:
            Path(temp_path).unlink()

    def test_missing_section_fails(self):
        invalid_brd = SAMPLE_VALID_BRD.replace("## 1. Executive Summary & Business Intent", "## Intro")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(invalid_brd)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Missing mandatory section", result.stdout)
        finally:
            Path(temp_path).unlink()

    def test_technical_leakage_detected_in_strict(self):
        leaked_brd = SAMPLE_VALID_BRD + "\n\nData is saved in PostgreSQL database via POST /api/v1/expenses"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(leaked_brd)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("technical scope leakage", result.stdout.lower())
        finally:
            Path(temp_path).unlink()

    def test_simple_scope_validation(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_SIMPLE_BRD)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--scope", "simple", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Validator failed: {result.stdout} {result.stderr}")
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "PASSED")
            self.assertEqual(data["scope"]["effective_scope"], "simple")
            self.assertEqual(data["summary"]["mandatory_sections_required"], 4)
        finally:
            Path(temp_path).unlink()

    def test_simple_scope_detected_without_flag(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_SIMPLE_BRD)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Validator failed: {result.stdout} {result.stderr}")
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "PASSED")
            self.assertEqual(data["scope"]["effective_scope"], "simple", "Scope should be detected from document metadata")
        finally:
            Path(temp_path).unlink()

    def test_simple_scope_missing_mapping_matrix(self):
        # Remove the Mapping Matrix section completely
        lines = SAMPLE_SIMPLE_BRD.split('\n')
        filtered_lines = [line for line in lines if not line.startswith("## 4. Mapping Matrix") and "Domain / Module" not in line]
        # Remove blank lines at the end
        while filtered_lines and not filtered_lines[-1].strip():
            filtered_lines.pop()
        simple_no_matrix = '\n'.join(filtered_lines)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(simple_no_matrix)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--scope", "simple", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Missing mandatory section", result.stdout)
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
