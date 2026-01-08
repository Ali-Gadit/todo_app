---
name: openai-agents-creater
description: Generates Python agents using the OpenAI Agents SDK with custom model providers, MCP server integration, handoffs, guardrails, and tracing. Supports Groq, Gemini, and other OpenAI-compatible APIs.
---

# OpenAI Agents Creator Skill

This Skill generates Python agent code using the OpenAI Agents SDK with support for custom model providers, MCP server integration, multi-agent workflows, and production features.

## Installation

```bash
pip install "openai-agents[ Agents]==0.2.9"  # Check latest version
```

## Basic Agent with Custom Model Provider

```python
# agent.py - Basic agent with custom provider (Groq, Gemini, etc.)
from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel
from agents.models import ModelSettings
from openai import AsyncOpenAI
from dotenv import load_dotenv 
import os

# Critical: Load .env before accessing API keys
load_dotenv()

# Configuration
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

# Initialize OpenAI-compatible client
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Configure the model
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="llama-3.3-70b-versatile"
)

# Set up run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
)

# Create the agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be concise and clear.",
)

# Run the agent
import asyncio

async def main():
    result = await Runner.run(agent, "What is the capital of France?")
    print(result.final_output)

asyncio.run(main())
```

## MCP Server Integration - Stdio Connection

Connect an agent to an MCP server using stdio transport for filesystem access, database queries, or any MCP tools.

```python
# agent_mcp_stdio.py - Connect agent to MCP server via stdio
import asyncio
import os
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from agents.tracing import trace, gen_trace_id

async def main():
    current_dir = Path(__file__).parent.resolve()
    samples_dir = current_dir / "sample_files"

    # Connect to MCP server via stdio
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)]
        }
    ) as server:
        # Create agent with MCP server access
        agent = Agent(
            name="File Assistant",
            instructions="Use the filesystem tools to read files and answer questions.",
            mcp_servers=[server]
        )

        # Enable tracing
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Filesystem Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")

            # List files
            result = await Runner.run(agent, "Read the files and list them.")
            print(result.final_output)

            # Ask about content
            result = await Runner.run(agent, "What is my #1 favorite book?")
            print(result.final_output)

            # Get recommendations
            result = await Runner.run(
                agent,
                "Look at my favorite songs. Suggest one new song I might like."
            )
            print(result.final_output)

asyncio.run(main())
```

## MCP Server Integration - Streamable HTTP

For production deployments, connect agents to MCP servers via HTTP transport.

```python
# agent_mcp_http.py - Connect agent to MCP server via HTTP
import asyncio
import os
from agents import Agent, Runner
from agents.models import ModelSettings
from agents.mcp import MCPServerStreamableHttp

async def main():
    token = os.environ.get("MCP_SERVER_TOKEN", "")

    async with MCPServerStreamableHttp(
        name="API Server",
        params={
            "url": "http://localhost:8000/mcp",
            "headers": {"Authorization": f"Bearer {token}"},
            "timeout": 30,
        },
        cache_tools_list=True,  # Cache tools for performance
        max_retry_attempts=3,
    ) as server:
        agent = Agent(
            name="API Assistant",
            instructions="Use the MCP tools to interact with the API.",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="required"),
        )

        result = await Runner.run(agent, "Get the user profile for user 123")
        print(result.final_output)

asyncio.run(main())
```

## MCP Server Integration - SSE (Server-Sent Events)

For real-time streaming connections, use SSE transport.

```python
# agent_mcp_sse.py - Connect agent via SSE
import asyncio
from agents import Agent, Runner
from agents.models import ModelSettings
from agents.mcp import MCPServerSse

async def main():
    workspace_id = "demo-workspace"

    async with MCPServerSse(
        name="Realtime Server",
        params={
            "url": "http://localhost:8000/sse",
            "headers": {"X-Workspace": workspace_id},
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="Realtime Assistant",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="required"),
        )

        result = await Runner.run(agent, "Subscribe to updates and report back")
        print(result.final_output)

asyncio.run(main())
```

## Hosted MCP (OpenAI Infrastructure)

Use OpenAI's hosted MCP servers for trusted third-party services.

