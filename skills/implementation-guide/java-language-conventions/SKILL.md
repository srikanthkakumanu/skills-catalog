---
name: java-language-conventions
description: >
  Java 27 (JDK 27) baseline for this catalog — version/toolchain/build facts and language-feature
  usage guidance (records, sealed interfaces, pattern matching, virtual threads, structured
  concurrency). Restates tech-stack/stacks/java-baseline.md's constraint; loaded unconditionally
  for every Java context by implementation-guide, never resolved per-topic.
---
# Java 27 (JDK 27)

Restates the constraint from `tech-stack/stacks/java-baseline.md` identically — read that file for
the decision and its rationale; this file states how `implementation-guide` applies it, and covers
both the version/toolchain facts and language-feature usage guidance in one place. Spring
Boot–specific project conventions live in `../spring-boot-conventions/SKILL.md`.

## Version

**Java 27 only.** Non-LTS, forward-looking house standard — not inherited from Spring Boot 4.x, which itself requires only Java 17+. No fallback to Java 21 or Java 25 LTS in this catalog's builds or CI.

## Build

- Gradle, Groovy DSL only — never Kotlin DSL, never Maven
- Explicit toolchain: `JavaLanguageVersion.of(27)`

## Runtime

OpenJDK or a vendor build of JDK 27 (Temurin, Corretto, Zulu, or official OpenJDK builds). Confirm your JDK provider actually publishes non-LTS builds before committing — some corporate distributions track LTS lines only.

## Preview features

Java 27 may ship features still flagged `--enable-preview` (e.g. structured concurrency, an
evolving Vector API). These are not finalized and are out of scope for production code paths in
this catalog — see Structured concurrency below for what's safe to use versus preview.

## Does NOT fit

Same disqualifiers as `java-baseline.md`: any constraint requiring an LTS runtime, or a codebase
pinned below Java 17.

## Records over classes for data carriers

Use a record for any immutable data holder — DTOs, value objects, command/query payloads. Compact
constructors validate; don't hand-write `equals`/`hashCode`/`toString`/accessors.

```java
// Bad — mutable class doing a record's job
public class CreateOrderRequest {
    private String customerId;
    private BigDecimal amount;
    // getters, setters, equals, hashCode, toString...
}

// Good
public record CreateOrderRequest(String customerId, BigDecimal amount) {
    public CreateOrderRequest {
        if (amount.signum() <= 0) throw new IllegalArgumentException("amount must be positive");
    }
}
```

## Sealed interfaces for closed domain hierarchies

Use `sealed` when a type has a fixed, known set of implementations the compiler should enforce
exhaustiveness over (state machines, result types, domain events). Don't seal a type meant to be
extended by unknown future implementations.

```java
public sealed interface PaymentResult permits Approved, Declined, Pending {}
public record Approved(String authCode) implements PaymentResult {}
public record Declined(String reason) implements PaymentResult {}
public record Pending(String reference) implements PaymentResult {}
```

## Pattern matching for switch

Prefer an exhaustive `switch` expression over `instanceof` chains once a type is sealed — the
compiler flags missing cases at the call site, not at runtime.

```java
// Bad
if (result instanceof Approved a) return ok(a.authCode());
else if (result instanceof Declined d) return error(d.reason());
else if (result instanceof Pending p) return accepted(p.reference());
else throw new IllegalStateException("unhandled");

// Good — exhaustive, no else/default needed once PaymentResult is sealed
return switch (result) {
    case Approved a -> ok(a.authCode());
    case Declined d -> error(d.reason());
    case Pending p -> accepted(p.reference());
};
```

Use guard conditions (`case Declined d when d.reason().equals("FRAUD")`) instead of nesting an `if`
inside the case body.

## Virtual threads

Use virtual threads for I/O-bound concurrency (blocking HTTP/DB/file calls fanned out across many
tasks) — not for CPU-bound work, where platform threads pinned to cores still win.

```java
// Good — virtual-thread-per-task executor for blocking I/O fan-out
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var futures = orderIds.stream()
        .map(id -> executor.submit(() -> orderClient.fetch(id)))
        .toList();
    // ...
}
```

Don't pool virtual threads (`newFixedThreadPool` defeats the point) and don't reach for them in
tight CPU-bound loops.

## Structured concurrency

Still preview in Java 27 — useful for sharing a deadline/cancellation scope across subtasks, but
don't ship it in production code paths until it finalizes. Flag any use in review as "preview API,
requires `--enable-preview`."

## Do NOT

- Do not use raw `Thread` or unbounded thread pools for I/O-bound fan-out — use virtual threads
- Do not hand-write `equals`/`hashCode`/`toString`/getters for immutable data — use a record
- Do not chain `instanceof` checks over a type family that could be sealed
- Do not ship preview-flagged APIs (structured concurrency, evolving Vector API) in production code
  paths
