# Python AI Observability Conventions

Resolved per-context — only cited when a confirmed context needs tracing/eval visibility into its
agentic-AI capability. Assumes `conventions/python/language-conventions.md` already applies.

## LangSmith is additive, not a framework choice

Per `stacks/defaults.md`: LangSmith (tracing/eval) is a separate, additive decision — it doesn't
compete with or imply a choice between LangChain and LangGraph, and applies regardless of which
orchestration framework (if any) the capability uses.

## Trace at the boundary, not just inside the framework

Instrument tool calls, retrieval steps, and model invocations with structured spans/metadata (input
size, latency, token counts) — don't rely solely on default framework instrumentation if a step
calls out to custom code the framework can't see into.

```python
# Bad — no visibility into what the tool actually did
@mcp.tool()
def search_orders(customer_id: str) -> list[OrderSummary]:
    return order_repo.find_by_customer(customer_id)

# Good — structured span around the boundary call
@mcp.tool()
@traceable(name="search_orders")
def search_orders(customer_id: str) -> list[OrderSummary]:
    return order_repo.find_by_customer(customer_id)
```

## Do NOT

- Do not treat LangSmith adoption as mutually exclusive with a LangChain-vs-LangGraph decision —
  it's additive to either
- Do not leave custom tool/retrieval code uninstrumented just because the surrounding framework has
  its own default tracing
