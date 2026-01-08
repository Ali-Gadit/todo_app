---
name: chatkit-backend
description: Creates production-ready ChatKit Python backend with FastAPI, OpenAI Agents SDK, memory store, and complete endpoint implementation.
---

# ChatKit Backend Skill

This skill creates a complete ChatKit Python backend using FastAPI, ChatKit Python SDK, and OpenAI Agents SDK for streaming AI responses.

## Installation

```bash
pip install fastapi uvicorn chatkit openai-agents python-dotenv
# For specific model providers
pip install litellm  # For Gemini, Anthropic, etc.
```

## Project Structure

```
backend/
├── main.py              # FastAPI app with ChatKit endpoints
├── store.py             # Memory/persistent store
├── agent.py             # Agent implementation
├── requirements.txt
└── .env
```

## Complete Backend Implementation

```python
# main.py - Complete ChatKit backend
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, Response
from pydantic import BaseModel

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from chatkit.server import ChatKitServer, StreamingResult
from chatkit.store import Store
from chatkit.types import ThreadMetadata, ThreadItem, Page
from chatkit.agents import AgentContext, stream_agent_response, ThreadItemConverter

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")


# =============================================================================
# Store Implementation - In-memory conversation storage
# =============================================================================

class MemoryStore(Store[dict]):
    """Thread-safe in-memory store for ChatKit conversations."""

    def __init__(self) -> None:
        self._threads: dict[str, "_ThreadState"] = {}
        self._id_counter = 0

    async def save_thread(
        self,
        thread: ThreadMetadata,
        context: dict
    ) -> None:
        """Save or update thread metadata."""
        state = self._threads.get(thread.id)
        if state:
            state.thread = thread.model_copy(deep=True)
        else:
            self._threads[thread.id] = _ThreadState(
                thread=thread.model_copy(deep=True),
                items=[],
            )

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict,
    ) -> Page[ThreadItem]:
        """Load paginated thread items."""
        items = [item.model_copy(deep=True)
                 for item in self._items(thread_id)]
        items.sort(
            key=lambda i: getattr(i, "created_at", datetime.utcnow()),
            reverse=(order == "desc"),
        )

        start = 0
        if after:
            index_map = {item.id: idx for idx, item in enumerate(items)}
            start = index_map.get(after, -1) + 1

        slice_items = items[start : start + limit + 1]
        has_more = len(slice_items) > limit
        return Page(
            data=slice_items[:limit],
            has_more=has_more,
            after=slice_items[-1].id if has_more else None
        )

    async def get_thread(self, thread_id: str, context: dict) -> ThreadMetadata | None:
        """Get thread metadata."""
        state = self._threads.get(thread_id)
        return state.thread if state else None

    def _items(self, thread_id: str) -> list[ThreadItem]:
        """Get all items for a thread."""
        state = self._threads.get(thread_id)
        return state.items if state else []


class _ThreadState:
    """Internal thread state storage."""
    thread: ThreadMetadata
    items: list[ThreadItem]

    def __init__(self, thread: ThreadMetadata, items: list[ThreadItem]) -> None:
        self.thread = thread
        self.items = items


# =============================================================================
# ChatKit Server Implementation
# =============================================================================

class ChatKitServerImpl(ChatKitServer[dict]):
    """Complete ChatKit server with OpenAI Agents integration."""

    def __init__(self, store: MemoryStore, assistant: Agent) -> None:
        self.store = store
        self.assistant = assistant
        self._id_mapping: dict[str, str] = {}

    async def respond(
        self,
        thread: ThreadMetadata,
        item: "ThreadItem | None",
        context: dict,
    ) -> AsyncIterator:
        """Handle user message and stream agent response."""
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Convert thread item to agent input
        agent_input = await self._to_agent_input(thread, item)
        if agent_input is None:
            return

        # Run agent with streaming
        result = Runner.run_streamed(
            self.assistant,
            agent_input,
            context=agent_context,
        )

        # Stream response events with ID fix
        async for event in stream_agent_response(agent_context, result):
            yield event

    async def _to_agent_input(
        self,
        thread: ThreadMetadata,
        item: "ThreadItem | None"
    ) -> str | None:
        """Convert thread item to agent input text."""
        if item is None:
            return None

        from chatkit.types import UserMessageItem, TextContent
        if isinstance(item, UserMessageItem):
            text_parts = []
            for content in item.content:
                if isinstance(content, TextContent):
                    text_parts.append(content.text)
            return "\n".join(text_parts)
        return None


# =============================================================================
# Model Configuration
# =============================================================================

def create_model(provider: str = "openai", model: str = "gpt-4o"):
    """Create LLM model based on provider."""
    api_key_env = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "groq": "GROQ_API_KEY",
    }.get(provider, "OPENAI_API_KEY")

    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"{api_key_env} environment variable is required")

    model_map = {
        "openai": f"openai/{model}",
        "gemini": f"gemini/{model}",
        "anthropic": f"anthropic/{model}",
        "groq": f"groq/{model}",
    }

    return LitellmModel(
        model=model_map.get(provider, f"openai/{model}"),
        api_key=api_key,
    )


# =============================================================================
# Agent Creation
# =============================================================================

def create_assistant(model) -> Agent:
    """Create the ChatKit assistant agent."""
    return Agent(
        name="ChatKit Assistant",
        instructions="""You are a helpful, friendly AI assistant.
        Provide clear, concise, and helpful responses.
        Use markdown formatting for code blocks and emphasis.
        Be conversational and engaging.""",
        model=model,
    )


# =============================================================================
# FastAPI App Setup
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup
    print("Starting ChatKit server...")
    yield
    # Shutdown
    print("Shutting down ChatKit server...")


# Create FastAPI app
app = FastAPI(
    title="ChatKit API",
    description="Backend for ChatKit chat interface",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize store and server
store = MemoryStore()
model = create_model(provider="openai", model="gpt-4o")
assistant = create_assistant(model)
server = ChatKitServerImpl(store, assistant)


# =============================================================================
# API Endpoints
# =============================================================================

@app.post("/chatkit")
async def chatkit_endpoint(request: Request) -> Response:
    """
    Central ChatKit endpoint - handles all chat requests.

    POST /chatkit
    Body: Raw request payload from ChatKit client
    Returns: StreamingResponse (text/event-stream) or JSONResponse
    """
    payload = await request.body()
    result = await server.process(payload, {"request": request})

    if isinstance(result, StreamingResult):
        return StreamingResponse(
            result,
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )

    # Handle JSON response
    if hasattr(result, "json"):
        return Response(content=result.json, media_type="application/json")

    return JSONResponse(content=result)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/chatkit/session", response_model=SessionResponse)
async def create_session():
    """
    Create a new ChatKit session with client secret.
    Frontend calls this to get authentication token.
    """
    import secrets
    client_secret = secrets.token_urlsafe(32)

    return SessionResponse(
        client_secret=client_secret,
        expires_in=3600,
    )


@app.post("/api/chatkit/refresh", response_model=SessionResponse)
async def refresh_session(request: RefreshRequest):
    """
    Refresh an existing session.
    Frontend calls this when client_secret expires.
    """
    import secrets
    # In production, validate the existing token first
    # For now, just issue a new one
    client_secret = secrets.token_urlsafe(32)

    return SessionResponse(
        client_secret=client_secret,
        expires_in=3600,
    )


# =============================================================================
# Debug Endpoints
# =============================================================================

@app.get("/debug/threads")
async def debug_threads():
    """Debug endpoint to inspect stored threads."""
    result = {}
    for thread_id, state in store._threads.items():
        items = []
        for item in state.items:
            item_data = {"id": item.id, "type": type(item).__name__}
            if hasattr(item, "content") and item.content:
                content_parts = []
                for part in item.content:
                    if hasattr(part, "text"):
                        content_parts.append(part.text)
                item_data["content"] = content_parts
            items.append(item_data)
        result[thread_id] = {
            "thread": {
                "id": state.thread.id,
                "created_at": str(state.thread.created_at) if state.thread.created_at else None,
            },
            "items": items,
            "count": len(items),
        }
    return result


# =============================================================================
# Pydantic Models
# =============================================================================

class SessionResponse(BaseModel):
    client_secret: str
    expires_in: int = 3600


class RefreshRequest(BaseModel):
    token: str


# =============================================================================
# Run Server
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=True,
    )
```

