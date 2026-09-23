# Spring Boot 4 · Spring AI + MCP

Rare fallback only — the AI/agentic layer defaults to Python (`python-ai-agentic.md`, see
`defaults.md`). Select this file only when a context deliberately hosts MCP exposure or LLM
integration inside an existing Spring Boot service rather than standing up a separate Python
service, and the Agentic-AI ADR (`architecture-decisions.md`) confirms a real capability — this
playbook does not fit an unconfirmed or "not applicable" verdict either way.

## Fits
- **Capability:** confirmed agentic-AI ADR — multi-step autonomous reasoning, RAG, tool-calling, or
  exposing application capabilities to external agents via MCP
- **Contract:** bounded DTO responses from any exposed tool, never entities or unbounded collections

## Does NOT fit
- No existing Spring Boot service to host it in, and no deliberate reason to add one — default to
  `python-ai-agentic.md` instead
- Agentic-AI ADR verdict is "Not applicable" — don't select this playbook on an FR alone if the
  confirmed ADR already closed that door; route back to `architecture-decisions` instead
- Simple deterministic business logic with no genuine LLM/agent need

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| LLM integration | Spring AI 2.0 (Boot 4 requires 2.0; Spring AI 1.x targets Boot 3 only) |
| MCP exposure | Spring AI's MCP server starter + native `@McpTool`/`@McpToolParam` annotations; standalone MCP Java SDK only when Spring integration is deliberately not wanted |
| Transport | Streamable HTTP preferred over SSE for a new remote server |
| Telemetry | AI-specific observability layered on the baseline production-observability setup — token usage, latency, cost attribution |

## Prerequisites
- API keys from environment/config, never hardcoded; model IDs configured externally (provider
  catalogs change)
- Tool hints are not authorization — enforce access control in application code, not by trusting
  what a tool description implies
- Prompts externalized to resources, not string-concatenated inline

## Tradeoffs
- Fast-moving dependency surface (Spring AI's 2.0 API already broke compatibility with 1.x once) —
  pin versions deliberately and expect more churn than the rest of this catalog

## Implementation detail
`implementation-guide` (Phase 7) — spring-ai-integration, mcp-server, ai-observability.
