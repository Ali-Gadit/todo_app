---
name: ChatKit Python Server
description: ChatKit Python server library for building production-ready chat backends with streaming support. Use when building Python/FastAPI backends that need (1) chat API endpoints, (2) streaming response handling, (3) ChatKitServer integration, (4) agent response management, (5) conversation state management, (6) tool execution coordination, or (7) real-time chat streaming. Provides ChatKitServer class, streaming patterns, async support, and agent integration with OpenAI Agents SDK.
---

# ChatKit Python Server

OpenAI's ChatKit Python library for building production-ready chat server backends with streaming responses, agent integration, and conversation management.

## Quick Start

### Installation

```bash
pip install chatkit openai
```

### Basic Setup

```python
from fastapi import FastAPI, WebSocket
from chatkit.server import ChatKitServer
from chatkit.store import MemoryStore
from agents import Agent, function_tool, Runner

app = FastAPI()

@function_tool
def example_tool(query: str) -> str:
    """Example tool for agent."""
    return f"Result for: {query}"

agent = Agent(
    model="gpt-4",
    instructions="You are a helpful assistant.",
    tools=[example_tool],
)

class MyServer(ChatKitServer):
    def __init__(self):
        super().__init__(store=MemoryStore())
        self.agent = agent

@app.websocket("/ws/chat/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    server = MyServer()
    await server.handle_websocket(websocket, thread_id)
```

## Core Components

### ChatKitServer

Base class for handling chat requests and streaming responses.

```python
from chatkit.server import ChatKitServer
from chatkit.store import MemoryStore

class ChatServer(ChatKitServer):
    def __init__(self, agent):
        super().__init__(store=MemoryStore())
        self.agent = agent

    async def respond(self, thread, item, context):
        """Process message and stream response."""
        agent_input = await self._to_agent_input(thread, item)
        if agent_input is None:
            return

        result = Runner.run_streamed(self.agent, agent_input)
        async for event in stream_agent_response(agent_context, result):
            yield event
```

### Thread Management

Handle conversation threads and message history:

```python
# Get or create thread
thread = await server.get_or_create_thread(thread_id)

# Access messages
messages = await thread.get_messages()

# Add message
thread.add_message("user", "Hello")

# Thread metadata
thread.id          # Thread ID
thread.created_at  # Creation timestamp
thread.messages    # Message list
```

### Store Interface

Persist conversation data:

```python
from chatkit.store import Store

class CustomStore(Store):
    async def store_message(self, thread_id: str, message: dict):
        """Store message in database."""
        pass

    async def get_thread_messages(self, thread_id: str) -> list:
        """Retrieve conversation history."""
        pass
```

## Streaming Responses

### Token-by-Token Streaming

Stream individual text tokens:

```python
from openai.types.responses import ResponseTextDeltaEvent
from agents import Runner

async def stream_tokens(agent, user_input):
    result = Runner.run_streamed(agent, user_input)

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                yield {
                    "type": "text_delta",
                    "delta": event.data.delta
                }
```

### Streaming with Tool Calls

Include tool execution events:

```python
async def stream_with_tools(agent, user_input):
    result = Runner.run_streamed(agent, user_input)

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                yield {
                    "type": "text_delta",
                    "delta": event.data.delta
                }

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                yield {
                    "type": "tool_call",
                    "tool_name": event.item.name,
                    "arguments": event.item.arguments
                }
            elif event.item.type == "tool_call_output_item":
                yield {
                    "type": "tool_output",
                    "output": event.item.output
                }
            elif event.item.type == "message_output_item":
                yield {
                    "type": "message_complete",
                    "text": event.item.text
                }
```

### Higher-Level Events

Stream at item completion level:

```python
from agents import ItemHelpers

async def stream_items(agent, user_input):
    result = Runner.run_streamed(agent, user_input)

    async for event in result.stream_events():
        # Skip raw token events
        if event.type == "raw_response_event":
            continue

        # Agent updates
        elif event.type == "agent_updated_stream_event":
            yield {
                "type": "agent_updated",
                "agent_name": event.new_agent.name
            }

        # Item completion events
        elif event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                text = ItemHelpers.text_message_output(event.item)
                yield {
                    "type": "message",
                    "text": text
                }
```

## Agent Integration

### Define Tools

```python
from agents import function_tool
import json

@function_tool
def search_database(query: str) -> str:
    """Search knowledge base."""
    results = db.search(query)
    return json.dumps(results)

@function_tool
def save_note(note: str) -> str:
    """Save note to database."""
    db.save(note)
    return "Note saved"

@function_tool
def get_user_info(user_id: str) -> str:
    """Get user information."""
    user = db.get_user(user_id)
    return json.dumps(user.to_dict())
```

### Create Agent

```python
from agents import Agent

agent = Agent(
    model="gpt-4",
    name="Support Assistant",
    instructions="""You are a helpful support assistant.
    Use tools to help users:
    - Search knowledge base for information
    - Save notes about conversations
    - Retrieve user information when needed
    """,
    tools=[
        search_database,
        save_note,
        get_user_info,
    ],
)
```

## FastAPI Integration

### WebSocket Endpoint

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

@app.websocket("/ws/chat/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    await websocket.accept()
    logger.info(f"WebSocket connected: {thread_id}")

    server = ChatServer(agent)
    thread = await server.get_or_create_thread(thread_id)

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            user_input = data.get("message", "")

            if not user_input:
                await websocket.send_json({
                    "type": "error",
                    "message": "Message required"
                })
                continue

            # Stream response
            try:
                async for event in server.respond(thread, user_input, {}):
                    await websocket.send_json(event)
            except Exception as e:
                logger.error(f"Error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Processing failed"
                })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {thread_id}")
