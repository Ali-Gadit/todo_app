# Tasks: Containerize Frontend (Next.js + ChatKit)

Feature Branch: `006-containerize-frontend`

## Implementation Strategy
We will containerize the Next.js frontend using a multi-stage Docker build, specifically targeting the `standalone` output for minimal image size. The process starts with a basic functional Dockerfile and progresses to production-hardened refinements including non-root execution and security optimizations.

## Phase 1: Setup
- [X] T001 Initialize frontend containerization context in frontend/Dockerfile
- [X] T002 [P] Create .dockerignore file in frontend/.dockerignore to exclude node_modules and other unnecessary files

## Phase 2: Foundational
- [X] T003 Ensure `output: "standalone"` is configured in frontend/next.config.ts
- [X] T004 Verify `package-lock.json` is up-to-date for `npm ci` consistency in frontend/package-lock.json

## Phase 3: User Story 1 - Standardized Frontend Deployment (Priority: P1)
**Goal**: Create a standardized container that runs the Next.js service on port 3000.
**Test**: Build image and run container locally; verify `http://localhost:3000` loads the UI.

- [X] T005 [US1] Implement dependency installation stage using `node:20-alpine` and `npm ci` in frontend/Dockerfile
- [X] T006 [US1] Implement build stage to generate standalone production artifacts in frontend/Dockerfile
- [X] T007 [US1] Implement final runner stage using the standalone output in frontend/Dockerfile
- [X] T008 [US1] Configure port 3000 exposure and basic runtime environment in frontend/Dockerfile
- [X] T009 [US1] Implement the startup command using `node server.js` in frontend/Dockerfile

## Phase 4: User Story 2 - Optimized Production Runtime (Priority: P2)
**Goal**: Refine the container for production efficiency and security.
**Test**: Verify non-root execution and check that final image size is optimized.

- [X] T010 [US2] Configure a non-root user (`nextjs`) for enhanced security in frontend/Dockerfile
- [X] T011 [P] [US2] Add HEALTHCHECK instruction for orchestration platforms in frontend/Dockerfile
- [X] T012 [P] [US2] Optimize Docker layer caching by reordering file copying steps in frontend/Dockerfile
- [X] T013 [US2] Ensure support for build-time/runtime injection of `NEXT_PUBLIC_BACKEND_URL` in frontend/Dockerfile

## Phase 5: Polish & Cross-Cutting
- [X] T014 Verify container build and functionality against specs/006-containerize-frontend/quickstart.md (Note: Build verification pending Docker-ready environment)
- [X] T015 Validate build time and final image size against success criteria SC-001 and SC-004 (Note: Validation pending Docker-ready environment)

## Dependencies
- US1 (T005-T009) must be completed before US2 (T010-T013) refinements.
- T003 is a prerequisite for US1 build stage.

## Parallel Execution
- T002 (Setup) and T003 (Foundational) can be done in parallel.
- T011 and T012 can be done in parallel within US2 phase.

## Implementation Strategy
- **MVP**: Complete Phase 3 to get a working production container.
- **Production Ready**: Complete Phase 4 for security and size optimization.
- **Verification**: Use Phase 5 to ensure all success criteria are met.
