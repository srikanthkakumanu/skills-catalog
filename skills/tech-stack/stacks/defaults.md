# Stack Defaults — standing policy

| Layer type                      | Default                            | Build tool                         |
| ------------------------------- | ---------------------------------- | ---------------------------------- |
| Microservice / business-logic   | Spring Boot 4.x, Java 27 — see `java-baseline.md` | Gradle (Groovy DSL) Latest Version |
| AI / agentic (MCP, RAG, agents) | Python (runtime settled by policy) | uv Latest Version                  |

**AI framework composition — not policy-resolved, ask individually:** LangChain,
LangGraph, OpenAI SDK, Claude SDK are all in scope; which combination applies
depends on what that specific AI capability needs (multi-agent orchestration
points toward LangGraph; a single direct model call may need no framework layer
at all). Present the options with a one-line note on when each fits, then ask.
LangSmith (tracing/eval) is a separate, additive choice — not a competing option
with the above.

Catalog playbooks: `stacks/python-ai-agentic.md` documents this default stack;
`stacks/springboot4-ai-mcp.md` is a rare fallback for hosting inside an existing
Spring Boot service — see `stacks/INDEX.md`.

**Common infra, any layer:** Docker · Kubernetes · GitHub Actions · Redis

**Messaging — pattern-based, not blanket:**

- High-throughput event-streaming / log-style / event-sourcing → Kafka
- Task/work-queue (job dispatch, retry/dead-letter, point-to-point async) → RabbitMQ
- Pattern not clear from `detailed-design.md` → do not assume; ask individually

**Database:** no blanket default. Derive constraints from `detailed-design.md`'s Data
Architecture per context; check other `stacks/*.md` catalog files for a matching DB
entry before treating the context as off-catalog.
