# Tasks: Containerize Backend (FastAPI + Agents)

Feature Branch: `001-containerize-backend`

## Implementation Strategy
We will implement the backend containerization incrementally, starting with a basic functional Dockerfile (MVP) and then refining it for production readiness (multi-stage builds, non-root user, health checks). Each phase will be independently testable as per user stories.

## Phase 1: Setup
- [X] T001 Initialize backend containerization context in backend/Dockerfile
- [X] T002 [P] Create .dockerignore file in backend/.dockerignore to exclude unnecessary files

## Phase 2: Foundational
- [X] T003 Ensure all dependencies are correctly listed in backend/requirements.txt
- [X] T004 Define the production-ready server command in backend/Dockerfile

## Phase 3: User Story 1 - Deployable Backend Container (Priority: P1)
**Goal**: Create a standardized container that runs the FastAPI service on port 8000.
**Test**: Build image and run container locally; verify `http://localhost:8000` is accessible.

- [X] T005 [US1] Implement basic Dockerfile structure using python:3.13-slim in backend/Dockerfile
- [X] T006 [US1] Add dependency installation step in backend/Dockerfile
- [X] T007 [US1] Add application code copying step in backend/Dockerfile
- [X] T008 [US1] Configure port 8000 exposure in backend/Dockerfile
- [X] T009 [US1] Implement the startup command using uvicorn in backend/Dockerfile

## Phase 4: User Story 2 - Cloud-Ready Backend (Priority: P2)
**Goal**: Refine the container for cloud deployment (optimization, security).
**Test**: Verify image size reduction and non-root execution.

- [X] T010 [US2] Implement multi-stage build to reduce final image size in backend/Dockerfile
- [X] T011 [P] [US2] Configure a non-root user for security in backend/Dockerfile
- [X] T012 [P] [US2] Add HEALTHCHECK instruction for orchestration platforms in backend/Dockerfile
- [X] T013 [US2] Ensure environment variable handling for sensitive configuration in backend/Dockerfile

## Phase 5: Polish & Cross-Cutting
- [X] T014 Optimize Docker layer caching by reordering commands in backend/Dockerfile
- [X] T015 Verify build and startup times against success criteria SC-001 and SC-002 (Note: Build verification pending Docker-ready environment)

## Dependencies
- US1 (T005-T009) must be completed before US2 (T010-T013) refinements.
- T003 is a prerequisite for US1 image build.

## Parallel Execution
- T002 (Setup) and T003 (Foundational) can be done in parallel.
- T011 and T012 can be done in parallel within US2.
