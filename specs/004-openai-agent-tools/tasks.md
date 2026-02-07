# Tasks: OpenAI Agent Tools

**Branch**: `004-openai-agent-tools` | **Spec**: [specs/004-openai-agent-tools/spec.md](specs/004-openai-agent-tools/spec.md) | **Plan**: [specs/004-openai-agent-tools/plan.md](specs/004-openai-agent-tools/plan.md)

## Implementation Strategy

We will implement the 5 tools incrementally, starting with setup and foundation, then moving through each tool as a distinct phase corresponding to its user story. All tools will reside in `backend/src/agent/tools.py` but will be implemented and tested sequentially to ensure quality. Unit tests will be added for each tool to verify logic independent of the LLM.

## Dependencies

- **Phase 1 (Setup)**: Blocks all other phases.
- **Phase 2 (Foundation)**: Blocks Phases 3-8.
- **Phase 3 (Add Task)**: Blocks verification of creation flow.
- **Phase 4 (List Tasks)**: Blocks verification of retrieval flow.
- **Phase 5 (Complete Task)**: Blocks verification of completion flow.
- **Phase 6 (Delete Task)**: Blocks verification of deletion flow.
- **Phase 7 (Update Task)**: Blocks verification of update flow.
- **Phase 8 (Agent Config)**: Blocks Phase 9.
- **Phase 9 (Verification)**: Depends on all previous phases.

## Phase 1: Setup

**Goal**: Initialize the environment and dependencies.

- [x] T001 Install `openai-agents` dependency in `backend/requirements.txt`
- [x] T002 [P] Create directory structure `backend/src/agent/`
- [x] T021 [P] Install `python-dotenv` and `openai` in `backend/requirements.txt`
- [x] T022 [P] Configure `GROQ_API_KEY` in `backend/.env`

## Phase 2: Foundation

**Goal**: Establish the module structure for agent tools.

- [x] T003 Create `backend/src/agent/__init__.py` to export tools
- [x] T004 Create `backend/src/agent/utils.py` for shared helpers (formatting, etc.)
- [x] T005 Create `backend/src/agent/tools.py` with initial imports and DB dependency setup

## Phase 3: User Story 1 (Add Task)

**Goal**: Enable the agent to create new tasks.
**Story**: [US1] Add Task via Agent (Priority: P1)

- [x] T006 [US1] Create test file `backend/tests/unit/test_agent_tools.py` with DB fixture
- [x] T007 [US1] Implement `add_task` signature and logic in `backend/src/agent/tools.py`
- [x] T008 [US1] Add unit test for `add_task` in `backend/tests/unit/test_agent_tools.py`

## Phase 4: User Story 2 (List Tasks)

**Goal**: Enable the agent to retrieve tasks.
**Story**: [US2] List Tasks (Priority: P1)

- [x] T009 [US2] Implement `list_tasks` logic in `backend/src/agent/tools.py`
- [x] T010 [US2] Add unit test for `list_tasks` (filtering by status) in `backend/tests/unit/test_agent_tools.py`

## Phase 5: User Story 3 (Complete Task)

**Goal**: Enable the agent to mark tasks as complete.
**Story**: [US3] Complete Task (Priority: P2)

- [x] T011 [US3] Implement `complete_task` logic in `backend/src/agent/tools.py`
- [x] T012 [US3] Add unit test for `complete_task` in `backend/tests/unit/test_agent_tools.py`

## Phase 6: User Story 4 (Delete Task)

**Goal**: Enable the agent to remove tasks.
**Story**: [US4] Delete Task (Priority: P3)

- [x] T013 [US4] Implement `delete_task` logic in `backend/src/agent/tools.py`
- [x] T014 [US4] Add unit test for `delete_task` in `backend/tests/unit/test_agent_tools.py`

## Phase 7: User Story 5 (Update Task)

**Goal**: Enable the agent to modify tasks.
**Story**: [US5] Update Task (Priority: P3)

- [x] T015 [US5] Implement `update_task` logic in `backend/src/agent/tools.py`
- [x] T016 [US5] Add unit test for `update_task` in `backend/tests/unit/test_agent_tools.py`

## Phase 8: Agent Integration

**Goal**: Configure the Agent with the implemented tools and Groq provider.

- [x] T017 Create `backend/src/agent/agent.py` using Groq configuration from root `openai-agents-creater` skill
- [x] T018 Integrate agent instantiation in `backend/src/agent/__init__.py` and verify importability

## Phase 9: Verification & Polish

**Goal**: Verify all tools work as expected in a manual script.

- [x] T019 Create manual verification script `backend/src/agent/manual_test.py` based on `specs/004-openai-agent-tools/quickstart.md`
- [x] T020 Run all unit tests to ensure no regressions
