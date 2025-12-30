# Tasks: Todo Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/models/, src/services/, src/cli/, src/lib/, tests/contract/, tests/integration/, tests/unit/
- [x] T002 Create pyproject.toml with UV configuration for Python 3.13+ project
- [x] T003 [P] Configure Ruff for linting and formatting in pyproject.toml
- [x] T004 [P] Configure pyright for type checking in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create custom exception types TaskNotFound and InvalidTitle in src/lib/exceptions.py
- [x] T006 Create Task entity dataclass with id, title, description, completed fields in src/models/task.py
- [x] T007 Create TaskService class with _tasks list and _next_id counter in src/services/task_service.py
- [x] T008 Implement add_task method with title validation in src/services/task_service.py
- [x] T009 Implement list_tasks method in src/services/task_service.py
- [x] T010 Implement get_task method in src/services/task_service.py
- [x] T011 Implement update_task method with validation in src/services/task_service.py
- [x] T012 Implement mark_complete method in src/services/task_service.py
- [x] T013 Implement mark_incomplete method in src/services/task_service.py
- [x] T014 Implement delete_task method in src/services/task_service.py
- [x] T015 Create CLI command handlers (add_task_cmd, list_tasks_cmd, update_task_cmd, complete_cmd, incomplete_cmd, delete_task_cmd) in src/cli/commands.py
- [x] T016 Create main entry point with argparse and command routing in src/cli/main.py
- [x] T017 Configure command-line interface in pyproject.toml with entry point

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with title and optional description

**Independent Test**: Can be fully tested by adding multiple tasks with different titles and descriptions, confirming each task is stored with unique sequential ID

### Implementation for User Story 1

- [x] T018 [P] [US1] Add argparse subparser for 'add' command with title and description arguments in src/cli/commands.py
- [x] T019 [US1] Integrate add_task_cmd with TaskService.add_task method for validation and task creation in src/cli/commands.py
- [x] T020 [US1] Add success/error message display for add command (task ID confirmation, title validation errors) in src/cli/commands.py
- [x] T021 [US1] Test add command with valid title only (no description) from CLI
- [x] T022 [US1] Test add command with valid title and description from CLI
- [x] T023 [US1] Test add command with empty title (should display error) from CLI
- [x] T024 [US1] Verify task ID increments sequentially for multiple added tasks

**Checkpoint**: At this point, User Story 1 (Add Tasks) should be fully functional and testable independently. Users can add tasks with unique sequential IDs.

---

## Phase 4: User Story 2 - View Tasks (Priority: P2)

**Goal**: Enable users to display all tasks with status indicators (complete/incomplete)

**Independent Test**: Can be fully tested by adding multiple tasks and viewing the list to confirm all tasks appear with correct status indicators and descriptions

### Implementation for User Story 2

- [x] T025 [P] [US2] Add argparse subparser for 'list' command in src/cli/commands.py
- [x] T026 [US2] Integrate list_tasks_cmd with TaskService.list_tasks method to retrieve all tasks in src/cli/commands.py
- [x] T027 [US2] Format task display with ID, title, description, and status indicators (⬜ for incomplete, ✅ for complete) in src/cli/commands.py
- [x] T028 [US2] Add empty list message ("No tasks found") when task list is empty in src/cli/commands.py
- [x] T029 [US2] Display task count summary (total, completed, pending) in src/cli/commands.py
- [x] T030 [US2] Test list command with multiple tasks (mixed statuses) from CLI
- [x] T031 [US2] Test list command with empty task list from CLI
- [x] T032 [US2] Verify task display is readable and organized with clear visual distinction between complete and incomplete tasks

**Checkpoint**: At this point, User Stories 1 (Add) AND 2 (View) should both work independently. Users can add tasks and view their task list.

---

## Phase 5: User Story 3 - Update Tasks (Priority: P3)

**Goal**: Enable users to modify task titles and descriptions by ID

**Independent Test**: Can be fully tested by creating a task, updating its title and/or description, and verifying changes are reflected when viewing task list

### Implementation for User Story 3

- [x] T033 [P] [US3] Add argparse subparser for 'update' command with id, title, and description arguments in src/cli/commands.py
- [x] T034 [US3] Integrate update_task_cmd with TaskService.update_task method for updating task details in src/cli/commands.py
- [x] T035 [US3] Add title validation for update operation (prevent empty titles) in src/cli/commands.py
- [x] T036 [US3] Add success/error message display for update command (task confirmation, task not found errors, validation errors) in src/cli/commands.py
- [x] T037 [US3] Test update command with title only (keep existing description) from CLI
- [x] T038 [US3] Test update command with title and description from CLI
- [x] T039 [US3] Test update command with non-existent task ID (should display error) from CLI
- [x] T040 [US3] Test update command with empty new title (should display error) from CLI
- [x] T041 [US3] Verify update operation preserves task ID and other unchanged fields

**Checkpoint**: At this point, User Stories 1 (Add), 2 (View), AND 3 (Update) should all work independently. Users can add, view, and update tasks.

---

## Phase 6: User Story 4 - Mark Complete (Priority: P4)

**Goal**: Enable users to toggle task status between complete and incomplete by ID

**Independent Test**: Can be fully tested by creating a task, marking it complete, verifying status indicator changes, then marking it incomplete and verifying status reverts

### Implementation for User Story 4

