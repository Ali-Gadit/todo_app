# Feature Specification: Todo AI Chatbot

**Feature Branch**: `003-todo-ai-chatbot`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "Phase III: Todo AI Chatbot - Basic Level Functionality - Objective: Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture"

## User Scenarios & Testing *(mandatory)*

<!--
  User stories are prioritized as user journeys ordered by importance.
  Each user story is INDEPENDENTLY TESTABLE - implementing one delivers a viable MVP.
  P1 = Must have (MVP), P2 = Should have, P3 = Nice to have
-->

### User Story 1 - AI-Powered Todo Management (Priority: P1)

As a user, I want to manage my todos through natural language conversation with an AI assistant, so that I can add, view, complete, and delete tasks without using a manual interface.

**Why this priority**: This is the core value proposition of Phase III - enabling AI-driven todo management through conversational interaction. Without this, there is no chatbot functionality.

**Independent Test**: Can be tested by opening the ChatKit chat interface, sending messages like "Add buy groceries to my list" or "Show me my tasks", and verifying tasks are created/displayed correctly in the database.

**Acceptance Scenarios**:

1. **Given** user has no tasks, **When** user sends "Add buy milk to my todo list", **Then** system creates a new task with title "buy milk", **And** AI responds confirming the task was added.

2. **Given** user has tasks in the database, **When** user sends "What are my tasks?", **Then** system retrieves tasks from database via MCP tool, **And** AI displays the list in a conversational format.

3. **Given** user has existing tasks, **When** user sends "Mark buy milk as complete", **Then** system updates task status to completed, **And** AI confirms the completion.

---

### User Story 2 - Conversation Context Persistence (Priority: P1)

As a returning user, I want my conversation history and task context to persist across sessions, so that I can continue my workflow seamlessly when I return.

**Why this priority**: Without conversation persistence, users lose context and cannot have meaningful multi-turn conversations with the AI about their tasks.

**Independent Test**: Can be tested by creating tasks in one session, refreshing the page, and verifying both the conversation thread and task data are restored.

**Acceptance Scenarios**:

1. **Given** user created tasks in a previous session, **When** user starts a new chat session, **Then** the conversation thread is loaded from database, **And** previous messages are visible, **And** task context is available.

2. **Given** user is in an active conversation, **When** user navigates away and returns, **Then** the same thread ID is restored, **And** conversation continues from where it left off.

---

### User Story 3 - Multi-Turn Task Refinement (Priority: P2)

As a user, I want to refine and modify my tasks through follow-up conversations, so that I can make changes using natural language without manual editing.

**Why this priority**: This enhances usability by allowing natural task management without switching to manual interfaces.

**Independent Test**: Can be tested by adding a task, then sending follow-up messages like "Change the due date to tomorrow" or "Rename it to buy almond milk", and verifying the task is updated correctly.

**Acceptance Scenarios**:

1. **Given** user has a task "buy milk", **When** user sends "Actually, change it to buy almond milk instead", **Then** system updates the task title, **And** AI confirms the change.

2. **Given** user has a task with title "buy milk", **When** user sends "Delete that task", **Then** system removes the task from database, **And** AI confirms deletion.

---

### User Story 4 - AI-Powered Task Suggestions (Priority: P3)

As a user, I want the AI to proactively suggest helpful task actions based on my conversation, so that I can manage my todos more efficiently.

**Why this priority**: This is a nice-to-have enhancement that provides additional value beyond basic CRUD operations.

**Independent Test**: Can be tested by sending messages about time-sensitive activities and verifying AI suggests relevant task creations.

**Acceptance Scenarios**:

1. **Given** user mentions "I need to finish the report by Friday", **When** AI detects this intent, **Then** AI suggests creating a task with deadline.

2. **Given** user has many incomplete tasks, **When** user asks for help prioritizing, **Then** AI analyzes tasks and suggests an order based on urgency or deadline.

---

### Edge Cases

