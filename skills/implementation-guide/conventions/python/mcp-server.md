# Python MCP Server Conventions

Resolved per-context — only cited when a confirmed context exposes an MCP server in Python (see
`tech-stack/stacks/python-ai-agentic.md`; for hosting MCP inside an existing Spring Boot service
instead, see `skills/ai-integration/mcp-server/` under the Java side). Assumes
`conventions/python/language-conventions.md` (type hints, Pydantic, async discipline) already applies.

## SDK choice

Official MCP Python SDK, or FastMCP for a standalone server — per `python-ai-agentic.md`'s Stack
table. Prefer Streamable HTTP transport over SSE for a new remote server; SSE is legacy transport at
this point.

## Tools return typed, bounded data — never raw ORM objects or unbounded collections

A tool's return type is part of its contract with the calling model — validate and shape it with
Pydantic, the same as any other API boundary.

```python
# Bad — leaks an ORM object and can return an unbounded result set
@mcp.tool()
def search_orders(customer_id: str):
    return db.query(Order).filter_by(customer_id=customer_id).all()

# Good — typed, paginated response
class OrderSummary(BaseModel):
    order_id: str
    status: str
    total: Decimal

@mcp.tool()
def search_orders(customer_id: str, limit: int = 20) -> list[OrderSummary]:
    orders = order_repo.find_by_customer(customer_id, limit=limit)
    return [OrderSummary.model_validate(o) for o in orders]
```

## Tool descriptions are not authorization

A tool's docstring/description tells the model what the tool does — it enforces nothing. Access
control belongs in the tool's implementation (auth context, permission checks), never assumed from
what the description implies a caller may or may not do.

## Do NOT

- Do not return unbounded query results from a tool — always paginate or cap
- Do not return raw database/ORM entities — map to a Pydantic response model first
- Do not treat a tool's docstring as an authorization boundary — enforce access control in code
- Do not use SSE transport for a new server — prefer Streamable HTTP
