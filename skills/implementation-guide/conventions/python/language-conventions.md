# Python Language Conventions

Universal Python baseline for every Python context in this catalog (currently the AI/agentic layer
— `tech-stack/stacks/python-ai-agentic.md`). Plain reference content, no `SKILL.md` frontmatter —
loaded unconditionally by `implementation-guide` whenever a confirmed context's resolved language is
Python, the same way `../../java-language-conventions/SKILL.md` is loaded unconditionally for Java. Capability-specific
guidance (MCP, LangGraph, LangChain, observability) lives in sibling files in this folder and is
resolved per-context by citation, not loaded unconditionally.

## Version

Python 3.11.x — see `tech-stack/conventions/compatibility-baseline.md` for the pinned line. No
Python 2 compatibility code, no reliance on pre-3.10 syntax (this catalog assumes structural pattern
matching and modern typing generics are available).

## Environment & dependencies

- `uv` exclusively for environment and dependency management (per `stacks/defaults.md`) — never
  bare `pip install` without a lockfile, never Poetry/Pipenv in this catalog
- `pyproject.toml` is the single source of truth for dependencies and tool config
- Pin dependency versions deliberately, especially across the LangChain/LangGraph/MCP SDK surface —
  `python-ai-agentic.md` already flags this as a fast-moving, high-churn dependency set

## Type hints

Mandatory on every public function/method signature — parameters and return type. Run `mypy` or
`pyright` in strict mode; don't use bare `Any` without a comment justifying why the type can't be
narrowed.

```python
# Bad
def fetch_order(order_id):
    ...

# Good
def fetch_order(order_id: str) -> Order | None:
    ...
```

## Data validation — Pydantic v2 at every boundary

Use a Pydantic `BaseModel` for anything crossing a boundary: API request/response bodies, config
loaded from env/files, responses from external APIs or LLM tool calls. Use a plain `dataclass` only
for internal-only data that never needs validation.

```python
# Bad — untyped dict passed across a boundary
def create_order(payload: dict) -> dict:
    ...

# Good
class CreateOrderRequest(BaseModel):
    customer_id: str
    amount: Decimal = Field(gt=0)

def create_order(request: CreateOrderRequest) -> OrderResponse:
    ...
```

## Formatting & linting — Ruff, not manual PEP 8

PEP 8 compliance is enforced by tooling, not by hand: run `ruff format` and `ruff check --fix`
before committing. Don't hand-format to match PEP 8 conventions Ruff already auto-fixes, and don't
add flake8/isort/pyupgrade as separate tools — Ruff replaces all of them in this catalog.

## Async discipline

This catalog's Python workloads (LangGraph orchestration, MCP servers, agentic tool-calling) are
async-first. Never block the event loop with synchronous I/O inside an `async def` — use `httpx`
(async client) instead of `requests`, and offload genuinely CPU-bound work to a thread/process pool
rather than running it inline.

## Error handling & logging

- Use the `logging` module, never `print()`, in library or service code
- Define a project-specific exception hierarchy — don't let bare `Exception` cross a service
  boundary uncaught
- Never use a bare `except:` — catch specific exception types

## Project structure

`src/<package>/` layout — package code under `src/`, not flat at the repo root — with `tests/`
mirroring the package structure. `pyproject.toml` at the repo root.

## Do NOT

- Do not use bare `pip install` without a lockfile — use `uv`
- Do not pass untyped `dict`/`Any` across a service or API boundary — use a Pydantic model
- Do not hand-enforce PEP 8 spacing/import-order rules that `ruff format`/`ruff check` already fix
- Do not perform blocking I/O inside `async def` functions
- Do not use `print()` for anything other than a CLI's actual user-facing output
- Do not hardcode API keys or model IDs — load from environment/config (per
  `python-ai-agentic.md`'s Prerequisites)
