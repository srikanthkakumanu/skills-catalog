# LangChain Integration Conventions

Resolved per-context — only cited when a confirmed context's AI capability needs a simpler chain
(not multi-agent orchestration — that's LangGraph's job, per `stacks/defaults.md`) and LangChain was
the chosen framework. Assumes `conventions/python/language-conventions.md` already applies.

## Prompts are externalized, not string-concatenated inline

Per `python-ai-agentic.md`'s Prerequisites: prompts live in resource files/templates, not built up
with inline string concatenation in application code.

```python
# Bad
prompt = "You are a helpful assistant. " + context + " Answer: " + question

# Good
prompt = prompt_template.invoke({"context": context, "question": question})
```

## Output parsers are typed

Parse LLM output into a Pydantic model rather than consuming raw text downstream — use LangChain's
structured-output/tool-calling support instead of regex-parsing a text response.

```python
# Bad
response = llm.invoke(prompt)
name = response.content.split("Name:")[1].strip()  # brittle text parsing

# Good
class ExtractedEntity(BaseModel):
    name: str
    category: str

structured_llm = llm.with_structured_output(ExtractedEntity)
result = structured_llm.invoke(prompt)
```

## Do NOT

- Do not build prompts via inline string concatenation — use externalized templates
- Do not parse LLM text output with string splitting/regex — use structured output into a Pydantic
  model
- Do not reach for LangChain when the capability is a single direct model call needing no framework
  (per `stacks/defaults.md`)