- **Empty Task List**: What happens when user asks for tasks but none exist? AI should respond with helpful guidance to add tasks.
- **Concurrent Modifications**: How does the system handle simultaneous task modifications via chat?
- **Invalid Natural Language**: What happens when user sends ambiguous or unparseable requests?
- **MCP Server Unavailable**: How does the system degrade when MCP server is unreachable?
- **Database Connection Failures**: How are transient errors handled and communicated to users?
- **Long Conversation History**: How does the system handle very long conversation threads?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose an MCP server with tools for todo CRUD operations (add_task, list_tasks, complete_task, delete_task, update_task).
- **FR-002**: System MUST provide a ChatKit-based chat interface for natural language interaction.
- **FR-003**: System MUST route chat messages through OpenAI Agents SDK to MCP server tools.
- **FR-004**: System MUST persist conversation state (threads, messages) in PostgreSQL database.
- **FR-005**: System MUST persist task data in PostgreSQL database via SQLModel ORM.
- **FR-006**: System MUST maintain stateless chat endpoints (FastAPI) with database-backed state.
- **FR-007**: System MUST authenticate users via Better Auth before allowing chat access.
- **FR-008**: System MUST stream AI responses in real-time using Server-Sent Events (SSE).
- **FR-009**: System MUST handle multi-turn conversations with context preservation.
- **FR-010**: System MUST provide session management for chat authentication.

### Non-Functional Requirements

- **NFR-001**: Chat responses MUST be delivered within 5 seconds for P95 latency.
- **NFR-002**: System MUST handle at least 10 concurrent chat sessions.
- **NFR-003**: Conversation history MUST be queryable within 100ms.
- **NFR-004**: System MUST gracefully handle MCP server unavailability with user-friendly errors.
- **NFR-005**: All chat data MUST be encrypted in transit (HTTPS/WSS).

### Key Entities

- **Task**: Represents a todo item with title, description, status (pending/completed), created_at, updated_at, and foreign key to user.
- **Conversation**: Represents a chat thread with thread_id, user_id, created_at, updated_at.
- **Message**: Represents a chat message within a conversation with role (user/assistant), content, created_at.
- **User**: Existing user entity from Phase II authentication system.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users CAN create tasks entirely through natural language conversation within 3 turns.
- **SC-002**: Users CAN view, update, and delete tasks through conversational commands.
- **SC-003**: Conversation context IS preserved across page refreshes.
- **SC-004**: AI responses for task operations COMPLETE within 5 seconds (P95).
- **SC-005**: System MAINTAINS 99% availability for chat endpoints during business hours.

### Technical Metrics

