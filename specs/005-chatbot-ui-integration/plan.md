# Implementation Plan: Chatbot UI Integration

**Branch**: `005-chatbot-ui-integration` | **Date**: 2026-02-02 | **Spec**: [specs/005-chatbot-ui-integration/spec.md](specs/005-chatbot-ui-integration/spec.md)
**Input**: Feature specification from `/specs/005-chatbot-ui-integration/spec.md`

## Summary

This feature integrates a floating AI agent chatbot into the Todo web application. We will use `openai-chatkit` for both the React frontend and FastAPI backend. The frontend will feature a toggleable chat widget in the bottom-right corner. The backend will expose a stateless chat endpoint that persists conversation history and message turns in PostgreSQL, using the previously implemented `todo_agent` to process natural language commands and invoke task-related tools.

## Technical Context

**Language/Version**: Python 3.12+, TypeScript (Next.js 16+)
**Primary Dependencies**:
- `chatkit-python`: Backend SDK for ChatKit integration.
- `@openai/chatkit-react`: Frontend React components for the chat UI.
- `openai-agents`: Already used for the `todo_agent`.
- `sqlmodel`: For database persistence of Conversations and Messages.
- `lucide-react`: For the agent icon (FAB).
**Storage**: Neon Serverless PostgreSQL.
**Testing**: `pytest` for API endpoint verification, `vitest` for frontend component rendering.
**Target Platform**: Web (Linux/Browser).
**Project Type**: Monorepo (Next.js + FastAPI).
**Performance Goals**: Agent response streaming (if possible) or < 2s response time for tool-less queries.
**Constraints**: Must maintain statelessness on the server (all state in DB).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-Driven Development**: Yes, spec exists.
- **Agentic Implementation**: Yes, using Claude Code.
- **Incremental Delivery**: Yes, focusing on P1 (Natural Language management) first.
- **Progressive Complexity**: Yes, moving to Phase III (AI Chatbot) justifies adding ChatKit and history persistence.
- **Clean Code**: Following monorepo standards and SQLModel patterns.

## Project Structure

### Documentation (this feature)

```text
specs/005-chatbot-ui-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── chat.py       # New: POST /api/{user_id}/chat logic
│   ├── models/
│   │   ├── conversation.py # New: Conversation model
│   │   └── message.py      # New: Message model
│   ├── services/
│   │   └── chat_service.py # New: Logic for stateless history fetching
│   └── main.py           # Registration of chat router
└── tests/
    └── integration/
        └── test_chat_api.py

frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatWidget.tsx # Floating widget container
│   │   │   └── ChatPanel.tsx  # Wrapper for ChatKit component
│   └── app/
│       └── layout.tsx      # Inject ChatWidget globally
└── package.json
```

**Structure Decision**: Integrated into standard `backend/` and `frontend/` folders. Models are separated for clarity. Frontend logic is kept in a dedicated `chat/` component folder.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New `chatkit` dependencies | Required for high-quality, streaming-capable UI components and standardized backend response formats. | Custom chat UI is time-consuming and hard to get right (accessibility, streaming). |
| Two new DB tables | Required for stateless session persistence and history-aware agent responses. | In-memory history would be lost on server restart and wouldn't scale. |