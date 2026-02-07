---
name: openai-agents-creater
description: Generates Python agents using the OpenAI Agents SDK with custom model providers like Groq, Gemini (OpenAI-compatible), or other OpenAI-compatible APIs.
---

# OpenAI Agents Creator Skill

This Skill generates Python agent code using the OpenAI Agents SDK with support for custom model providers and OpenAI-compatible APIs (like Groq).

## Usage

To generate an agent, specify:
- **agent_name**: Name for the agent variable/class.
- **instructions**: System instructions for the agent.
- **model_name**: The exact model ID (e.g., `openai/gpt-oss-20b` or `llama-3.3-70b-versatile`).
- **base_url**: The API endpoint (e.g., `https://api.groq.com/openai/v1`).
- **api_key_var**: The environment variable name (e.g., `GROQ_API_KEY`).

## Code Template

The skill uses this robust pattern to ensure custom routing and proper environment setup for tracing:

```python
from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Critical: Load .env before accessing API keys to avoid tracing errors
load_dotenv()

# Get API key with explicit error handling for better debugging/tracing
API_KEY = os.getenv("API_KEY_VAR")
if not API_KEY:
    raise ValueError("API_KEY_VAR environment variable is required in .env file (missing this causes tracing errors)")

# Initialize OpenAI-compatible client (e.g., Groq, Gemini, etc.)
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="BASE_URL"
)

# Configure the model wrapper
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="MODEL_NAME"
)

# Set up run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
)

# Create the agent
agent = Agent(
    name="AGENT_NAME",
    instructions="INSTRUCTIONS"
)
```

## Advanced Features (Hooks, Guardrails, etc.)

For advanced requirements like **Hooks**, **Guardrails**, or **Runner Hooks**, use the **context7 mcp server** (or `claude-code-guide` agent) to fetch the latest implementation details from the official OpenAI Agents SDK documentation.

Examples of what to ask after generation:
- "Add a file-saving hook to this agent"
- "Add an input guardrail to check for PII"
- "Add a tool to this agent using @function_tool"
