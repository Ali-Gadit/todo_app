---
name: mcp-python-sdk
description: Complete guide to build, test, and deploy Model Context Protocol (MCP) Python servers. Covers FastMCP, tools, resources, prompts, sampling, authentication, and production deployment with Streamable HTTP.
---

# MCP Python SDK Skill

This skill provides a comprehensive guide to building Model Context Protocol (MCP) servers in Python using the official MCP Python SDK. MCP enables applications to provide standardized context for LLMs, exposing tools, resources, and prompts.

## Installation

```bash
# Core SDK
pip install mcp

# FastMCP (recommended high-level API)
pip install "mcp[cli]"

# For Streamable HTTP transport
pip install starlette uvicorn
```

## Project Structure

```
mcp_server/
├── server.py              # Main server entry point
├── tools/
│   ├── __init__.py
│   ├── weather.py         # Weather tool
│   └── database.py        # Database tools
├── resources/
│   ├── __init__.py
│   └── config.py          # Resource handlers
├── prompts/
│   ├── __init__.py
│   └── templates.py       # Prompt templates
├── models/
│   ├── __init__.py
│   └── context.py         # Shared context
├── pyproject.toml
└── .env                   # Environment variables
```

## FastMCP Server - Quick Start

```python
# server.py - Basic MCP server with FastMCP
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("My App")

# Define a tool
@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """Get current weather for a city."""
    weather_data = {
        "new york": "Sunny, 22°C",
        "london": "Rainy, 12°C",
        "tokyo": "Clear, 25°C",
    }
    return weather_data.get(city.lower(), f"Weather in {city}: Unknown")

# Define a resource
@mcp.resource("config://settings")
def get_settings() -> str:
    """Expose application settings as a resource."""
    return '{"theme": "dark", "language": "en", "notifications": true}'

# Define a prompt template
@mcp.prompt()
def review_code(code: str) -> str:
    """Generate a code review prompt."""
    return f"""Please review this code for:
- Best practices
- Potential bugs
- Performance issues
- Security concerns

Code:
```
{code}
```"""

# Run the server (defaults to stdio transport)
if __name__ == "__main__":
    mcp.run()
```

## Tools with Context and Logging

```python
# tools/weather.py
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from typing import Optional
import httpx

mcp = FastMCP("Weather Service")

@mcp.tool()
async def get_weather(
    city: str,
    ctx: Context[ServerSession, None],
    unit: str = "celsius"
) -> str:
    """Get weather using external API with logging."""
    await ctx.info(f"Fetching weather for {city}")

    # Make API call (using sampling if needed)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.weather.example.com/{city}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        data = response.json()

    await ctx.debug(f"Weather API response: {data}")

    if unit == "fahrenheit":
        temp_c = data["temp_c"]
        temp_f = (temp_c * 9/5) + 32
        return f"{city}: {temp_f}°F"
    return f"{city}: {data['temp_c']}°C"


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> dict:
    """Perform mathematical operations with structured output."""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    result = operations[operation](a, b)

    return {
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    }
```

## Resources - Data Exposure

```python
# resources/config.py
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

mcp = FastMCP("Config Service")

# Static resource
@mcp.resource("config://app-settings")
def app_settings() -> str:
    """Return application settings."""
    return '{"version": "1.0.0", "debug": false}'

# Dynamic resource with template
@mcp.resource("users://{user_id}/profile")
def user_profile(user_id: str) -> str:
    """Get user profile from database."""
    # In production, fetch from DB
    return f'{{"id": "{user_id}", "name": "User {user_id}", "role": "member"}}'

# List available resources
@mcp.list_resources()
def list_configs() -> list[Resource]:
    """List all available configuration resources."""
    return [
        Resource(
            uri="config://app-settings",
            name="Application Settings",
            description="Main application configuration"
        ),
        Resource(
            uri="config://database",
            name="Database Config",
            description="Database connection settings"
        ),
    ]
```

## Prompts - Reusable Templates

```python
# prompts/templates.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Prompt Service")

@mcp.prompt()
def explain_code(code: str, language: str = "python") -> str:
    """Generate a code explanation prompt."""
    return f"""Explain this {language} code in simple terms:

```{language}
{code}
```

Focus on:
1. What the code does
2. How it works
3. Key concepts used"""


@mcp.prompt()
def generate_tests(code: str) -> str:
    """Generate unit test prompt."""
    return f"""Write comprehensive unit tests for this code:

```{python}
{code}
```

Include tests for:
- Happy path
- Edge cases
- Error conditions
- Use pytest framework"""


@mcp.prompt()
def document_api(endpoint: str, method: str, body: str = "") -> str:
    """Generate API documentation."""
    return f"""Document this API endpoint:

**Endpoint**: {method} {endpoint}
**Request Body**:
```json
{body}
```

Provide:
1. Description
2. Parameters
3. Response format
4. Error codes
5. Example usage"""
```

## Lifespan - Shared Resources

```python
# server.py - With lifespan for shared resources
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from mcp.server.fastmcp import Context, FastMCP
import httpx

@dataclass
class AppContext:
    http_client: httpx.AsyncClient
    database_url: str
    api_key: str

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with shared resources."""
    # Startup
    client = httpx.AsyncClient(timeout=30.0)
    config = {
        "database_url": "postgresql://localhost/mydb",
        "api_key": "secret-key"
    }

    try:
        yield AppContext(http_client=client, **config)
    finally:
        # Shutdown
        await client.aclose()

mcp = FastMCP("My App", lifespan=app_lifespan)

@mcp.tool()
async def query_database(
    query: str,
    ctx: Context
) -> dict:
    """Query the database using shared connection."""
    app_ctx = ctx.request_context.lifespan_context

    # Use shared HTTP client for database API
    response = await app_ctx.http_client.get(
        f"{app_ctx.database_url}/query",
        params={"q": query},
        headers={"Authorization": f"Bearer {app_ctx.api_key}"}
    )

    return response.json()
```

