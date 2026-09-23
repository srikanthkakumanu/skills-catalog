# LangGraph Orchestration Conventions

Resolved per-context — only cited when a confirmed context's AI capability needs multi-agent or
stateful orchestration and LangGraph was the chosen framework (per `stacks/defaults.md`: framework
choice among LangChain/LangGraph/none is asked individually per capability, never assumed here).
Assumes `conventions/python/language-conventions.md` already applies.

## State is a typed schema, not a bare dict

Define the graph's state as a `TypedDict` or Pydantic model — every node's input/output shape should
be checkable, not implicit.

```python
# Bad
def add_context_node(state: dict) -> dict:
    state["context"] = retrieve(state["query"])
    return state

# Good
class GraphState(TypedDict):
    query: str
    context: list[str]
    answer: str | None

def add_context_node(state: GraphState) -> GraphState:
    return {**state, "context": retrieve(state["query"])}
```

## Nodes are pure functions over state where possible

Keep side effects (LLM calls, tool calls, external I/O) explicit and isolated per node — avoid a
node silently mutating shared state that other nodes depend on implicitly.

## Checkpointing for anything long-running or resumable

Use LangGraph's checkpointer for graphs that need to survive a restart or support human-in-the-loop
interruption — don't hold multi-step conversation state only in process memory.

## Do NOT

- Do not use a bare `dict` for graph state — define a typed schema
- Do not assume LangGraph is the right choice without checking `stacks/defaults.md`'s guidance
  (LangGraph is for multi-agent/stateful orchestration; a single direct model call needs no
  framework at all)
- Do not skip checkpointing for a graph whose conversation needs to survive a process restart
