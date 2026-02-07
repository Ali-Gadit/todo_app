# Research: OpenAI Agent Tools

**Feature**: `004-openai-agent-tools`
**Date**: 2026-02-02
**Status**: Complete

## Decision: Use `openai-agents-python` SDK

We will use the `openai-agents-python` library to define our agent and its tools. This library simplifies the process of creating function-calling agents by using Python decorators to automatically generate schemas and handle tool execution.

### Rationale

- **Declarative Syntax**: The `@function_tool` decorator allows us to define tools as standard Python functions with type hints and docstrings. The SDK handles the conversion to OpenAI's JSON schema format.
- **Type Safety**: Leveraging Python's type hints ensures that the tools are robust and errors are caught early.
- **Integration**: It integrates well with our existing Python backend stack.
- **Documentation**: The library provides clear examples for synchronous and asynchronous tools, which matches our needs (DB ops are typically async).

### Alternatives Considered

- **Manual Schema Generation**: We could manually write the JSON schemas for each tool and pass them to the standard `openai` library.
    - *Rejected*: Error-prone, verbose, and duplicates effort (code + schema must be kept in sync).
- **LangChain**: A larger framework that supports agents.
    - *Rejected*: Overkill for this specific requirement. We want a lightweight integration for Phase III, not a full framework rewrite. `openai-agents-python` is more focused.

## Implementation Details

### Tool Definition Pattern

Based on the research, we will define tools using the `@function_tool` decorator.

```python
from agents import function_tool

@function_tool
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task for the user."""
    # DB logic here
    return {"task_id": 1, "status": "created", "title": title}
```

### Dependency Injection

The tools need access to the database. The `openai-agents-python` library supports a context wrapper (`RunContextWrapper`) which can be used to pass dependencies like the DB session or connection pool to the tools.

```python
from agents import function_tool, RunContextWrapper

@function_tool
def list_tasks(ctx: RunContextWrapper[dict], status: str = "all") -> list:
    db = ctx.context.get("db_session")
    # ... use db ...
```

*Refinement*: For simplicity in the initial implementation, if `RunContextWrapper` adds too much complexity, we might use a scoped session dependency or a helper function to get a fresh session per tool invocation, ensuring thread safety.

## Action Items

1.  Add `openai-agents-python` to `backend/requirements.txt`.
2.  Create `backend/src/agent/tools.py` to house the 5 functions.
3.  Ensure `Task` model in `backend/src/models/` is accessible to the tools.
