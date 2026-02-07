# Implementation Plan: OpenAI Agent Tools

**Branch**: `004-openai-agent-tools` | **Date**: 2026-02-02 | **Spec**: [specs/004-openai-agent-tools/spec.md](specs/004-openai-agent-tools/spec.md)
**Input**: Feature specification from `/specs/004-openai-agent-tools/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The goal is to implement 5 function tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) for an OpenAI Agent using the `openai-agents-python` library. The agent will process natural language user requests (e.g., "Add a task to buy milk") and invoke the appropriate tool to perform CRUD operations on the Todo application's database. This moves the application from a manual CLI/Web interface to an agentic interface.

## Technical Context

**Language/Version**: Python 3.12+ (to match `openai-agents-python` requirements and project standards)
**Primary Dependencies**:
- `openai-agents`: For Agent and Tool definitions.
- `openai`: AsyncOpenAI client for Groq integration.
- `python-dotenv`: To load API keys.
- `sqlmodel`: For database interactions.
**Model Provider**: Groq (Llama-3.3-70b-versatile) via OpenAI-compatible SDK.
**Storage**: Neon Serverless PostgreSQL (via SQLModel).
**Testing**: `pytest` for unit testing the tools and agent logic.
**Target Platform**: Linux server / Container (Docker).
**Project Type**: Backend service (integrated into existing backend).
**Performance Goals**: Tools should execute within standard HTTP timeout limits (<2s typically for DB ops). Agent response time depends on LLM but tool execution must be fast.
**Constraints**: Stateless tools preferred. Must handle DB connections cleanly.
**Scale/Scope**: 5 tools, 1 agent configuration.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-Driven Development**: Yes, spec exists.
- **Agentic Implementation**: Yes, using Claude Code for implementation.
- **Incremental Delivery**: Yes, focusing on P1 tools first.
- **Progressive Complexity**: Yes, moving to Phase III (AI Chatbot) which justifies the use of Agents SDK and MCP.
- **Clean Code**: Tools will be typed, documented, and tested.
- **Tech Stack**: Matches Phase III stack (Python, FastAPI, OpenAI Agents SDK).

## Project Structure

### Documentation (this feature)

```text
specs/004-openai-agent-tools/
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
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── tools.py      # The 5 function tools
│   │   ├── agent.py      # Agent definition and configuration
│   │   └── utils.py      # Helper functions (e.g. formatting)
│   ├── main.py           # Integration point (if exposing via API)
│   └── models/           # Existing models (Task)
└── tests/
    └── unit/
        └── test_agent_tools.py # Unit tests for tools
```

**Structure Decision**: Integrated into existing `backend/` directory under a new `src/agent/` module to keep agent logic encapsulated but close to the models and DB logic it needs to access.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New `openai-agents-python` dependency | Required for Phase III AI Chatbot | Custom prompt engineering + manual function calling is brittle and harder to maintain than the SDK. |