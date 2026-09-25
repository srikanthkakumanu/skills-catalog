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
| React (frontend, evidence-gated) | 19.3.x — see `../typescript-language-conventions/SKILL.md` |
| Next.js (frontend, evidence-gated) | 16.2.x, App Router, Turbopack default |
| TypeScript (frontend, evidence-gated) | 5.9.x only — see `../typescript-language-conventions/SKILL.md` |
| TanStack Query                | 5.103.x (`@tanstack/react-query`) |
| Zod                           | 4.6.x |
| React Hook Form               | 7.88.x (+ `@hookform/resolvers` ^5.1.0) |
| Tailwind CSS                  | 4.3.x, CSS-first `@theme` |
| Vitest                        | 5.0.x |
| React Testing Library          | 16.3.x (`@testing-library/react`) |
| Playwright                    | 1.63.x (`@playwright/test`) |
| Node.js (frontend)             | 24.x, Active LTS |
| pnpm                          | Latest Version — house package manager for frontend contexts |

Cloud/deployment: zero vendor lock-in, pure open-source (Apache 2.0 / Spring License);
cloud-agnostic across Kubernetes, AWS, GCP, Azure, on-premises.
