# Tasks: SpecifyPlus MCP Server

**Input**: Design documents from `/specs/001-mcp-server/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only included if explicitly requested. This feature spec does not explicitly request tests, so test tasks are NOT included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `mcp-server/src/`, `mcp-server/tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create mcp-server directory at repository root
- [X] T002 Initialize Python project with UV in mcp-server/ (pyproject.toml)
- [X] T003 [P] Create src/ directory structure: src/models/, src/services/, src/lib/
- [X] T004 [P] Create tests/ directory structure: tests/unit/, tests/integration/, tests/fixtures/
- [X] T005 [P] Add dependencies to pyproject.toml: mcp, python-frontmatter, pytest, ruff
- [X] T006 [P] Create __init__.py files in src/, src/models/, src/services/, src/lib/, tests/
- [X] T007 [P] Create README.md with project description and setup instructions
- [X] T008 [P] Create .env.example with environment variable template (if needed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 Implement Handoff model in mcp-server/src/models/handoff.py (label, agent, prompt, send attributes with type hints)
- [X] T010 [P] Implement PromptTemplate model in mcp-server/src/models/template.py (content, has_arguments attributes, interpolate() and sanitize_arguments() methods)
- [X] T011 [P] Implement CommandDefinition model in mcp-server/src/models/command.py (name, file_path, description, handoffs, template attributes)
- [X] T012 Implement argument sanitizer in mcp-server/src/lib/sanitizer.py (escape $ and ` characters, preserve quotes/braces)
- [X] T013 [P] Implement YAML parser in mcp-server/src/lib/yaml_parser.py (parse frontmatter from markdown files using python-frontmatter)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Connect MCP Server to Any IDE (Priority: P1) 🎯 MVP

**Goal**: Enable MCP clients to connect, list all 13 commands, and see them as available prompts

**Independent Test**: Start server, connect from Claude Desktop, send prompts/list request, verify all 13 commands returned

### Implementation for User Story 1

- [X] T014 [P] [US1] Implement command loader service in mcp-server/src/services/command_loader.py (scan .claude/commands/*.md, parse YAML frontmatter, create CommandDefinition objects, return Dict[str, CommandDefinition])
- [X] T015 [P] [US1] Implement MCP handler for prompts/list in mcp-server/src/services/mcp_handler.py (list_prompts() function, return list of Prompt objects with name, description, arguments)
- [X] T016 [US1] Create main server entry point in mcp-server/src/server.py (create Server instance, register @server.list_prompts() handler, setup stdio transport with stdio_server())
- [X] T017 [US1] Add server startup logic in mcp-server/src/server.py (load commands at startup using command_loader, log loaded commands count, handle loading errors gracefully)
- [X] T018 [US1] Add error handling for missing .claude/commands/ directory (log warning, continue with empty commands dict)
- [X] T019 [US1] Add logging configuration in mcp-server/src/server.py (log to stderr, levels: INFO/DEBUG/WARNING/ERROR, include timestamps and context)

**Checkpoint**: At this point, User Story 1 should be fully functional - server starts, clients connect, all 13 commands listed

---

## Phase 4: User Story 2 - Execute SpecifyPlus Commands via Prompts (Priority: P2)

**Goal**: Enable prompt invocation with argument interpolation ($ARGUMENTS replacement)

**Independent Test**: Connect to server, invoke sp.specify with argument "Add user authentication", verify template returned with $ARGUMENTS replaced

### Implementation for User Story 2

- [X] T020 [P] [US2] Implement template processor service in mcp-server/src/services/template_processor.py (process_template() function that calls template.interpolate())
- [X] T021 [US2] Implement MCP handler for prompts/get in mcp-server/src/services/mcp_handler.py (get_prompt() function with name and arguments parameters)
- [X] T022 [US2] Register @server.get_prompt() handler in mcp-server/src/server.py (lookup command by name, extract arguments, call template_processor, return GetPromptResult)
- [X] T023 [US2] Add error handling for command not found in mcp-server/src/services/mcp_handler.py (return error with list of available commands)
- [X] T024 [US2] Add error handling for template processing failures (catch exceptions, return error with details)
- [X] T025 [US2] Handle empty arguments gracefully (default to empty string if not provided)
- [X] T026 [US2] Add invocation logging in mcp-server/src/services/mcp_handler.py (log command name, argument preview first 100 chars, timestamp)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - clients can list commands AND invoke them with arguments

---

## Phase 5: User Story 3 - Discover Command Metadata and Handoffs (Priority: P3)

**Goal**: Expose command descriptions and handoffs for discoverability

**Independent Test**: Send prompts/list request, verify descriptions present, verify handoffs accessible (if MCP supports metadata)

### Implementation for User Story 3

- [X] T027 [P] [US3] Add description field to Prompt objects in mcp-server/src/services/mcp_handler.py list_prompts() (extract from CommandDefinition.description)
- [X] T028 [US3] Expose handoffs via prompt arguments or description (document handoffs in prompt description or as metadata if MCP protocol supports)
- [X] T029 [US3] Verify all 13 commands have descriptions from YAML frontmatter (add validation in command_loader)
- [X] T030 [US3] Add handoff information to GetPromptResult if supported by MCP protocol (include handoffs in response metadata)

**Checkpoint**: All user stories should now be independently functional - clients can connect, invoke commands, and discover metadata

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T031 [P] Add comprehensive docstrings to all public functions (models, services, lib modules)
- [X] T032 [P] Run Ruff linter and fix PEP 8 violations across all source files
- [X] T033 [P] Add type hints verification with mypy or pyright (ensure all functions have complete type annotations)
- [X] T034 Update README.md with complete setup instructions, usage examples, and Claude Desktop configuration
- [X] T035 [P] Create test fixtures in mcp-server/tests/fixtures/sample_commands/ (sample .md files for testing)
- [X] T036 [P] Verify all 13 commands load successfully from .claude/commands/ (manual test or integration test)
- [X] T037 Test special characters handling (invoke with $VAR, `code`, {braces}, 'quotes' - verify sanitization works)
- [X] T038 Test concurrent connections (launch 10 clients simultaneously, verify all successful)
- [X] T039 Validate quickstart scenarios from specs/001-mcp-server/quickstart.md (5 scenarios)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires US1 complete for server infrastructure, but template interpolation is independent
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires US1 complete for MCP handlers, metadata enhancement is independent

**Note**: US2 and US3 have soft dependencies on US1 (need server running), but can be developed in parallel if server infrastructure from US1 is in place.

### Within Each User Story

- **User Story 1**: Command loader and MCP list handler before server entry point
- **User Story 2**: Template processor before get_prompt handler
- **User Story 3**: Metadata enhancements after list_prompts exists

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T008)
- All Foundational tasks marked [P] can run in parallel within their dependencies (T010-T011, T013)
- Within User Story 1: T014 and T015 can run in parallel
- Within User Story 2: T020 can run in parallel with other tasks
- Within User Story 3: T027-T028 can run in parallel
- Polish tasks marked [P] can run in parallel (T031-T033, T035-T036)

---

## Parallel Example: User Story 1

```bash
# Launch command loader and MCP handler together:
Task: "Implement command loader service in mcp-server/src/services/command_loader.py"
Task: "Implement MCP handler for prompts/list in mcp-server/src/services/mcp_handler.py"

# After both complete, create server entry point:
Task: "Create main server entry point in mcp-server/src/server.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Start server: `uv run python -m src.server`
   - Connect from Claude Desktop
   - Verify prompts/list returns all 13 commands
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T014-T019)
   - Developer B: User Story 2 (T020-T026)
   - Developer C: User Story 3 (T027-T030)
3. Stories complete and integrate independently

**Note**: In practice, US2 and US3 need US1 infrastructure (server, MCP handlers), so sequential implementation (P1 → P2 → P3) is more practical for this feature.

---

## Task Summary

**Total Tasks**: 39

**Task Count per Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 5 tasks (BLOCKING)
- Phase 3 (US1 - P1): 6 tasks 🎯 MVP
- Phase 4 (US2 - P2): 7 tasks
- Phase 5 (US3 - P3): 4 tasks
- Phase 6 (Polish): 9 tasks

**Parallel Opportunities Identified**: 15 tasks marked [P]

**Independent Test Criteria**:
- **US1**: Server starts, all 13 commands listed via prompts/list
- **US2**: Prompt invocation returns template with $ARGUMENTS replaced
- **US3**: Descriptions and handoffs visible in prompt metadata

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 19 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included (not explicitly requested in spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are absolute and follow mcp-server/ project structure from plan.md
- The 13 commands to load: sp.specify, sp.plan, sp.tasks, sp.implement, sp.clarify, sp.analyze, sp.checklist, sp.adr, sp.phr, sp.constitution, sp.git.commit_pr, sp.reverse-engineer, sp.taskstoissues