```python
# agent_hosted_mcp.py - Use OpenAI's hosted MCP infrastructure
import asyncio
from agents import Agent, Runner
from agents.mcp import HostedMCPTool

async def main():
    # Use hosted MCP server via OpenAI Responses API
    agent = Agent(
        name="Git Assistant",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "gitmcp",
                    "server_url": "https://gitmcp.io/openai/codex",
                    "require_approval": "never"  # Only for trusted servers
                }
            )
        ]
    )

    result = await Runner.run(
        agent,
        "Which language is this repository written in? Show me the file structure."
    )
    print(result.final_output)

asyncio.run(main())
```

## Multi-Agent Workflow with Handoffs

Create agents that can delegate to specialized agents.

```python
# agent_handoffs.py - Multi-agent with handoffs
from agents import Agent, Runner
from pydantic import BaseModel
import asyncio


class CodingOutput(BaseModel):
    code: str
    language: str
    explanation: str


class ReviewOutput(BaseModel):
    issues: list[str]
    suggestions: list[str]
    score: int


# Specialized coding agent
coding_agent = Agent(
    name="Coding Agent",
    handoff_description="Expert programmer for any coding task",
    instructions="""You are an expert programmer. Write clean, efficient code.
    Always explain your solution and provide working examples.""",
    output_type=CodingOutput,
)

# Specialized review agent
review_agent = Agent(
    name="Code Reviewer",
    handoff_description="Thorough code reviewer",
    instructions="""You review code for bugs, performance issues, and best practices.
    Provide detailed feedback with specific suggestions.""",
    output_type=ReviewOutput,
)

# Triage agent with handoffs
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You coordinate between coding and review tasks.
    Route coding requests to the Coding Agent and review requests to the Reviewer.""",
    handoffs=[coding_agent, review_agent],
)


async def main():
    # Coding task
    result = await Runner.run(
        triage_agent,
        "Write a Python function to calculate Fibonacci numbers efficiently."
    )
    print(result.final_output)

    # Review task
    result = await Runner.run(
        triage_agent,
        "Review this code: def add(a,b): return a+b"
    )
    print(result.final_output)

asyncio.run(main())
```

## Input Guardrails

Validate user inputs before processing.

```python
# agent_guardrails.py - Input validation with guardrails
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio


class HomeworkCheck(BaseModel):
    is_homework: bool
    subject: str
    confidence: float


# Guardrail agent
guardrail_agent = Agent(
    name="Homework Detector",
    instructions="Determine if the user is asking about homework.",
    output_type=HomeworkCheck,
)


async def homework_guardrail(ctx, agent, input_data):
    """Check if input is homework-related."""
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    output = result.final_output_as(HomeworkCheck)

    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=not output.is_homework,  # Block if NOT homework
    )


# Main agent with guardrail
tutor_agent = Agent(
    name="Tutor",
    instructions="You are a helpful tutor.",
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)


async def main():
    # This should pass (homework question)
    result = await Runner.run(
        tutor_agent,
        "Can you explain how derivatives work in calculus?"
    )
    print(result.final_output)

    # This should be blocked (non-homework)
    try:
        result = await Runner.run(
            tutor_agent,
            "What's for dinner?"
        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail blocked: Non-homework question")

asyncio.run(main())
```

## Output Guardrails

Validate agent outputs before returning.

```python
# agent_output_guardrail.py - Output validation
from agents import Agent, OutputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import re
import asyncio


class SafetyCheck(BaseModel):
    is_safe: bool
    reason: str


safety_agent = Agent(
    name="Safety Checker",
    instructions="Check if content is safe for work.",
    output_type=SafetyCheck,
)


async def safety_guardrail(ctx, agent, input_data, output_data):
    """Validate output is safe."""
    result = await Runner.run(
        safety_agent,
        f"Input: {input_data}\n\nOutput: {output_data}\n\nIs this safe?"
    )
    output = result.final_output_as(SafetyCheck)

    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=not output.is_safe,
    )


safe_agent = Agent(
    name="Safe Assistant",
    instructions="You are a helpful assistant.",
    output_guardrails=[
        OutputGuardrail(guardrail_function=safety_guardrail),
    ],
)


async def main():
    result = await Runner.run(safe_agent, "Tell me a joke about cats")
    print(result.final_output)

asyncio.run(main())
```

