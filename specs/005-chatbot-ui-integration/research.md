# Research: Chatbot UI Integration

**Feature**: `005-chatbot-ui-integration`
**Date**: 2026-02-02
**Status**: Complete

## Decision: Use `openai-chatkit` (JS/React + Python)

We will use the official OpenAI ChatKit libraries to build the chatbot experience.

### Rationale

- **High-Fidelity UI**: ChatKit JS provides production-ready components that handle message list rendering, composer state, and agent persona with minimal code.
- **Streaming Support**: Built-in support for streaming responses from the backend.
- **Standardized Backend**: `chatkit-python` provides helper classes for formatting responses and handling the message items required by the frontend.
- **Agent Integration**: Seamless integration with the `openai-agents` SDK (which we already use for `todo_agent`).

### Alternatives Considered

- **Custom React UI + Standard API**:
    - *Rejected*: Requires building complex UI logic for message bubbles, scrolling, and loading states from scratch.
- **LangChain / Vercel AI SDK**:
    - *Rejected*: While powerful, `openai-chatkit` is specifically optimized for the OpenAI Agents SDK workflow we are implementing.

## Implementation Details

### Frontend Widget Pattern

The ChatBot icon will be a fixed-position `button` in `layout.tsx`.
When clicked, it will toggle a state `isChatOpen`.
The chat window will render the `ChatKit` component (from `@openai/chatkit-react`) inside a styled container.

### Backend Stateless Request Cycle

Following the provided specification:
1.  **Input**: `{user_id}`, `conversation_id` (optional), `message`.
2.  **Fetch History**: Query the `Message` table for the last 10-20 turns matching the `conversation_id`.
3.  **Agent Run**:
    ```python
    from agents import Runner
    # Convert DB messages to agent items
    input_items = [Item(role=m.role, content=m.content) for m in history]
    input_items.append(Item(role="user", content=message))
    
    result = await Runner.run(todo_agent, input_items)
    ```
4.  **Persistence**: Save the new user message and the agent's response to the `Message` table.
5.  **Output**: Return the response text and any tool calls made by the agent.

## Action Items

1.  Add `@openai/chatkit-react` to `frontend/package.json`.
2.  Add `chatkit-python` to `backend/requirements.txt`.
3.  Create DB migrations for `Conversation` and `Message`.
