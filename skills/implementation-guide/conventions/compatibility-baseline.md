# Compatibility Baseline

Verified-compatible version pins for this catalog's Spring Boot 4.x stack, as of Aug 2026.
Extracted from the retired omnibus playbook prototype (it fit every constraint and disqualified
nothing, so it was split into `tech-stack/stacks/*.md` — this table is the one part of it that
wasn't a decision and was worth keeping).

Recheck against official release notes before adopting a later release on any line.

| Component                    | Version                      |
| ---------------------------- | ---------------------------- |
| Spring Boot                  | 4.1.x                        |
| Spring Framework             | 7.x                          |
| Spring Cloud                 | 2025.1 BOM                   |
| Spring AI                    | 2.0.x                        |
| MCP Java SDK                 | 2.0.x                        |
| Spring Cloud Gateway         | 5.0.x                        |
| GraalVM (native compilation) | 25.x+                        |
| Java                         | 27 only — see `../java-language-conventions/SKILL.md`      |
| Python                       | 3.11.* — see `conventions/python/language-conventions.md` |
| uv                           | Latest Version               |
| Gradle                       | Latest Version               |

Cloud/deployment: zero vendor lock-in, pure open-source (Apache 2.0 / Spring License);
cloud-agnostic across Kubernetes, AWS, GCP, Azure, on-premises.