- **TM-001**: MCP tool calls succeed with 99.5% reliability.
- **TM-002**: Database queries for conversation loading complete under 100ms.
- **TM-003**: No memory leaks in long-running chat sessions (session memory < 100MB).
- **TM-004**: Streaming connection reconnection succeeds within 2 seconds.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ChatKit Frontend (React)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  useChatKit hook + Chat component + Thread persistence  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                    POST /chat (SSE)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /chat - Stateless streaming chat endpoint         │   │
│  │  GET  /conversations - List user's conversations        │   │
│  │  GET  /conversations/{id} - Get conversation history    │   │
│  │  POST /auth/* - Better Auth endpoints                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│              ┌───────────────┴───────────────┐                  │
│              ▼                               ▼                  │
│  ┌─────────────────────┐       ┌─────────────────────┐          │
│  │  OpenAI Agents SDK  │       │    PostgreSQL DB    │          │
│  │  - Agent with MCP   │       │  - Tasks table      │          │
│  │  - Streaming runner │       │  - Conversations    │          │
│  └──────────┬──────────┘       │  - Messages         │          │
│             │                  └─────────────────────┘          │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MCP Server (Python FastMCP)                 │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ Tools:                                            │   │   │
│  │  │ - add_task(title, description, due_date)         │   │   │
│  │  │ - list_tasks(status, limit, offset)              │   │   │
│  │  │ - complete_task(task_id)                         │   │   │
│  │  │ - delete_task(task_id)                           │   │   │
│  │  │ - update_task(task_id, **updates)                │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose | Source |
|-------|------------|---------|--------|
| **Frontend UI** | ChatKit (React) | AI chat interface with useChatKit hook | `.claude/skills/chatkit/*` |
| **Frontend Framework** | Next.js 16+ (App Router) | React framework for web UI | `.claude/skills/nextjs-app-router` |
| **Backend API** | FastAPI | Python web framework for chat endpoints | `.claude/skills/fastapi-sqlmodel` |
| **Agent Orchestration** | OpenAI Agents SDK | Agent runner, handoffs, guardrails | `.claude/skills/openai-agents-creater` |
| **Tool Server** | MCP Python SDK (FastMCP) | MCP server with tools for tasks | `.claude/skills/mcp-python-sdk` |
| **Database** | PostgreSQL (Neon) | Serverless database for persistence | `.claude/skills/postgresql-neon` |
| **ORM** | SQLModel | SQL + Pydantic ORM for database models | `.claude/skills/fastapi-sqlmodel` |
| **Authentication** | Better Auth | JWT-based authentication | `.claude/skills/better-auth` |
| **AI Models** | LiteLLM | Multi-provider LLM support (OpenAI, Gemini, Anthropic, Groq) | `.claude/skills/openai-agents-creater` |
| **Streaming** | Server-Sent Events (SSE) | Real-time AI response streaming | `.claude/skills/fastapi-chatbot` |

### MCP Tools (5 tools)

| Tool | Parameters | Returns |
|------|------------|---------|
| `add_task` | title: str, description?: str, due_date?: str | Task object |
| `list_tasks` | status?: "pending" \| "completed", limit?: int, offset?: int | List[Task] |
| `complete_task` | task_id: str | Task object |
| `delete_task` | task_id: str | Success boolean |
| `update_task` | task_id: str, title?: str, description?: str, due_date?: str | Task object |

### Architecture Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Layer                             │
│  ChatKit UI (React) ←→ Next.js 16+ App Router                │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    Backend Layer                              │
│  FastAPI ←→ Better Auth (JWT)                                │
│       │                                                       │
│       ├──→ OpenAI Agents SDK (Agent + Streaming Runner)      │
│       │         │                                              │
│       │         └──→ MCP Server (FastMCP)                     │
│       │                   │                                   │
│       │                   └──→ PostgreSQL (Neon)              │
│       │                                                     │
│       └──→ SQLModel ORM                                      │
└──────────────────────────────────────────────────────────────┘
```

## API Contracts

### POST /chat

**Purpose**: Stateless streaming chat endpoint

**Input**:
```json
{
  "message": "string (required)",
  "thread_id": "string (optional)",
  "conversation_id": "string (optional)"
}
```

**Output**: Server-Sent Events (SSE)
```
data: {"type": "message", "content": "..."}
data: {"type": "message", "content": "..."}
data: {"type": "done"}
```

**Errors**:
- 401: Unauthorized - Invalid or missing auth token
- 400: Bad Request - Invalid message format
- 503: Service Unavailable - MCP server unreachable

### MCP Tools

| Tool | Parameters | Returns |
|------|------------|---------|
| add_task | title: str, description?: str, due_date?: str | Task object |
| list_tasks | status?: "pending" \| "completed", limit?: int, offset?: int | List[Task] |
| complete_task | task_id: str | Task object |
| delete_task | task_id: str | Success boolean |
| update_task | task_id: str, title?: str, description?: str, due_date?: str | Task object |

## Dependencies

### External Services
- **OpenAI API**: For LLM inference (gpt-4o or equivalent)
- **Neon PostgreSQL**: Serverless database for persistence
- **ChatKit CDN**: Frontend component delivery

### Internal Modules
- Phase II: `fastapi-sqlmodel` skill for backend patterns
- Phase II: `better-auth` skill for authentication
- Phase II: `postgresql-neon` skill for database configuration
- Phase II: `nextjs-app-router` skill for frontend patterns
- Phase II: `mcp-python-sdk` skill for MCP server
- Phase II: `openai-agents-creater` skill for agent integration
- Phase II: `chatkit-complete` skill for ChatKit integration

## Constraints & Non-Goals

### Constraints
- Must use existing Phase II authentication system
- Must integrate with existing PostgreSQL schema
- Must use ChatKit for frontend chat interface
- Must use OpenAI Agents SDK for agent orchestration
- Must use MCP Python SDK for tool definition

### Out of Scope (Phase III)
- Voice/audio chat interfaces
- Image attachments in chat
- Advanced AI features (memory, personalization)
- Multi-user collaborative todos
- Task sharing/collaboration
- Push notifications
- Mobile app support

## Implementation Hints

### Recommended Tools
- `mcp-python-sdk`: For creating MCP server with FastMCP
- `openai-agents-creater`: For agent with MCP server integration
- `chatkit-complete`: For full ChatKit frontend + backend integration
- `fastapi-sqlmodel`: For REST endpoints and ORM models
- `postgresql-neon`: For Neon database configuration

### Key Patterns
- Use Streamable HTTP transport for MCP servers
- Implement conversation context via thread_id in localStorage
- Use SSE for streaming AI responses to ChatKit
- Store conversation history for context injection

## Validation Checklist

- [ ] Chat interface renders without blank screen
- [ ] Natural language task creation works (add, view, complete, delete)
- [ ] Conversation thread persists across page refresh
- [ ] AI responses stream in real-time
- [ ] Authentication protects chat endpoints
- [ ] MCP tools execute successfully against database
- [ ] Error handling provides user-friendly messages
- [ ] System handles concurrent chat sessions
- [ ] Streaming connection reconnects on disconnect
- [ ] Conversation history loads within 100ms