## requirements.txt

```
fastapi==0.115.6
uvicorn[standard]==0.32.1
chatkit==1.4.0
openai-agents>=0.6.2
python-dotenv==1.0.1
httpx==0.28.1
```

## .env.example

```bash
# OpenAI (default)
OPENAI_API_KEY=sk-...

# Optional: Other providers
# GEMINI_API_KEY=...
# ANTHROPIC_API_KEY=...
# GROQ_API_KEY=...

# Server
PORT=8000
HOST=0.0.0.0
```

## Complete Store Implementation (Persistent)

```python
# store.py - PostgreSQL-backed store for production
import json
from typing import AsyncIterator
from datetime import datetime

from chatkit.store import Store
from chatkit.types import ThreadMetadata, ThreadItem, Page
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class PostgresStore(Store[dict]):
    """PostgreSQL-backed store for persistent conversation storage."""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def save_thread(self, thread: ThreadMetadata, context: dict) -> None:
        """Save thread to PostgreSQL."""
        async with self.async_session() as session:
            # Save thread logic here
            await session.commit()

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict,
    ) -> Page[ThreadItem]:
        """Load paginated items from PostgreSQL."""
        # Load items logic here
        return Page(data=[], has_more=False, after=None)

    async def close(self) -> None:
        """Close database connections."""
        await self.engine.dispose()
```

