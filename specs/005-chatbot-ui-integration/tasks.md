# Tasks: Chatbot UI Integration

**Input**: Design documents from `/specs/005-chatbot-ui-integration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Install `chatkit-python` dependency in `backend/requirements.txt`
- [x] T002 Install `@openai/chatkit-react` dependency in `frontend/package.json`
- [x] T003 [P] Create backend directory structure `backend/src/api/` and `backend/src/services/`
- [x] T004 [P] Create frontend directory structure `frontend/src/components/chat/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T005 [P] Create `Conversation` model in `backend/src/models/conversation.py`
- [x] T006 [P] Create `Message` model in `backend/src/models/message.py`
- [x] T007 Register new models in `backend/src/models/__init__.py`
- [x] T008 Create and run DB migration for `Conversation` and `Message` tables

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to manage tasks via natural language chat in a floating widget.

**Independent Test**: User can open the chat widget, send "Add a task to buy groceries", and see the agent's confirmation.

### Implementation for User Story 1

- [x] T009 [US1] Implement `ChatService` for history fetching in `backend/src/services/chat_service.py`
- [x] T010 [US1] Implement `POST /api/{user_id}/chat` endpoint in `backend/src/api/chat.py`
- [x] T011 [US1] Register chat router in `backend/src/main.py`
- [x] T012 [P] [US1] Create `ChatPanel.tsx` in `frontend/src/components/chat/ChatPanel.tsx` using `@openai/chatkit-react`
- [x] T013 [P] [US1] Create `ChatWidget.tsx` floating container in `frontend/src/components/chat/ChatWidget.tsx`
- [x] T014 [US1] Inject `ChatWidget` in `frontend/src/app/layout.tsx`

**Checkpoint**: User Story 1 functional - basic chat interaction works.

---

## Phase 4: User Story 2 - Conversation Persistence (Priority: P2)

**Goal**: Preserve chat history across sessions using `conversation_id`.

**Independent Test**: User refreshes the page and previously sent messages remain in the chat window.

### Implementation for User Story 2

- [x] T015 [US2] Update `ChatService` to handle `conversation_id` filtering and session creation in `backend/src/services/chat_service.py`
- [x] T016 [US2] Update chat API to return and persist `conversation_id` in `backend/src/api/chat.py`
- [x] T017 [US2] Implement history loading logic in `frontend/src/components/chat/ChatPanel.tsx`

**Checkpoint**: User Story 2 functional - history is persisted and loaded correctly.

---

## Phase 5: User Story 3 - Agent Tool Feedback (Priority: P3)

**Goal**: Provide feedback to the user regarding the agent's tool invocations.

**Independent Test**: API response for a task addition includes the `tool_calls` array with `add_task` details.

### Implementation for User Story 3

- [x] T018 [US3] Capture and return `tool_calls` in `POST /api/{user_id}/chat` response in `backend/src/api/chat.py`
- [x] T019 [US3] Update `frontend/src/components/chat/ChatPanel.tsx` to handle tool call rendering or feedback
...
## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T020 [P] Add integration test for chat API in `backend/tests/integration/test_chat_api.py`
- [x] T021 Verify user isolation (RBAC) for chat endpoints in `backend/src/api/chat.py`
- [x] T022 Run `quickstart.md` validation and cleanup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup. BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational completion.
- **Polish (Final Phase)**: Depends on all user stories.

### Parallel Opportunities

- T003, T004 (Structure)
- T005, T006 (Models)
- T012, T013 (Frontend MVP components)
- T020 (Integration testing)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **VALIDATE**: Verify natural language task management via the UI.

### Incremental Delivery

1. Foundation ready.
2. Add US1 (Chat Widget) -> MVP.
3. Add US2 (Persistence).
4. Add US3 (Feedback).