- [x] T042 [P] [US4] Add argparse subparser for 'complete' command with task ID argument in src/cli/commands.py
- [x] T043 [US4] Integrate complete_cmd with TaskService.mark_complete method in src/cli/commands.py
- [x] T044 [P] [US4] Add argparse subparser for 'incomplete' command with task ID argument in src/cli/commands.py
- [x] T045 [US4] Integrate incomplete_cmd with TaskService.mark_incomplete method in src/cli/commands.py
- [x] T046 [US4] Add success/error message display for complete/incomplete commands (task confirmation, task not found errors) in src/cli/commands.py
- [x] T047 [US4] Test complete command with valid task ID (incomplete → complete) from CLI
- [x] T048 [US4] Test incomplete command with valid task ID (complete → incomplete) from CLI
- [x] T049 [US4] Test complete command with non-existent task ID (should display error) from CLI
- [x] T050 [US4] Test incomplete command with non-existent task ID (should display error) from CLI
- [x] T051 [US4] Verify status toggle works correctly (complete ↔ incomplete) and displays correct indicator in list

**Checkpoint**: At this point, User Stories 1 (Add), 2 (View), 3 (Update), AND 4 (Mark Complete) should all work independently. Users can add, view, update, and toggle task completion status.

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P5)

**Goal**: Enable users to permanently remove tasks by ID

**Independent Test**: Can be fully tested by creating a task, deleting it by ID, and verifying it no longer appears in task list

### Implementation for User Story 5

- [x] T052 [P] [US5] Add argparse subparser for 'delete' command with task ID argument in src/cli/commands.py
- [x] T053 [US5] Integrate delete_task_cmd with TaskService.delete_task method in src/cli/commands.py
- [x] T054 [US5] Add success/error message display for delete command (task confirmation, task not found errors) in src/cli/commands.py
- [x] T055 [US5] Test delete command with valid task ID from CLI
- [x] T056 [US5] Test delete command with non-existent task ID (should display error) from CLI
- [x] T057 [US5] Verify deletion removes task from list and does not renumber remaining task IDs
- [x] T058 [US5] Verify deleted task no longer appears when viewing task list

**Checkpoint**: At this point, ALL User Stories (1, 2, 3, 4, AND 5) should now be independently functional. Users can add, view, update, complete/incomplete, and delete tasks.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T059 [P] Create README.md with setup instructions and usage examples
- [x] T060 [P] Verify all operations meet performance criteria from spec (add <10s, view <1s, update <5s, complete/delete <3s)
- [x] T061 [P] Test all edge cases from spec: long inputs (>1000 chars), special characters/emojis, duplicate titles, rapid successive commands
- [x] T062 [P] Verify task list displays remain readable with 50+ tasks
- [x] T063 [P] Run Ruff to ensure PEP 8 compliance and fix any issues
- [x] T064 [P] Run pyright to ensure type checking passes and fix any issues
- [x] T065 Run quickstart.md validation checklist to ensure all items pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Add Tasks)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - View Tasks)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3 - Update Tasks)**: Can start after Foundational (Phase 2) - May use add/view commands but should be independently testable
- **User Story 4 (P4 - Mark Complete)**: Can start after Foundational (Phase 2) - May use add/view commands but should be independently testable
- **User Story 5 (P5 - Delete Tasks)**: Can start after Foundational (Phase 2) - May use add/view commands but should be independently testable

### Within Each User Story

- CLI command implementations before integration tests
- Core implementation before integration tests
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- All user story CLI integration tasks can run in parallel within their phases:
  - Phase 3: T018 can run in parallel (US1)
  - Phase 4: T025 can run in parallel (US2)
  - Phase 5: T033 can run in parallel (US3)
  - Phase 6: T042, T044 can run in parallel (US4)
  - Phase 7: T052 can run in parallel (US5)
- All Polish tasks marked [P] can run in parallel (T059, T060-T065)
- Different user stories can be worked on in parallel by different team members after Foundational phase

---

## Parallel Example: User Story 1 (Add Tasks)

```bash
# Launch all implementation tasks for User Story 1 together:
Task: "Add argparse subparser for 'add' command in src/cli/commands.py"
Task: "Integrate add_task_cmd with TaskService.add_task method in src/cli/commands.py"
Task: "Add success/error message display for add command in src/cli/commands.py"

# Then launch all test tasks for User Story 1:
Task: "Test add command with valid title only from CLI"
Task: "Test add command with valid title and description from CLI"
Task: "Test add command with empty title from CLI"
Task: "Verify task ID increments sequentially for multiple added tasks"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only - Add Tasks)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories) (T005-T017)
3. Complete Phase 3: User Story 1 (Add Tasks) (T018-T024)
4. **STOP and VALIDATE**: Test User Story 1 independently - can add tasks with titles and descriptions
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T017)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Complete Polish → Validate all quickstart.md items
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T017)
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Tasks) (T018-T024)
   - Developer B: User Story 2 (View Tasks) (T025-T032)
   - Developer C: User Story 3 (Update Tasks) (T033-T041)
   - Developer D: User Story 4 (Mark Complete) (T042-T051)
   - Developer E: User Story 5 (Delete Tasks) (T052-T058)
3. Stories complete and integrate independently
4. Team completes Polish phase together (T059-T065)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are OPTIONAL per specification - not included as tests were not explicitly requested
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total task count: 65 tasks
- Task count per user story:
  - Setup (Phase 1): 4 tasks (T001-T004)
  - Foundational (Phase 2): 13 tasks (T005-T017)
  - User Story 1 (Phase 3): 7 tasks (T018-T024)
  - User Story 2 (Phase 4): 8 tasks (T025-T032)
  - User Story 3 (Phase 5): 9 tasks (T033-T041)
  - User Story 4 (Phase 6): 10 tasks (T042-T051)
  - User Story 5 (Phase 7): 7 tasks (T052-T058)
  - Polish (Phase 8): 7 tasks (T059-T065)
- Parallel opportunities identified: 7 groups of parallelizable tasks
- MVP scope: Phase 1 + Phase 2 + Phase 3 (24 tasks) - delivers Add Tasks functionality
