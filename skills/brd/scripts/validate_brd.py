#!/usr/bin/env python3
"""
validate_brd.py - Production-Grade Business Requirements Document (BRD) Validator
Compliant with BABOK Guide v3 and IEEE 29148:2018 Standards.

Supports Scope Boundaries:
- prototype: Rapid concept feasibility & happy path validation
- mvp: Production-ready Day-1 viable scope (Default)
- full: Comprehensive enterprise multi-phase specification

Verifies:
1. Presence of all 7 mandatory BRD sections.
2. Zero technical scope leakage (detects SQL, REST endpoints, cloud infra, code constructs).
3. Persona-to-UseCase traceability (identifies orphaned personas).
4. Formal Given-When-Then acceptance criteria in use cases.
5. Adherence to selected scope boundaries (prototype, mvp, full).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

# ANSI color escape sequences
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

MANDATORY_SECTIONS = [
    (1, r"1\.\s*Executive\s+Summary\s+&\s+Business\s+Intent", "1. Executive Summary & Business Intent"),
    (2, r"2\.\s*Stakeholder,\s*Persona\s+&\s+Actor\s+Ecosystem", "2. Stakeholder, Persona & Actor Ecosystem"),
    (3, r"3\.\s*Functional\s+Domain\s+Taxonomy\s+&\s+Boundaries", "3. Functional Domain Taxonomy & Boundaries"),
    (4, r"4\.\s*Comprehensive\s+Business\s+Use\s+Case\s+Catalog", "4. Comprehensive Business Use Case Catalog"),
    (5, r"5\.\s*MVP\s+Scoping\s+&\s+Phased\s+Rollout\s+Matrix", "5. MVP Scoping & Phased Rollout Matrix"),
    (6, r"6\.\s*Business\s+Constraints\s+&\s+Governance\s+Guardrails", "6. Business Constraints & Governance Guardrails"),
    (7, r"7\.\s*Refinement\s+&\s+Validation\s+Changelog", "7. Refinement & Validation Changelog"),
]

MANDATORY_SECTIONS_SIMPLE = [
    (1, r"1\.\s*Domain\s+&\s+Module\s+Taxonomy", "1. Domain & Module Taxonomy"),
    (2, r"2\.\s*Personas", "2. Personas"),
    (3, r"3\.\s*Use\s+Case\s+Catalog", "3. Use Case Catalog"),
    (4, r"4\.\s*Mapping\s+Matrix", "4. Mapping Matrix"),
]

# Patterns representing technical implementation details that violate pure functional scope
TECHNICAL_LEAKAGE_PATTERNS = [
    (r"\b(SELECT\s+[\w\*,\s]+\s+FROM|INSERT\s+INTO\s+\w+|UPDATE\s+\w+\s+SET|DELETE\s+FROM\s+\w+|FOREIGN\s+KEY|PRIMARY\s+KEY)\b", "SQL Query / Schema DDL", "Database operations violate functional neutrality"),
    (r"\b(PostgreSQL|MongoDB|MySQL|DynamoDB|Redis\s+cache|Oracle\s+DB|Elasticsearch|Cassandra|Prisma|TypeORM|Hibernate)\b", "Database / Storage Technology", "Specific storage engines are technical implementation choices"),
    (r"\b(GET|POST|PUT|DELETE|PATCH)\s+/[a-zA-Z0-9_\-\./{}]+\b", "HTTP REST Endpoint Route", "Specific API routes and HTTP verbs belong in Technical Architecture"),
    (r"\b(JSON\s+payload|HTTP\s+(?:status\s+)?(?:200|201|400|401|403|404|500)|GraphQL\s+(?:mutation|query)|WebSocket\s+endpoint)\b", "API / Protocol Low-Level Construct", "Protocol-level exchange details should be abstract business messages"),
    (r"\b(Kubernetes|k8s|Docker\s+container|AWS\s+Lambda|Amazon\s+S3|EC2|Cloud\s+Run|Terraform|Helm\s+chart|Kafka\s+broker|RabbitMQ)\b", "Cloud / Container Infrastructure", "Infrastructure topology is out of scope for pure business requirements"),
    (r"\b(React\s+component|Redux\s+store|Vuex|Angular\s+service|Node\.js|FastAPI|Spring\s+Boot|Django\s+view|TypeScript\s+interface|async\s+def\s+\w+|public\s+class\s+\w+)\b", "Software Framework / Code Artifact", "Programming frameworks and code constructs leak implementation details"),
]

PERSONA_DECLARATION_PATTERN = re.compile(r"`?(PER-[A-Za-z0-9_-]+)`?", re.IGNORECASE)
USE_CASE_HEADER_PATTERN = re.compile(r"###\s+(UC-[A-Za-z0-9_-]+)[:\s]+(.+)", re.IGNORECASE)
GHERKIN_SCENARIO_PATTERN = re.compile(r"\bScenario:\s*(.+)", re.IGNORECASE)
SCOPE_HEADER_PATTERN = re.compile(r"\|\s*\*{0,2}Scope\s+Level\*{0,2}\s*\|\s*`?([A-Za-z0-9_-]+)`?", re.IGNORECASE)


class BRDValidator:
    def __init__(self, file_path: Path, strict: bool = False, scope: Optional[str] = None):
        self.file_path = file_path
        self.strict = strict
        self.requested_scope = scope.lower() if scope else None
        self.detected_scope: Optional[str] = None
        self.effective_scope: str = "mvp"
        self.raw_content = ""
        self.lines: List[str] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.section_matches: Dict[int, int] = {}  # section_id -> line_number
        self.declared_personas: Set[str] = set()
        self.referenced_personas: Set[str] = set()
        self.use_cases: List[Dict] = []
        self.technical_leakages: List[Dict] = []

    def load_file(self) -> bool:
        if not self.file_path.exists():
            self.errors.append(f"Target file not found: {self.file_path}")
            return False
        try:
            self.raw_content = self.file_path.read_text(encoding="utf-8")
            self.lines = self.raw_content.splitlines()
            return True
        except Exception as e:
            self.errors.append(f"Failed to read file {self.file_path}: {str(e)}")
            return False

    def extract_scope(self) -> None:
        """Detect scope level from document metadata or fall back to requested/default scope."""
        match = SCOPE_HEADER_PATTERN.search(self.raw_content)
        if match:
            self.detected_scope = match.group(1).lower()

        if self.requested_scope:
            self.effective_scope = self.requested_scope
            if self.detected_scope and self.detected_scope != self.requested_scope:
                self.warnings.append(
                    f"Scope Mismatch: Document metadata specifies Scope Level '{self.detected_scope.capitalize()}', "
                    f"but validation was executed with '--scope {self.requested_scope}'."
                )
        elif self.detected_scope in ["simple", "prototype", "mvp", "full"]:
            self.effective_scope = self.detected_scope
        else:
            self.effective_scope = "mvp"

    def validate_mandatory_sections(self) -> None:
        """Ensure all 7 mandatory sections exist in the document."""
        for sec_id, pattern, display_name in MANDATORY_SECTIONS:
            regex = re.compile(r"^#{1,3}\s+" + pattern, re.MULTILINE | re.IGNORECASE)
            found = False
            for idx, line in enumerate(self.lines):
                if regex.search(line):
                    self.section_matches[sec_id] = idx + 1
                    found = True
                    break
            if not found:
                self.errors.append(f"Missing mandatory section: '{display_name}'")

    def validate_mandatory_sections_simple(self) -> None:
        """Ensure all 4 mandatory sections exist in a simple-scope document."""
        for sec_id, pattern, display_name in MANDATORY_SECTIONS_SIMPLE:
            regex = re.compile(r"^#{1,3}\s+" + pattern, re.MULTILINE | re.IGNORECASE)
            found = False
            for idx, line in enumerate(self.lines):
                if regex.search(line):
                    self.section_matches[sec_id] = idx + 1
                    found = True
                    break
            if not found:
                self.errors.append(f"Missing mandatory section: '{display_name}'")

    def validate_technical_leakage(self) -> None:
        """Scan for technical keywords and architecture constructs."""
        in_code_block = False
        for idx, line in enumerate(self.lines, start=1):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                # Skip checking inside Gherkin feature blocks unless it contains obvious tech keywords
                if "gherkin" in line.lower() or "cucumber" in line.lower():
                    continue

            # Check for technical leakage patterns
            for pattern, category, guidance in TECHNICAL_LEAKAGE_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    matched_text = match.group(0)
                    # Ignore schema document self-references or warnings
                    if "BRD_SCHEMA" in line or "Zero Technical Leakage" in line:
                        continue
                    item = {
                        "line": idx,
                        "matched": matched_text,
                        "category": category,
                        "guidance": guidance,
                        "line_content": line.strip()
                    }
                    self.technical_leakages.append(item)
                    msg = f"Line {idx}: Detected technical scope leakage [{category}] -> '{matched_text}'. {guidance}."
                    if self.strict:
                        self.errors.append(msg)
                    else:
                        self.warnings.append(msg)

    def extract_personas_and_use_cases(self) -> None:
        """Extract declared personas in Section 2 and use case mappings in Section 4."""
        sec2_line = self.section_matches.get(2, 0)
        sec3_line = self.section_matches.get(3, len(self.lines))
        sec4_line = self.section_matches.get(4, 0)
        sec5_line = self.section_matches.get(5, len(self.lines))

        # Extract declared personas from Section 2 lines
        if sec2_line > 0:
            end_line = sec3_line if sec3_line > sec2_line else len(self.lines)
            sec2_text = "\n".join(self.lines[sec2_line - 1 : end_line])
            for match in PERSONA_DECLARATION_PATTERN.finditer(sec2_text):
                p_id = match.group(1).upper()
                if p_id not in ("PER-XXX", "PER-YYY", "PER-ZZZ", "PER-00N", "PER-NNN"):
                    self.declared_personas.add(p_id)

        # Extract use cases and referenced personas from Section 4 lines
        if sec4_line > 0:
            end_line = sec5_line if sec5_line > sec4_line else len(self.lines)
            current_uc = None

            for line_idx in range(sec4_line - 1, end_line):
                line = self.lines[line_idx]
                uc_match = USE_CASE_HEADER_PATTERN.search(line)
                if uc_match:
                    if current_uc:
                        self.use_cases.append(current_uc)
                    current_uc = {
                        "id": uc_match.group(1).upper(),
                        "title": uc_match.group(2).strip(),
                        "start_line": line_idx + 1,
                        "has_given_when_then": False,
                        "personas": set(),
                    }
                    continue

                if current_uc:
                    # Scan for persona references
                    for p_match in PERSONA_DECLARATION_PATTERN.finditer(line):
                        p_id = p_match.group(1).upper()
                        if p_id not in ("PER-XXX", "PER-YYY", "PER-ZZZ", "PER-00N", "PER-NNN"):
                            current_uc["personas"].add(p_id)
                            self.referenced_personas.add(p_id)

                    # Check for Given/When/Then or Gherkin scenarios
                    if ("Given " in line or "When " in line or "Then " in line or GHERKIN_SCENARIO_PATTERN.search(line)):
                        current_uc["has_given_when_then"] = True

            if current_uc:
                self.use_cases.append(current_uc)

    def extract_personas_and_use_cases_simple(self) -> None:
        """Extract declared personas in Section 2 and use case mappings in Section 3 (simple scope)."""
        sec2_line = self.section_matches.get(2, 0)
        sec3_line = self.section_matches.get(3, len(self.lines))
        sec4_line = self.section_matches.get(4, len(self.lines))

        # Extract declared personas from Section 2 lines
        if sec2_line > 0:
            end_line = sec3_line if sec3_line > sec2_line else len(self.lines)
            sec2_text = "\n".join(self.lines[sec2_line - 1 : end_line])
            for match in PERSONA_DECLARATION_PATTERN.finditer(sec2_text):
                p_id = match.group(1).upper()
                if p_id not in ("PER-XXX", "PER-YYY", "PER-ZZZ", "PER-00N", "PER-NNN"):
                    self.declared_personas.add(p_id)

        # Extract use cases and referenced personas from Section 3 lines (simple scope)
        if sec3_line > 0:
            end_line = sec4_line if sec4_line > sec3_line else len(self.lines)
            current_uc = None

            for line_idx in range(sec3_line - 1, end_line):
                line = self.lines[line_idx]
                uc_match = USE_CASE_HEADER_PATTERN.search(line)
                if uc_match:
                    if current_uc:
                        self.use_cases.append(current_uc)
                    current_uc = {
                        "id": uc_match.group(1).upper(),
                        "title": uc_match.group(2).strip(),
                        "start_line": line_idx + 1,
                        "has_given_when_then": False,
                        "personas": set(),
                    }
                    continue

                if current_uc:
                    # Scan for persona references
                    for p_match in PERSONA_DECLARATION_PATTERN.finditer(line):
                        p_id = p_match.group(1).upper()
                        if p_id not in ("PER-XXX", "PER-YYY", "PER-ZZZ", "PER-00N", "PER-NNN"):
                            current_uc["personas"].add(p_id)
                            self.referenced_personas.add(p_id)

                    # Check for Given/When/Then or Gherkin scenarios
                    if ("Given " in line or "When " in line or "Then " in line or GHERKIN_SCENARIO_PATTERN.search(line)):
                        current_uc["has_given_when_then"] = True

            if current_uc:
                self.use_cases.append(current_uc)

    def validate_persona_traceability(self) -> None:
        """Ensure no declared persona is orphaned without an associated use case."""
        orphaned = self.declared_personas - self.referenced_personas
        if orphaned:
            for p in sorted(orphaned):
                self.warnings.append(
                    f"Orphaned Persona Warning: Persona '{p}' is declared in Section 2 but has no mapped use cases in Section 4."
                )

    def validate_use_cases(self) -> None:
        """Validate use cases contain acceptance criteria and meaningful definitions."""
        if self.section_matches.get(4) and len(self.use_cases) == 0:
            self.errors.append("Section 4 is present but contains no identifiable use cases (expected format: '### UC-101: Title')")
            return

        for uc in self.use_cases:
            if not uc["has_given_when_then"]:
                self.warnings.append(
                    f"Use Case '{uc['id']}' (Line {uc['start_line']}): Missing formal Given-When-Then acceptance criteria."
                )

    def validate_use_cases_simple(self) -> None:
        """Validate use cases in simple scope (Section 3) contain acceptance criteria."""
        if self.section_matches.get(3) and len(self.use_cases) == 0:
            self.errors.append("Section 3 (Use Case Catalog) is present but contains no identifiable use cases (expected format: '### UC-101: Title')")
            return

        for uc in self.use_cases:
            if not uc["has_given_when_then"]:
                self.warnings.append(
                    f"Use Case '{uc['id']}' (Line {uc['start_line']}): Missing formal Given-When-Then acceptance criteria."
                )

    def validate_mapping_matrix_simple(self) -> None:
        """Validate that the Mapping Matrix (Section 4) references personas and use cases."""
        if not self.section_matches.get(4):
            return

        sec4_line = self.section_matches.get(4, 0)
        end_line = len(self.lines)

        has_mapping_refs = False
        for line_idx in range(sec4_line, end_line):
            line = self.lines[line_idx]
            # Check if line contains both a persona reference and a use case reference
            has_per = any(ref in line.upper() for ref in self.declared_personas)
            has_uc = any(f"UC-{uc['id'].split('-')[1]}" in line for uc in self.use_cases)
            if has_per and has_uc:
                has_mapping_refs = True
                break

        if not has_mapping_refs and self.declared_personas and self.use_cases:
            self.warnings.append(
                "Section 4 (Mapping Matrix): Expected to find at least one row linking a persona and a use case."
            )

    def validate_scope_boundaries(self) -> None:
        """Verify the document matches the expectations of the effective scope level."""
        persona_count = len(self.declared_personas)
        use_case_count = len(self.use_cases)

        if self.effective_scope == "simple":
            if persona_count == 0:
                self.warnings.append("Simple Scope: At least 1 persona should be declared in Section 2.")
            if use_case_count == 0:
                self.errors.append("Simple Scope: At least 1 use case must be defined in Section 3.")
        elif self.effective_scope == "prototype":
            if persona_count == 0:
                self.warnings.append("Prototype Scope: At least 1 core persona should be declared in Section 2.")
            elif persona_count > 3:
                self.warnings.append(
                    f"Prototype Scope Boundary Note: {persona_count} personas declared. Prototypes typically focus on 1-2 core user personas."
                )
            if use_case_count == 0:
                self.errors.append("Prototype Scope: At least 1 happy-path use case must be defined in Section 4.")
        elif self.effective_scope == "mvp":
            if persona_count < 2:
                self.warnings.append(
                    f"MVP Scope: Found {persona_count} declared personas. An MVP typically defines at least 2-3 core operational personas (End-User, Ops, Admin)."
                )
            if use_case_count < 2:
                self.warnings.append(
                    f"MVP Scope: Found {use_case_count} use cases. MVP releases typically define at least 2-3 core functional use cases."
                )
        elif self.effective_scope == "full":
            if persona_count < 3:
                self.warnings.append(
                    f"Full Enterprise Scope: Found only {persona_count} declared personas. Full enterprise specifications should define a comprehensive 360° ecosystem (4+ personas including Support, Risk/Compliance, Admin)."
                )
            if use_case_count < 2:
                self.warnings.append(
                    f"Full Enterprise Scope: Found {use_case_count} use cases. Full enterprise releases typically require comprehensive L1/L2 capability use case catalogs."
                )

    def run_all(self) -> bool:
        """Execute full validation suite and return True if passed."""
        if not self.load_file():
            return False

        self.extract_scope()

        if self.effective_scope == "simple":
            # Simple scope validation path
            self.validate_mandatory_sections_simple()
            self.validate_technical_leakage()
            self.extract_personas_and_use_cases_simple()
            self.validate_persona_traceability()
            self.validate_use_cases_simple()
            self.validate_mapping_matrix_simple()
            self.validate_scope_boundaries()
        else:
            # Original 7-section validation path (prototype/mvp/full)
            self.validate_mandatory_sections()
            self.validate_technical_leakage()
            self.extract_personas_and_use_cases()
            self.validate_persona_traceability()
            self.validate_use_cases()
            self.validate_scope_boundaries()

        return len(self.errors) == 0

    def generate_json_report(self) -> str:
        mandatory_sections_for_scope = MANDATORY_SECTIONS_SIMPLE if self.effective_scope == "simple" else MANDATORY_SECTIONS
        data = {
            "file": str(self.file_path),
            "status": "PASSED" if len(self.errors) == 0 else "FAILED",
            "strict_mode": self.strict,
            "scope": {
                "effective_scope": self.effective_scope,
                "detected_in_document": self.detected_scope,
                "requested_by_user": self.requested_scope,
            },
            "summary": {
                "errors_count": len(self.errors),
                "warnings_count": len(self.warnings),
                "mandatory_sections_found": len(self.section_matches),
                "mandatory_sections_required": len(mandatory_sections_for_scope),
                "personas_declared": len(self.declared_personas),
                "personas_mapped": len(self.referenced_personas),
                "use_cases_count": len(self.use_cases),
                "technical_leakage_detected": len(self.technical_leakages),
            },
            "errors": self.errors,
            "warnings": self.warnings,
            "declared_personas": sorted(list(self.declared_personas)),
            "use_cases": [
                {
                    "id": uc["id"],
                    "title": uc["title"],
                    "line": uc["start_line"],
                    "has_acceptance_criteria": uc["has_given_when_then"],
                    "mapped_personas": sorted(list(uc["personas"])),
                }
                for uc in self.use_cases
            ],
            "technical_leakages": self.technical_leakages,
        }
        return json.dumps(data, indent=2)

    def print_text_report(self) -> None:
        print(f"\n{COLOR_BOLD}{COLOR_BLUE}=== Business Requirements Document (BRD) Linter ==={COLOR_RESET}")
        print(f"Target File:    {COLOR_BOLD}{self.file_path}{COLOR_RESET}")
        print(f"Scope Boundary: {COLOR_BOLD}{COLOR_CYAN}{self.effective_scope.upper()}{COLOR_RESET}" + (" (Detected in document)" if self.detected_scope else " (Default)"))
        print(f"Strict Mode:    {'Enabled' if self.strict else 'Disabled'}\n")

        # Mandatory Sections Check
        mandatory_sections_for_scope = MANDATORY_SECTIONS_SIMPLE if self.effective_scope == "simple" else MANDATORY_SECTIONS
        section_header = "Mandatory Sections (Simple Scope - 4 Sections):" if self.effective_scope == "simple" else "Mandatory Sections (BABOK & IEEE 29148 - 7 Sections):"
        print(f"{COLOR_BOLD}1. {section_header}{COLOR_RESET}")
        for sec_id, _, name in mandatory_sections_for_scope:
            if sec_id in self.section_matches:
                line_no = self.section_matches[sec_id]
                print(f"  {COLOR_GREEN}✓{COLOR_RESET} Section {sec_id}: {name} (Line {line_no})")
            else:
                print(f"  {COLOR_RED}✗{COLOR_RESET} Section {sec_id}: {name} {COLOR_RED}[MISSING]{COLOR_RESET}")

        # Persona & Use Case Statistics
        print(f"\n{COLOR_BOLD}2. Traceability & Persona Coverage:{COLOR_RESET}")
        print(f"  • Personas Declared:   {len(self.declared_personas)} ({', '.join(sorted(self.declared_personas)) or 'None'})")
        print(f"  • Personas Mapped:     {len(self.referenced_personas)} ({', '.join(sorted(self.referenced_personas)) or 'None'})")
        print(f"  • Use Cases Analyzed:  {len(self.use_cases)}")

        # Technical Scope Leakage
        print(f"\n{COLOR_BOLD}3. Pure Functional Scope Integrity:{COLOR_RESET}")
        if len(self.technical_leakages) == 0:
            print(f"  {COLOR_GREEN}✓ Zero technical scope leakage detected (pure business specification).{COLOR_RESET}")
        else:
            status_color = COLOR_RED if self.strict else COLOR_YELLOW
            print(f"  {status_color}! Found {len(self.technical_leakages)} potential technical leakage instances.{COLOR_RESET}")

        # Warnings & Errors
        if self.warnings:
            print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Warnings ({len(self.warnings)}):{COLOR_RESET}")
            for w in self.warnings:
                print(f"  {COLOR_YELLOW}⚠ {w}{COLOR_RESET}")

        if self.errors:
            print(f"\n{COLOR_BOLD}{COLOR_RED}Errors ({len(self.errors)}):{COLOR_RESET}")
            for e in self.errors:
                print(f"  {COLOR_RED}✖ {e}{COLOR_RESET}")

        # Final Result Banner
        print("\n" + "=" * 60)
        if len(self.errors) == 0:
            print(f"{COLOR_BOLD}{COLOR_GREEN}✓ VALIDATION PASSED: The document is a verified, pure Business Requirements Document [{self.effective_scope.upper()} Scope].{COLOR_RESET}")
        else:
            print(f"{COLOR_BOLD}{COLOR_RED}✗ VALIDATION FAILED: {len(self.errors)} blocking issue(s) detected.{COLOR_RESET}")
        print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Business Requirements Documents (BRD) against BABOK and IEEE 29148 standards."
    )
    parser.add_argument("file_path", type=str, help="Path to the BRD markdown file to validate")
    parser.add_argument("--scope", choices=["simple", "prototype", "mvp", "full"], help="Target scope boundary to validate against (simple, prototype, mvp, full)")
    parser.add_argument("--strict", action="store_true", help="Enable strict mode (fails on technical leakage warnings)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON report")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-error text output")

    args = parser.parse_args()
    target_path = Path(args.file_path).resolve()

    validator = BRDValidator(target_path, strict=args.strict, scope=args.scope)
    passed = validator.run_all()

    if args.json:
        print(validator.generate_json_report())
    elif not args.quiet:
        validator.print_text_report()

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