```

### REST Streaming Endpoint

```python
from fastapi.responses import StreamingResponse
import json

@app.post("/chat/stream")
async def chat_stream(request: dict):
    thread_id = request.get("thread_id", "default")
    user_input = request.get("message", "")

    if not user_input:
        return {"error": "Message required"}

    server = ChatServer(agent)
    thread = await server.get_or_create_thread(thread_id)

    async def generate():
        try:
            async for event in server.respond(thread, user_input, {}):
                yield json.dumps(event) + "\n"
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield json.dumps({
                "type": "error",
                "message": "Stream failed"
            }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )
```

## Error Handling

```python
import logging

logger = logging.getLogger(__name__)

async def safe_respond(server, thread, user_input):
    try:
        async for event in server.respond(thread, user_input, {}):
            yield event

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        yield {
            "type": "error",
            "code": "validation_error",
            "message": "Invalid input"
        }

    except TimeoutError as e:
        logger.error(f"Timeout: {e}")
        yield {
            "type": "error",
            "code": "timeout_error",
            "message": "Request timed out"
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        yield {
            "type": "error",
            "code": "server_error",
            "message": "Unexpected error occurred"
        }
```

## Database Integration

### PostgreSQL Store

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from chatkit.store import Store

class PostgresStore(Store):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    async def store_message(self, thread_id: str, message: dict):
        """Store message in PostgreSQL."""
        with Session(self.engine) as session:
            db_message = Message(
                thread_id=thread_id,
                role=message["role"],
                content=message["content"]
            )
            session.add(db_message)
            session.commit()

    async def get_thread_messages(self, thread_id: str) -> list:
        """Retrieve messages from database."""
        with Session(self.engine) as session:
            messages = session.query(Message).filter(
                Message.thread_id == thread_id
            ).all()
            return [msg.to_dict() for msg in messages]

# Use in server
server = ChatServer(agent)
server.store = PostgresStore("postgresql://user:pass@localhost/chatdb")
```

## Complete Server Example

Production-ready FastAPI server:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from chatkit.server import ChatKitServer
from chatkit.store import MemoryStore
from agents import Agent, function_tool, Runner
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ChatKit Server",
    description="Chat API with streaming responses",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define tools
@function_tool
def search_knowledge_base(query: str) -> str:
    """Search knowledge base."""
    logger.info(f"Searching: {query}")
    return json.dumps({"results": []})

# Create agent
agent = Agent(
    model="gpt-4",
    name="Assistant",
    instructions="You are a helpful assistant.",
    tools=[search_knowledge_base],
)

# Create server
class MyServer(ChatKitServer):
    def __init__(self):
        super().__init__(store=MemoryStore())
        self.agent = agent

    async def respond(self, thread, item, context):
        agent_input = await self._to_agent_input(thread, item)
        if agent_input is None:
            return

        result = Runner.run_streamed(self.agent, agent_input)
        async for event in result.stream_events():
            yield event

server = MyServer()

# Endpoints
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat/stream")
async def chat_stream(request: dict):
    thread_id = request.get("thread_id", "default")
    message = request.get("message", "")

    if not message:
        raise HTTPException(status_code=400, detail="Message required")

    thread = await server.get_or_create_thread(thread_id)

    async def generate():
        try:
            async for event in server.respond(thread, message, {}):
                yield json.dumps(event) + "\n"
        except Exception as e:
            logger.error(f"Error: {e}")
            yield json.dumps({"type": "error", "message": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")

@app.websocket("/ws/chat/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    await websocket.accept()
    thread = await server.get_or_create_thread(thread_id)

    try:
        while True:
            data = await websocket.receive_json()
            async for event in server.respond(thread, data["message"], {}):
                await websocket.send_json(event)
    except WebSocketDisconnect:
        logger.info(f"Disconnected: {thread_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Configuration

### Environment Variables

```bash
OPENAI_API_KEY=sk-...
CHATKIT_STORE_TYPE=memory  # or postgres
DATABASE_URL=postgresql://user:pass@localhost/chatdb
LOG_LEVEL=INFO
```

### Development Setup

```bash
# Install dependencies
pip install fastapi uvicorn python-agents chatkit openai

# Run server
python server.py

# Or with uvicorn directly
uvicorn server:app --reload --port 8000
```

## Best Practices

1. **Always handle errors** in respond() method
2. **Use async/await** for all I/O operations
3. **Log extensively** for debugging
4. **Validate user input** before processing
5. **Use environment variables** for secrets
6. **Implement rate limiting** for production
7. **Test streaming responses** thoroughly
8. **Monitor performance** and resource usage

## Troubleshooting

**WebSocket connection refused**: Check FastAPI server is running and CORS is configured

**Agent not responding**: Verify OpenAI API key and model is available

**Streaming stalls**: Check event loop and async/await usage

**Memory leaks**: Ensure threads are properly cleaned up

**Tool not executing**: Verify tool definition and agent instructions

## Performance Tips

1. **Batch stream events** for efficiency
2. **Reuse thread objects** instead of creating new ones
3. **Implement connection pooling** for database
4. **Cache frequently used data**
5. **Monitor token usage** for cost control

## Resources

- GitHub: https://github.com/openai/openai-chatkit-advanced-samples
- OpenAI Agents: https://github.com/openai/openai-agents-python
- FastAPI: https://fastapi.tiangolo.com/
- WebSocket Guide: https://fastapi.tiangolo.com/advanced/websockets/
