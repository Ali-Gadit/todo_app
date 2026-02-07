---
name: chatkit
description: Comprehensive guide for building AI chat experiences with OpenAI ChatKit (JS/React) and ChatKit-Python. Use when integrating a floating chatbot UI, handling stateless chat history in FastAPI, or connecting agents to a web interface.
---

# ChatKit Integration Skill

This skill provides verified patterns for integrating OpenAI ChatKit into a full-stack application (Next.js/React + FastAPI).

## Core Principles

1. **Direct Web Component Usage**: In React/Next.js, prefer using the standard `<openai-chatkit />` custom element with `setOptions` for maximum stability and version compatibility.
2. **Stateless Request Cycle**: Persist all messages in a database (SQLModel/PostgreSQL) and load history on every request to keep the server stateless.
3. **Formal Handshake**: Implement a `/session` endpoint on the backend to provide a `client_secret` for secure initialization.

## Frontend Implementation (React/Next.js)

### 1. Global Type Declaration
Create `src/types/chatkit.d.ts` to fix TypeScript intrinsic element errors:

```typescript
import * as React from 'react';
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'openai-chatkit': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
        ref?: React.RefObject<any>;
      };
    }
  }
}
```

### 2. ChatPanel Component
The most stable pattern for initializing the chat interface:

```tsx
"use client";
import { useAuth } from "@/lib/auth";
import { useEffect, useRef, useState } from "react";

export default function ChatPanel() {
  const { user } = useAuth();
  const chatRef = useRef<any>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const SCRIPT_URL = "https://cdn.platform.openai.com/deployments/chatkit/chatkit.js";
    const existingScript = document.querySelector(`script[src="${SCRIPT_URL}"]`);
    if (!existingScript) {
      const script = document.createElement("script");
      script.src = SCRIPT_URL;
      script.async = true;
      script.onload = () => setIsLoaded(true);
      document.head.appendChild(script);
    } else {
      setIsLoaded(true);
    }
  }, []);

  useEffect(() => {
    if (isLoaded && chatRef.current && user) {
      chatRef.current.setOptions({
        api: {
          url: `http://localhost:8000/api/chat/${user.id}/chat`,
          domainKey: "localhost", 
          async getClientSecret() {
            const res = await fetch('http://localhost:8000/api/chat/session');
            const data = await res.json();
            return data.client_secret;
          }
        },
        theme: { colorScheme: "light" },
        startScreen: { greeting: "Hello! I'm your AI Assistant." }
      });
    }
  }, [isLoaded, user]);

  return <openai-chatkit ref={chatRef} style={{ height: '100%', width: '100%' }} />;
}
```

## Backend Implementation (FastAPI)

### 1. SQLModel Store
Implement the `Store` interface for persistence:

```python
from chatkit.store import Store, NotFoundError
from chatkit.types import ThreadMetadata, ThreadItem, Page

class SQLModelChatStore(Store[dict]):
    async def load_thread(self, thread_id: str, context: dict) -> ThreadMetadata:
        # DB fetch logic...
        return ThreadMetadata(id=thread_id, created_at=datetime.utcnow())

    async def load_thread_items(self, thread_id, after, limit, order, context) -> Page:
        # DB fetch history logic...
        return Page(data=items, has_more=False)

    async def add_thread_item(self, thread_id, item, context):
        # Save message to DB logic...
        pass
```

### 2. ChatKit Server & Endpoint
Integrate the agent with the streaming server:

```python
from chatkit.server import ChatKitServer, StreamingResult
from chatkit.agents import stream_agent_response

class AgentChatKitServer(ChatKitServer[dict]):
    async def respond(self, thread, item, context):
        input_items = await self.load_history_for_agent(thread.id)
        result = Runner.run_streamed(my_agent, input_items)
        async for event in stream_agent_response(agent_context, result):
            yield event

@router.post("/{user_id}/chat")
async def chatkit_endpoint(request: Request):
    return await server.process(await request.body(), context={})
```

## Common Issues & Fixes

- **Blank Screen**: Ensure the parent container has an explicit height (e.g., `h-[600px]`) and `display: block` is applied to the custom element.
- **Invalid input at api**: Ensure `url` does not have a trailing slash and `domainKey` is present.
- **Hydration Failed**: Wrap the widget in a `mounted` check to ensure it only renders on the client.