---
name: fastapi-chatbot
description: Generates FastAPI routes and session management for an AI chatbot powered by the OpenAI Agents SDK.
---

# FastAPI Chatbot Skill

This Skill generates the necessary FastAPI routes, session management, and Pydantic models to expose an OpenAI Agent as a web API.

## Usage

To generate the FastAPI structure, specify:
- **agent_instance**: The variable name of your initialized Agent (e.g., `codeverse_agent`).
- **run_config**: The variable name of your `RunConfig` (e.g., `config`).
- **app_instance**: The FastAPI app instance (e.g., `app`).
- **speaker_names**: Name for user and bot (e.g., `USER` and `CODEY`).

## Code Template

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import asyncio

# Pydantic models for request/response
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    success: bool
    session_id: str

# In-memory session store (replace with Redis/DB for production)
conversation_sessions: Dict[str, List[Message]] = {}

def build_conversation_history(message_history: List[Message], new_message: str) -> str:
    """Formats conversation history for the agent input"""
    if not message_history:
        return f"USER: {new_message}\n\nASSISTANT:"

    conversation_text = "Previous context:\n\n"
    for msg in message_history:
        speaker = "USER" if msg.role == "user" else "ASSISTANT"
        conversation_text += f"{speaker}: {msg.content}\n\n"

    conversation_text += f"Current: {new_message}\n\nASSISTANT:"
    return conversation_text

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    try:
        # Session Management
        session_id = request.session_id or str(uuid.uuid4())
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []

        session_history = conversation_sessions[session_id]
        complete_input = build_conversation_history(session_history, request.message)

        # Execute Agent
        runner = await Runner.run(
            starting_agent=agent_instance,
            run_config=run_config,
            input=complete_input
        )

        # Update History
        conversation_sessions[session_id].append(Message(role="user", content=request.message))
        conversation_sessions[session_id].append(Message(role="assistant", content=runner.final_output))

        return ChatResponse(
            response=runner.final_output,
            success=True,
            session_id=session_id
        )

    except Exception as e:
        print(f"Chat error: {e}")
        return ChatResponse(
            response="Sorry, I am currently unavailable. Please try again later.",
            success=False,
            session_id=request.session_id or ""
        )
```

## Features Included
- **Session ID generation**: Automatically creates UUIDs for new conversations.
- **Context Awareness**: Passes full conversation history to the agent.
- **Error Handling**: Graceful error responses for production stability.
- **Pydantic Validation**: Robust input/output parsing.
