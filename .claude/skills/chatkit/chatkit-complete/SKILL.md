---
name: chatkit-complete
description: Complete ChatKit integration from zero to running - connects React frontend to FastAPI backend with OpenAI Agents SDK for streaming AI chat.
---

# ChatKit Complete Integration Skill

This skill creates a production-ready ChatKit chat system combining frontend, backend, agent, and storage into a complete streaming AI chat application.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React + Vite)                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  index.html - CDN script for ChatKit                     │   │
│  │  src/App.tsx - useChatKit hook + Chat component         │   │
│  │  src/main.tsx - React entry point                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                    POST /chatkit (SSE)                          │
│                              │                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /chatkit - Main streaming endpoint                 │   │
│  │  GET  /health - Health check                             │   │
│  │  GET  /api/chatkit/session - Create session              │   │
│  │  POST /api/chatkit/refresh - Refresh session             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│              ┌───────────────┴───────────────┐                  │
│              ▼                               ▼                  │
│  ┌─────────────────────┐       ┌─────────────────────┐          │
│  │  ChatKitServerImpl  │       │    MemoryStore      │          │
│  │  (agent + streaming)│       │  (conversation      │          │
│  │                     │       │   persistence)      │          │
│  └─────────────────────┘       └─────────────────────┘          │
│                              │                                   │
│                              ▼                                  │
│              ┌─────────────────────────────────┐                │
│              │  OpenAI Agents SDK + LiteLLM    │                │
│              │  (gpt-4o, gemini, anthropic...) │                │
│              └─────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
chatkit-app/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       └── components/
│           └── Chat.tsx
├── backend/
│   ├── main.py
│   ├── store.py
│   ├── agent.py
│   ├── requirements.txt
│   └── .env
└── docker-compose.yml
```

## Frontend Implementation

### index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ChatKit AI Chat</title>
    <!-- CRITICAL: CDN script for ChatKit -->
    <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #root { height: 100%; width: 100%; }
      body {
        font-family: 'Inter', system-ui, sans-serif;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### src/App.tsx

```tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useState, useEffect } from 'react';

export default function App() {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('chatkit-thread-id');
    setThreadId(saved);
    setIsReady(true);
  }, []);

  const { control } = useChatKit({
    api: {
      url: 'http://localhost:8000/chatkit',
      // Production: use getClientSecret for auth
      async getClientSecret(existing?: string) {
        const res = await fetch('http://localhost:8000/api/chatkit/session', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        const data = await res.json();
        return data.client_secret;
      },
    },
    initialThread: threadId,
    theme: {
      colorScheme: 'dark',
      color: {
        accent: { primary: '#4cc9f0', level: 1 },
        grayscale: { hue: 220, tint: 6, shade: -1 },
      },
      radius: 'round',
    },
    startScreen: {
      greeting: 'Hello! I am your AI assistant. How can I help?',
      prompts: [
        { label: 'Help', prompt: 'What can you help me with?' },
        { label: 'Code', prompt: 'Help me write Python code' },
        { label: 'Explain', prompt: 'Explain quantum computing' },
      ],
    },
    onThreadChange: ({ threadId }) => {
      if (threadId) {
        localStorage.setItem('chatkit-thread-id', threadId);
      } else {
        localStorage.removeItem('chatkit-thread-id');
      }
    },
    onError: ({ error }) => console.error('ChatKit error:', error),
  });

  if (!isReady) {
    return (
      <div style={{
        height: '100vh', display: 'flex', alignItems: 'center',
        justifyContent: 'center', color: '#4cc9f0',
      }}>
        Loading ChatKit...
      </div>
    );
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{
        padding: '1rem 2rem', background: '#16213e',
        borderBottom: '1px solid #0f3460',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      }}>
        <h1 style={{ color: '#4cc9f0', fontSize: '1.5rem' }}>AI Chat</h1>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={() => {
              localStorage.removeItem('chatkit-thread-id');
              setThreadId(null);
            }}
            style={{
              padding: '0.5rem 1rem', background: '#4361ee',
              color: 'white', border: 'none', borderRadius: '0.5rem',
              cursor: 'pointer',
            }}
          >
            New Chat
          </button>
        </div>
      </header>
      <main style={{ flex: 1, overflow: 'hidden' }}>
        <ChatKit control={control} className="h-full w-full" />
      </main>
    </div>
  );
}
```

### src/main.tsx

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

### package.json

```json
{
  "name": "chatkit-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@openai/chatkit-react": "^1.3.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.7.2",
    "vite": "^6.0.3"
  }
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
});
```

## Backend Implementation

### backend/main.py

```python
import os
import secrets
from pathlib import Path
from datetime import datetime
from typing import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response, JSONResponse
from pydantic import BaseModel

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from chatkit.server import ChatKitServer, StreamingResult
from chatkit.store import Store
from chatkit.types import ThreadMetadata, ThreadItem, Page
from chatkit.agents import AgentContext, stream_agent_response

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")


# =============================================================================
# Store - In-memory conversation storage
# =============================================================================

