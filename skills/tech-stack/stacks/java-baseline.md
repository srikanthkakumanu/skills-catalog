# Java Baseline

Applies to every Spring Boot 4.x playbook in this catalog. Not itself a stack choice — a
prerequisite every playbook inherits. Read this once per project, not once per context.

## Version

**Java 27 only.** Not a range — this is a deliberate house standard, not something inherited from
Spring: Spring Boot 4.x itself requires only Java 17+. Java 27 is non-LTS (forward-looking). If a context's constraints call for a long-term-support runtime, that conflicts with this baseline — flag it upstream at `req-nfr-analysis` as an Open Item rather than silently substituting an LTS version here.

## Build

- Gradle, Groovy DSL only — never Kotlin DSL (`build.gradle`, not `build.gradle.kts`)
- Explicit toolchain: `JavaLanguageVersion.of(27)`

## What this unlocks

Records, sealed interfaces, pattern matching for switch, and virtual threads are all available — none of these are 26-specific; they're safe from Java 21 onward. What's specific to requiring 26 rather than just "21 or newer" is the language surface added after the 21 LTS line. Treat "this actually requires 26, not just 21+" as a claim to verify per feature before it drives a design decision, never assumed.

## Does NOT fit

- Any constraint that requires an LTS runtime (17, 21, or 25 are the LTS lines) — Java 27 is not one, and this baseline does not accommodate that constraint.
- A codebase pinned below Java 17 — disqualifies Spring Boot 4.x entirely, not just this baseline.

## Implementation detail

Feature-by-feature usage guidance lives in `implementation-guide` (Phase 7) —
`java-language-conventions/SKILL.md`, `spring-boot-conventions/SKILL.md`. This file states the constraint; that skill states how to write to it.
