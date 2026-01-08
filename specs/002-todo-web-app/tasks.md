# Implementation Tasks: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Feature Branch**: `002-todo-web-app`
**Created**: 2026-01-06
**Priority Order**: US1 (Auth) → US2 (Create/View Tasks) → US3 (Update/Delete) → US4 (Mark Complete) → US5 (Responsive UI)

---

## Dependency Graph

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (JWT Auth, DB Models)
    │
    ├──────────────────────────────────────────────────────────┐
    │                                                          │
    ▼                                                          ▼
Phase 3: US1 (Auth)                                     Phase 5: US5 (Responsive UI)
    │                                                          │ (can be done in parallel)
    │                                                          │
    ▼                                                          │
Phase 4: US2 (Create/View Tasks) ──────► Phase 6: US3 (Update/Delete)
    │                                          │
    │                                          ▼
    └───────────────────────────────────► Phase 7: US4 (Mark Complete)
                                                  │
                                                  ▼
                                        Phase 8: Polish & Testing
```

## Independent Test Criteria by User Story

| User Story | Independent Test Criteria |
|------------|---------------------------|
| **US1 - Auth** | User can sign up, sign in, and access protected dashboard |
| **US2 - Create/View** | Authenticated user can create tasks and see them in list |
| **US3 - Update/Delete** | User can modify and remove their own tasks |
| **US4 - Mark Complete** | User can toggle task completion status |
| **US5 - Responsive UI** | App works on mobile, tablet, and desktop |

## Parallel Execution Opportunities

- **Frontend & Backend setup** can happen in parallel after Phase 1
- **US5 (Responsive UI)** can be implemented in parallel with other user stories
- **Component development** can run alongside API development

---

## Phase 1: Project Setup

**Goal**: Initialize both frontend and backend projects with required dependencies.

### Backend Setup

- [x] T001 Create backend directory structure `backend/src/` with `__init__.py`
- [x] T002 Create `backend/pyproject.toml` with FastAPI, SQLModel, and auth dependencies
- [x] T003 Create `backend/requirements.txt` with all Python dependencies
- [x] T004 Create `backend/.env.example` with environment variable template

### Frontend Setup

- [x] T005 Create `frontend/` directory structure `frontend/src/{app,components,lib}`
- [x] T006 Initialize Next.js project with `npx create-next-app@latest frontend --typescript --tailwind --eslint`
- [x] T007 Create `frontend/package.json` if not created by create-next-app
- [x] T008 Create `frontend/.env.local.example` with environment variable template

### Common Setup

- [x] T009 Create root `.env` template with shared BETTER_AUTH_SECRET
- [x] T010 Create root `docker-compose.yml` for local development

---

## Phase 2: Foundational Components

**Goal**: Create shared components needed by all user stories (database, auth, models).

### Database Foundation

- [x] T011 Create `backend/src/db.py` with SQLModel engine and session management
- [x] T012 Create `backend/src/models.py` with User SQLModel table model
- [x] T013 Create `backend/src/models.py` with Task SQLModel table model
- [x] T014 Create `backend/src/schemas.py` with Pydantic request/response schemas

### Authentication Foundation

- [x] T015 [P] Create `backend/src/auth.py` with JWT verification dependency
- [x] T016 [P] Create `backend/src/middleware.py` with CORS middleware configuration

### Frontend Foundation

- [x] T017 [P] Create `frontend/src/lib/api.ts` with API client and JWT injection
- [x] T018 [P] Create `frontend/src/lib/auth.ts` with Better Auth client configuration
- [x] T019 [P] Create `frontend/src/types/index.ts` with TypeScript interfaces

### Environment Configuration

- [x] T020 Create `backend/.env` with DATABASE_URL and BETTER_AUTH_SECRET
- [x] T021 Create `frontend/.env.local` with NEXT_PUBLIC_API_URL and BETTER_AUTH settings

---

## Phase 3: User Story 1 - Authentication (P1)

**Goal**: User registration and login functionality.

**Independent Test**: User can sign up with email/password, then sign in and access dashboard.

### Backend Auth Endpoints

- [x] T022 [US1] Create `backend/src/routes/auth.py` for authentication endpoints
- [x] T023 [US1] Implement user registration validation in `auth.py`
- [x] T024 [US1] Create JWT verification endpoint for frontend token validation

### Frontend Auth Pages

- [x] T025 [US1] Create `frontend/src/app/signup/page.tsx` signup form component
- [x] T026 [US1] Create `frontend/src/app/login/page.tsx` login form component
- [x] T027 [US1] Create `frontend/src/components/AuthForm.tsx` reusable auth form
- [x] T028 [US1] Create `frontend/src/components/Header.tsx` with user info and sign out

### Protected Routes

- [x] T029 [US1] Create `frontend/src/components/ProtectedRoute.tsx` route wrapper
- [x] T030 [US1] Protect `frontend/src/app/page.tsx` dashboard with auth check

### Integration

- [x] T031 [US1] Connect frontend signup to Better Auth API
- [x] T032 [US1] Connect frontend login to Better Auth and store JWT

---

## Phase 4: User Story 2 - Create and View Tasks (P1)

**Goal**: Core task CRUD operations - create and list tasks.

**Independent Test**: Authenticated user can create tasks and see them in their personal list.

### Backend Task Endpoints (Create/List)

- [x] T033 [US2] Create `backend/src/routes/tasks.py` router with CRUD endpoints
- [x] T034 [US2] Implement GET `/api/{user_id}/tasks` endpoint with filtering
- [x] T035 [US2] Implement POST `/api/{user_id}/tasks` endpoint with validation
- [x] T036 [US2] Implement GET `/api/{user_id}/tasks/{id}` endpoint for single task

### Frontend Task Components

- [x] T037 [US2] Create `frontend/src/components/AddTaskForm.tsx` with title/description inputs
- [x] T038 [US2] Create `frontend/src/components/TaskList.tsx` to display tasks
- [x] T039 [US2] Create `frontend/src/components/TaskItem.tsx` individual task display
- [x] T040 [US2] Create `frontend/src/components/FilterTabs.tsx` for All/Pending/Completed filter

### Dashboard Integration

- [x] T041 [US2] Connect `frontend/src/app/page.tsx` to API for task list
- [x] T042 [US2] Implement task creation flow in dashboard
- [x] T043 [US2] Add loading states and empty state messages

---

## Phase 5: User Story 3 - Update and Delete Tasks (P2)

**Goal**: Modify and remove existing tasks.

**Independent Test**: User can edit task title/description and delete tasks.

### Backend Update/Delete Endpoints

- [x] T044 [US3] Implement PUT `/api/{user_id}/tasks/{id}` endpoint in `tasks.py`
- [x] T045 [US3] Implement DELETE `/api/{user_id}/tasks/{id}` endpoint in `tasks.py`
- [x] T046 [US3] Add user ownership validation to update/delete operations

### Frontend Update/Delete UI

- [x] T047 [US3] Add edit mode to `frontend/src/components/TaskItem.tsx`
- [x] T048 [US3] Add delete button with confirmation to `TaskItem.tsx`
- [x] T049 [US3] Create `frontend/src/components/EditTaskModal.tsx` for inline editing

### Integration

- [x] T050 [US3] Connect edit functionality to PUT endpoint
- [x] T051 [US3] Connect delete functionality to DELETE endpoint with confirmation
- [x] T052 [US3] Add success/error toast notifications

---

## Phase 6: User Story 4 - Mark Tasks Complete (P2)

**Goal**: Toggle task completion status.

**Independent Test**: User can mark tasks complete/incomplete with visual feedback.

### Backend Toggle Endpoint

- [x] T053 [US4] Implement PATCH `/api/{user_id}/tasks/{id}/complete` endpoint
- [x] T054 [US4] Add completion status validation and update logic

### Frontend Completion UI

- [x] T055 [US4] Add checkbox to `frontend/src/components/TaskItem.tsx`
- [x] T056 [US4] Create visual distinction for completed vs pending tasks
- [x] T057 [US4] Add optimistic UI update for toggle action

### Integration

- [x] T058 [US4] Connect checkbox to PATCH endpoint
- [x] T059 [US4] Add filter by status functionality to TaskList
- [x] T060 [US4] Add task count statistics (pending/completed)

---

## Phase 7: User Story 5 - Responsive Web Interface (P3)

**Goal**: Ensure app works on all device sizes.

**Independent Test**: App interface adapts correctly to mobile, tablet, and desktop.

### Responsive Layout

- [x] T061 [US5] Create `frontend/src/app/globals.css` with Tailwind directives and base styles
- [x] T062 [US5] Update `frontend/src/app/layout.tsx` with responsive metadata
- [x] T063 [US5] Create responsive grid layout in `frontend/src/app/page.tsx`

### Mobile Optimizations

- [x] T064 [US5] Add touch-friendly sizing to `AddTaskForm.tsx`
- [x] T065 [US5] Add touch-friendly sizing to `TaskItem.tsx` buttons
- [x] T066 [US5] Implement mobile navigation in `Header.tsx`

### Component Responsiveness

- [x] T067 [US5] Make `TaskList.tsx` responsive (single column on mobile)
- [x] T068 [US5] Make `FilterTabs.tsx` scrollable on mobile
- [x] T069 [US5] Add responsive spacing and typography throughout

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: UI improvements, error handling, and testing.

### UI/UX Improvements

- [x] T070 Add toast notifications for success/error feedback
- [x] T071 Create empty state components for no tasks
- [x] T072 Add loading skeletons for task list loading
- [x] T073 Implement smooth transitions and animations

### Error Handling

- [x] T074 Add global error boundary in `frontend/src/app/layout.tsx`
- [x] T075 Implement retry logic for failed API requests
- [x] T076 Add network disconnection handling

### Testing

- [ ] T077 Create backend pytest tests for task endpoints
- [ ] T078 Create backend pytest tests for auth endpoints
- [ ] T079 Create frontend Vitest tests for components
- [ ] T080 Create integration tests for user flows

### Documentation

- [ ] T081 Update root `README.md` with setup instructions
- [ ] T082 Create `API.md` with endpoint documentation
- [ ] T083 Create `DEPLOYMENT.md` with production deployment guide

---

## Task Summary

| Phase | User Story | Task Count | Description |
|-------|------------|------------|-------------|
| 1 | - | 10 | Project Setup |
| 2 | - | 10 | Foundational Components |
| 3 | US1 (Auth) | 12 | Authentication |
| 4 | US2 (Create/View) | 11 | Create & View Tasks |
| 5 | US3 (Update/Delete) | 9 | Update & Delete Tasks |
| 6 | US4 (Mark Complete) | 8 | Mark Tasks Complete |
| 7 | US5 (Responsive UI) | 9 | Responsive Web Interface |
| 8 | - | 8 | Polish & Testing |
| **Total** | - | **77** | All Tasks |

---

## Suggested MVP Scope

For Minimum Viable Product, implement through **Phase 4 (US2)**:
- User authentication (US1)
- Create and view tasks (US2)

This delivers:
- User accounts with secure login
- Personal task management
- Persistent storage

The remaining phases (US3-US5) can be added incrementally.

---

## File Paths Reference

### Backend Files

| Task | File Path |
|------|-----------|
| T001-T004 | `backend/src/`, `backend/pyproject.toml`, `backend/requirements.txt` |
| T011 | `backend/src/db.py` |
| T012 | `backend/src/models.py` (User model) |
| T013 | `backend/src/models.py` (Task model) |
| T014 | `backend/src/schemas.py` |
| T015 | `backend/src/auth.py` |
| T016 | `backend/src/middleware.py` |
| T022-T024 | `backend/src/routes/auth.py` |
| T033-T036 | `backend/src/routes/tasks.py` (GET, POST, GET single) |
| T044-T046 | `backend/src/routes/tasks.py` (PUT, DELETE) |
| T053-T054 | `backend/src/routes/tasks.py` (PATCH toggle) |

### Frontend Files

| Task | File Path |
|------|-----------|
| T005-T010 | `frontend/src/`, `frontend/package.json` |
| T017 | `frontend/src/lib/api.ts` |
| T018 | `frontend/src/lib/auth.ts` |
| T019 | `frontend/src/types/index.ts` |
| T025 | `frontend/src/app/signup/page.tsx` |
| T026 | `frontend/src/app/login/page.tsx` |
| T027 | `frontend/src/components/AuthForm.tsx` |
| T028 | `frontend/src/components/Header.tsx` |
| T029 | `frontend/src/components/ProtectedRoute.tsx` |
| T037 | `frontend/src/components/AddTaskForm.tsx` |
| T038 | `frontend/src/components/TaskList.tsx` |
| T039 | `frontend/src/components/TaskItem.tsx` |
| T040 | `frontend/src/components/FilterTabs.tsx` |
| T047-T049 | `frontend/src/components/EditTaskModal.tsx` |
| T061 | `frontend/src/app/globals.css` |
| T062 | `frontend/src/app/layout.tsx` |

---

## Implementation Strategy

### MVP First (Phases 1-4)
1. Set up project structure (T001-T010)
2. Create database and auth foundation (T011-T021)
3. Implement user authentication (T022-T032)
4. Implement task creation and viewing (T033-T043)

### Incremental Delivery
- After MVP: Add update/delete (US3)
- After CRUD: Add completion toggle (US4)
- Throughout: Refine responsive UI (US5)
- Final: Polish, testing, documentation (Phase 8)