## Complete Multi-Agent Workflow Example

```python
# agent_complete.py - Complete workflow with handoffs and guardrails
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio


# --- Data Models ---
class MathOutput(BaseModel):
    solution: str
    steps: list[str]
    answer: float


class HistoryOutput(BaseModel):
    event: str
    year: int
    significance: str


class RoutingDecision(BaseModel):
    should_route: bool
    agent: str
    reason: str


# --- Specialized Agents ---
math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist for math problems",
    instructions="""You provide help with math problems.
    Explain your reasoning at each step and include examples.""",
    output_type=MathOutput,
)

history_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist for historical questions",
    instructions="""You provide assistance with historical queries.
    Explain important events and their context clearly.""",
    output_type=HistoryOutput,
)


# --- Guardrail ---
routing_agent = Agent(
    name="Router",
    instructions="Determine if this is a math or history question.",
    output_type=RoutingDecision,
)


async def routing_guardrail(ctx, agent, input_data):
    result = await Runner.run(routing_agent, input_data, context=ctx.context)
    decision = result.final_output_as(RoutingDecision)

    return GuardrailFunctionOutput(
        output_info=decision,
        tripwire_triggered=not decision.should_route,
    )


# --- Main Triage Agent ---
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route questions to the appropriate specialist.",
    handoffs=[history_agent, math_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=routing_guardrail),
    ],
)


# --- Execution ---
async def main():
    # Math question
    try:
        result = await Runner.run(
            triage_agent,
            "If a train travels 60 miles in 1.5 hours, what is its average speed?"
        )
        print(f"Math Answer: {result.final_output}")
    except InputGuardrailTripwireTriggered:
        print("Could not route math question")

    # History question
    try:
        result = await Runner.run(
            triage_agent,
            "What was the significance of the Magna Carta?"
        )
        print(f"History Answer: {result.final_output}")
    except InputGuardrailTripwireTriggered:
        print("Could not route history question")

    # Non-routable question
    try:
        result = await Runner.run(
            triage_agent,
            "What is the best pizza topping?"
        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Question blocked: Cannot route to specialist")


if __name__ == "__main__":
    asyncio.run(main())
```

## Tracing and Debugging

```python
# agent_tracing.py - Enable tracing for debugging
import asyncio
from agents import Agent, Runner
from agents.tracing import trace, set_tracing_export_api_key, gen_trace_id

# Set up tracing (get API key from platform.openai.com)
set_tracing_export_api_key("sk-...")

agent = Agent(name="Assistant", instructions="You are helpful.")

async def main():
    trace_id = gen_trace_id()

    with trace(
        workflow_name="My Agent Workflow",
        trace_id=trace_id,
        tags=["production", "v1.0"]
    ):
        result = await Runner.run(agent, "Hello, world!")
        print(result.final_output)

    print(f"Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

asyncio.run(main())
```

## Model Settings

```python
# agent_model_settings.py - Configure model behavior
from agents import Agent, Runner
from agents.models import ModelSettings
import asyncio

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(
        tool_choice="required",  # "auto", "required", or "none"
        max_tokens=4096,
        temperature=0.7,
        top_p=0.95,
    ),
)

async def main():
    result = await Runner.run(agent, "Explain quantum computing")
    print(result.final_output)

asyncio.run(main())
```

## pyproject.toml

```toml
[project]
name = "my-agents"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "openai-agents>=0.2.9",
    "python-dotenv>=1.0.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

## Validation Checklist

- [ ] Agent creates without errors
- [ ] Agent responds to prompts correctly
- [ ] MCP tools are available when connected
- [ ] Handoffs work between agents
- [ ] Guardrails block inappropriate inputs
- [ ] Tracing captures workflow
- [ ] Custom model provider works (if configured)

## Common Errors

| Error | Fix |
|-------|-----|
| ImportError: No module named 'agents' | Install: `pip install openai-agents` |
| 401 Unauthorized | Check API key in environment |
| MCP connection refused | Verify MCP server is running |
| Handoff failed | Check handoff descriptions are set |
| Guardrail triggered unexpectedly | Tune guardrail agent instructions |

## Related Skills

- `mcp-python-sdk` - Build MCP servers to connect to agents
- `fastapi-sqlmodel` - Backend for MCP servers
