# Quickstart: OpenAI Agent Tools

**Feature**: `004-openai-agent-tools`

## Prerequisites

1.  **Environment**: Ensure you have Python 3.12+ and `uv` installed.
2.  **Database**: Ensure Neon PostgreSQL is running (or local equivalent).
3.  **API Key**: Set `OPENAI_API_KEY` in `backend/.env` (though not strictly needed for tool *execution* unit tests, it is needed for full agent integration).

## Setup

1.  Install dependencies:
    ```bash
    cd backend
    uv pip install openai-agents-python
    # or
    pip install openai-agents-python
    ```

## Running Tests

We will have unit tests specifically for the tools to ensure they interact with the DB correctly without needing a real LLM call.

```bash
cd backend
pytest tests/unit/test_agent_tools.py
```

## Manual Verification

You can test the tools interactively in a Python shell:

```python
import asyncio
from src.agent.tools import add_task, list_tasks
from src.db import get_session

async def test_tools():
    # Mock context or set up dependency injection manually for this script
    # This part depends on final implementation details of dependency injection
    print(await add_task(user_id="test_user", title="Test Task"))
    print(await list_tasks(user_id="test_user"))

if __name__ == "__main__":
    asyncio.run(test_tools())
```