class MemoryStore(Store[dict]):
    def __init__(self):
        self._threads: dict[str, "_ThreadState"] = {}

    async def save_thread(self, thread: ThreadMetadata, context: dict):
        state = self._threads.get(thread.id)
        if state:
            state.thread = thread.model_copy(deep=True)
        else:
            self._threads[thread.id] = _ThreadState(
                thread=thread.model_copy(deep=True),
                items=[],
            )

    async def load_thread_items(self, thread_id, after, limit, order, context):
        items = [item.model_copy(deep=True) for item in self._items(thread_id)]
        items.sort(key=lambda i: getattr(i, "created_at", datetime.utcnow()),
                   reverse=(order == "desc"))

        start = 0
        if after:
            index_map = {item.id: idx for idx, item in enumerate(items)}
            start = index_map.get(after, -1) + 1

        slice_items = items[start:start + limit + 1]
        has_more = len(slice_items) > limit
        return Page(data=slice_items[:limit], has_more=has_more,
                    after=slice_items[-1].id if has_more else None)

    def _items(self, thread_id):
        state = self._threads.get(thread_id)
        return state.items if state else []


class _ThreadState:
    def __init__(self, thread: ThreadMetadata, items: list[ThreadItem]):
        self.thread = thread
        self.items = items


# =============================================================================
# ChatKit Server
# =============================================================================

class ChatKitServerImpl(ChatKitServer[dict]):
    def __init__(self, store: MemoryStore, assistant: Agent):
        self.store = store
        self.assistant = assistant

    async def respond(self, thread, item, context) -> AsyncIterator:
        agent_context = AgentContext(thread=thread, store=self.store,
                                      request_context=context)

        # Convert message to agent input
        from chatkit.types import UserMessageItem, TextContent
        if isinstance(item, UserMessageItem):
            text_parts = [c.text for c in item.content if isinstance(c, TextContent)]
            agent_input = "\n".join(text_parts)
        else:
            return

        # Stream agent response
        result = Runner.run_streamed(self.assistant, agent_input,
                                     context=agent_context)
        async for event in stream_agent_response(agent_context, result):
            yield event


# =============================================================================
# Model and Agent Setup
# =============================================================================

def create_model(provider: str = "openai"):
    api_key_env = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "groq": "GROQ_API_KEY",
    }.get(provider, "OPENAI_API_KEY")

    model_map = {
        "openai": f"openai/gpt-4o",
        "gemini": f"gemini/gemini-2.0-flash",
        "anthropic": f"anthropic/claude-3-sonnet-20240229",
        "groq": f"groq/llama-3.3-70b-versatile",
    }

    return LitellmModel(
        model=model_map.get(provider, "openai/gpt-4o"),
        api_key=os.getenv(api_key_env),
    )


def create_assistant(model) -> Agent:
    return Agent(
        name="ChatKit Assistant",
        instructions="You are a helpful AI assistant. Be friendly and concise.",
        model=model,
    )


# =============================================================================
# FastAPI App
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting ChatKit server...")
    yield
    print("Shutting down...")

app = FastAPI(title="ChatKit API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

store = MemoryStore()
model = create_model("openai")
assistant = create_assistant(model)
server = ChatKitServerImpl(store, assistant)


@app.post("/chatkit")
async def chatkit_endpoint(request: Request) -> Response:
    payload = await request.body()
    result = await server.process(payload, {"request": request})

    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache"})

    if hasattr(result, "json"):
        return Response(content=result.json, media_type="application/json")
    return JSONResponse(content=result)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/chatkit/session")
async def create_session():
    return {"client_secret": secrets.token_urlsafe(32), "expires_in": 3600}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### backend/requirements.txt

```
fastapi==0.115.6
uvicorn[standard]==0.32.1
chatkit==1.4.0
openai-agents>=0.6.2
python-dotenv==1.0.1
```

### backend/.env

```bash
OPENAI_API_KEY=sk-...
# GEMINI_API_KEY=...
# ANTHROPIC_API_KEY=...
PORT=8000
```

## Docker Compose

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    env_file:
      - backend/.env

  frontend:
    build: ./frontend
    ports:
      - "3000:3000
    depends_on:
      - backend
```

### frontend/Dockerfile

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npx", "serve", "dist", "-l", "3000"]
```

### backend/Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## Running the Application

### Development Mode

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Access at http://localhost:3000

### Production Mode (Docker)

```bash
docker-compose up -d --build
```

Access at http://localhost:3000

## Validation Checklist

- [ ] Frontend builds without TypeScript errors
- [ ] Backend starts on port 8000
- [ ] Health check returns 200
- [ ] Chat messages stream correctly
- [ ] Thread persistence works (refresh page)
- [ ] New chat creates empty thread
- [ ] CORS allows frontend origin
- [ ] Docker deployment works

## Common Errors

| Error | Solution |
|-------|----------|
| Blank chat UI | Add CDN script to index.html |
| CORS error | Configure allow_origins in FastAPI |
| 401 Unauthorized | Check OPENAI_API_KEY in .env |
| Streaming timeout | Increase client timeout |
| Memory growth | Implement persistent store |

## Related Skills

- `chatkit-frontend` - Detailed frontend patterns
- `chatkit-backend` - Detailed backend patterns
- `chatkit-store` - Persistent storage
- `openai-agents-creater` - Agent customization
