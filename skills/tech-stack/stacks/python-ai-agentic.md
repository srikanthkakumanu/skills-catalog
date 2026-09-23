# Python · AI / Agentic (LangChain, LangGraph, MCP)

Default playbook for the AI/agentic layer — `stacks/defaults.md` policy-resolves this layer to
Python; select this file whenever a context has a confirmed agentic-AI capability and no
deliberate reason to host it inside an existing Spring service (see `springboot4-ai-mcp.md` for
that rare fallback).

## Fits
- **Capability:** confirmed agentic-AI ADR — multi-step autonomous reasoning, RAG, tool-calling, or
  exposing application capabilities to external agents via MCP
- **Contract:** bounded, typed responses from any exposed tool, never raw ORM objects or unbounded
  collections

## Does NOT fit
- Agentic-AI ADR verdict is "Not applicable" — don't select this playbook on an FR alone if the
  confirmed ADR already closed that door; route back to `architecture-decisions` instead
- Simple deterministic business logic with no genuine LLM/agent need
- A deliberate choice to host MCP exposure inside an existing Spring Boot service — use
  `springboot4-ai-mcp.md` for that case instead

## Stack
| Component | Choice |
|---|---|
| Language / runtime | Python (uv-managed environment and dependency resolution, per `defaults.md`) |
| Orchestration | LangChain or LangGraph — not policy-resolved; pick per capability (LangGraph for multi-agent/stateful orchestration, LangChain for simpler chains, no framework at all for a single direct model call) |
| Model access | OpenAI SDK and/or Claude SDK, direct — per the model provider(s) the capability actually needs |
| MCP exposure | Official MCP Python SDK (or FastMCP) for a standalone MCP server; Streamable HTTP preferred over SSE for a new remote server |
| Observability | LangSmith — separate, additive choice per `defaults.md`, not a competing option with the orchestration framework |

## Prerequisites
- API keys from environment/config, never hardcoded; model IDs configured externally (provider
  catalogs change)
- Tool hints are not authorization — enforce access control in application code, not by trusting
  what a tool description implies
- Prompts externalized to resources/templates, not string-concatenated inline
- Framework choice (LangChain vs. LangGraph vs. none) and LangSmith are always asked individually
  per `defaults.md` — this playbook documents the tool surface, it does not pre-select among them

## Tradeoffs
- Fast-moving dependency surface across LangChain/LangGraph/MCP SDKs — pin versions deliberately
  and expect more churn than the rest of this catalog
- Running a separate Python service (vs. embedding in an existing Java service) adds a deployable
  and an inter-service call for contexts that already have a Spring Boot service doing related work

## Implementation detail
`implementation-guide` (Phase 7) — `conventions/python/language-conventions.md` (unconditional
baseline), then per-capability: `conventions/python/langchain-integration.md`,
`conventions/python/langgraph-orchestration.md`, `conventions/python/mcp-server.md`,
`conventions/python/ai-observability.md`.