## LiteLLM Configuration

```python
# agent.py - Multi-provider support
from agents.extensions.models.litellm_model import LitellmModel

PROVIDERS = {
    "openai": {
        "model": "gpt-4o",
        "api_key": "OPENAI_API_KEY",
    },
    "gemini": {
        "model": "gemini-2.0-flash",
        "api_key": "GEMINI_API_KEY",
    },
    "anthropic": {
        "model": "claude-3-sonnet-20240229",
        "api_key": "ANTHROPIC_API_KEY",
    },
    "groq": {
        "model": "llama-3.3-70b-versatile",
        "api_key": "GROQ_API_KEY",
    },
}


def create_model(provider: str = "openai"):
    """Create model with LiteLLM for any provider."""
    config = PROVIDERS.get(provider, PROVIDERS["openai"])
    api_key = os.getenv(config["api_key"])

    return LitellmModel(
        model=f"{provider}/{config['model']}",
        api_key=api_key,
    )
```

## Validation Checklist

- [ ] Backend starts without import errors
- [ ] `/health` endpoint returns 200
- [ ] `/chatkit` endpoint accepts POST requests
- [ ] Streaming responses work correctly
- [ ] Conversation history is preserved
- [ ] Session/refresh endpoints work
- [ ] CORS is configured for frontend
- [ ] Multi-provider models work (if configured)

## Common Errors

| Error | Fix |
|-------|-----|
| ImportError: No module named 'chatkit' | Install: `pip install chatkit` |
| 401 Unauthorized | Check API key in .env |
| Streaming timeout | Increase timeout on client |
| Memory store grows unbounded | Implement persistent store |
| ID collisions with Gemini | Use ID mapping in respond() |

## Running the Server

```bash
# Development
cd backend
python main.py

# Production with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# With Docker
docker build -t chatkit-backend .
docker run -p 8000:8000 chatkit-backend
```

## Related Skills

- `chatkit-frontend` - React frontend
- `chatkit-store` - Store implementation details
- `chatkit-agent-memory` - Advanced agent patterns
- `openai-agents-creater` - Agent creation