## Sampling - LLM Generation

```python
# tools/sampling.py
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP("Sampling Service")

@mcp.tool()
async def generate_poem(
    topic: str,
    style: str = "haiku",
    ctx: Context[ServerSession, None] = None
) -> str:
    """Generate a poem using LLM sampling."""
    if ctx is None:
        return f"Poem about {topic} in {style} style"

    prompt = f"Write a {style} poem about {topic}"

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        max_tokens=100,
    )

    if result.content.type == "text":
        return result.content.text
    return str(result.content)


@mcp.tool()
async def summarize_text(
    text: str,
    max_length: int = 50,
    ctx: Context[ServerSession, None] = None
) -> str:
    """Summarize text using LLM."""
    prompt = f"Summarize this in {max_length} words or less:\n\n{text}"

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(role="user", content=TextContent(type="text", text=prompt))
        ],
        max_tokens=max_length + 20,
    )

    return result.content.text if result.content.type == "text" else str(result.content)
```

## Authentication - OAuth 2.1

```python
# auth.py - MCP Server with OAuth 2.1 authentication
from pydantic import AnyUrl
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP

class SimpleTokenVerifier(TokenVerifier):
    """Verify access tokens from authorization server."""

    async def verify_token(self, token: str) -> AccessToken | None:
        # Implement actual token validation
        # - Verify signature with AS public key
        # - Check expiration
        # - Validate scopes
        if token == "valid-token":
            return AccessToken(
                token=token,
                scopes=["read", "write"],
                expires_at=None
            )
        return None

# Create protected server
mcp = FastMCP(
    "Protected Service",
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyUrl("https://auth.example.com"),
        resource_server_url=AnyUrl("http://localhost:3001"),
        required_scopes=["user"]
    )
)

@mcp.tool()
def get_private_data() -> dict:
    """Tool requiring authentication."""
    return {"data": "sensitive information"}
```

## Production Deployment - Streamable HTTP

```python
# server.py - Production deployment with Streamable HTTP
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.middleware.cors import CORSMiddleware
import contextlib

# Create stateful server
mcp = FastMCP("Production Service", json_response=True)

@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 22°C"

# Option 1: Run directly with streamable-http
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
    # Server accessible at http://localhost:8000/mcp

# Option 2: Mount to existing Starlette app
mcp_stateless = FastMCP("Stateless Service", stateless_http=True, json_response=True)

@mcp_stateless.tool()
def echo(message: str) -> str:
    return f"Echo: {message}"

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        await stack.enter_async_context(mcp_stateless.session_manager.run())
        yield

app = Starlette(
    routes=[
        Mount("/weather", mcp.streamable_http_app()),
        Mount("/echo", mcp_stateless.streamable_http_app())
    ],
    lifespan=lifespan
)

# Add CORS for browser clients
app = CORSMiddleware(
    app,
    allow_origins=["https://myapp.com"],
    allow_methods=["GET", "POST", "DELETE"],
    expose_headers=["Mcp-Session-Id"]
)

# Run with: uvicorn server:app --host 0.0.0.0 --port 8000
```

## Client Connection

```python
# client.py - Connect to MCP server
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def main():
    # Connect via stdio
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None  # or {"PYTHONPATH": "/path"}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # List resources
            resources = await session.list_resources()
            print(f"Available resources: {[r.uri for r in resources.resources]}")

            # List prompts
            prompts = await session.list_prompts()
            print(f"Available prompts: {[p.name for p in prompts.prompts]}")

            # Call a tool
            result = await session.call_tool("get_weather", {"city": "London"})
            print(f"Weather: {result.content[0].text}")

            # Read a resource
            resource = await session.read_resource("config://settings")
            print(f"Config: {resource.contents[0].text}")

            # Get a prompt
            prompt = await session.get_prompt("review_code", {"code": "print('hello')"})
            print(f"Prompt: {prompt.messages[0].content}")

asyncio.run(main())
```

## HTTP Client Connection

```python
# client_http.py - Connect via Streamable HTTP
import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

async def main():
    async with streamablehttp_client(
        "http://localhost:8000/mcp",
        headers={"Authorization": "Bearer my-token"}
    ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Use tools
            result = await session.call_tool("get_weather", {"city": "Tokyo"})
            print(result.content[0].text)

asyncio.run(main())
```

## pyproject.toml

```toml
[project]
name = "mcp-weather-service"
version = "0.1.0"
description = "MCP server for weather information"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.25.0",
    "starlette>=0.35.0",
    "uvicorn>=0.25.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
target-version = "py310"
```

## Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application
COPY *.py ./

# Run server
CMD ["python", "server.py"]
```

```yaml
# docker-compose.yml
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - API_KEY=${API_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
```

## Validation Checklist

- [ ] Server starts without import errors
- [ ] Tools are discoverable via list_tools
- [ ] Tool calls return expected results
- [ ] Resources are accessible
- [ ] Prompts generate correctly
- [ ] Streamable HTTP transport works
- [ ] CORS is configured properly
- [ ] Authentication blocks unauthorized access (if enabled)
- [ ] Server shuts down gracefully

## Common Errors

| Error | Fix |
|-------|-----|
| ImportError: No module named 'mcp' | Install with `pip install mcp` |
| Connection refused | Check server is running on correct port |
| Tool not found | Verify tool decorator was applied |
| 401 Unauthorized | Check authentication token |
| CORS error | Configure CORSMiddleware allow_origins |

## Related Skills

- `openai-agents-creater` - Connect MCP to OpenAI agents
- `fastapi-sqlmodel` - Build MCP server with FastAPI backend
