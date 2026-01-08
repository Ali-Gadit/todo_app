# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `002-todo-web-app` | **Date**: 2026-01-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-todo-web-app/spec.md`

## Summary

Transform the Phase I console todo app into a full-stack web application with:
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, Neon PostgreSQL
- **Auth**: Better Auth with JWT tokens
- **UI**: Modern, responsive, clean design with good UX

## Technical Context

**Language/Version**: TypeScript (Next.js), Python 3.11+ (FastAPI)
**Primary Dependencies**:
- Frontend: Next.js 16+, better-auth, tailwindcss
- Backend: FastAPI 0.128+, SQLModel 0.0.24, python-jose, passlib
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web browser (desktop, tablet, mobile)
**Project Type**: Web application (monorepo: frontend + backend)
**Performance Goals**:
- API response < 200ms p95
- Page load < 2s
- Smooth 60fps UI interactions
**Constraints**:
- JWT token expiration: 7 days
- Title max: 200 chars, Description max: 1000 chars
- User data isolation enforced
**Scale/Scope**: Single-tenant, individual user accounts

## Constitution Check

*Passed - All gates satisfied*

| Gate | Status | Notes |
|------|--------|-------|
| Spec-driven workflow | ✅ | Specification created and validated |
| Agentic implementation | ✅ | All code via Claude Code |
| Incremental delivery | ✅ | P1 features first (auth + CRUD) |
| Complexity justified | ✅ | Database persistence required for multi-user |
| Clean code standards | ✅ | TypeScript + Python with type hints |

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (tech research)
├── data-model.md        # Phase 1 output (entities)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── rest-endpoints.md
│   └── service-interface.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
todo_app/
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   │   ├── page.tsx        # Dashboard (protected)
│   │   │   ├── layout.tsx      # Root layout with auth
│   │   │   ├── globals.css     # Tailwind imports
│   │   │   ├── login/          # Login page
│   │   │   └── signup/         # Signup page
│   │   ├── components/         # React components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── AddTaskForm.tsx
│   │   │   ├── Header.tsx
│   │   │   └── ui/             # Reusable UI components
│   │   └── lib/                # Utilities
│   │       ├── api.ts          # API client
│   │       └── auth.ts         # Better Auth config
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                     # FastAPI application
│   ├── src/
│   │   ├── main.py             # FastAPI entry point
│   │   ├── models.py           # SQLModel models
│   │   ├── db.py               # Database connection
│   │   ├── auth.py             # JWT verification middleware
│   │   ├── schemas.py          # Pydantic schemas
│   │   └── routes/
│   │       └── tasks.py        # Task API endpoints
│   ├── requirements.txt
│   └── pyproject.toml
│
├── specs/
│   └── 002-todo-web-app/
│       └── ...
│
└── README.md
```

**Structure Decision**: Monorepo with separate frontend and backend directories. This follows the Spec-Kit Plus convention for full-stack projects and allows Claude Code to see and edit both codebases in a single context.

## Complexity Tracking

*No violations - all complexity justified by requirements*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Database persistence | Multi-user isolation required | In-memory (Phase I) insufficient |
| JWT authentication | Stateless API auth between frontend/backend | Session-based would require shared state |
| Better Auth library | Comprehensive auth with JWT plugin | Custom auth would require more code |

---

## Implementation Phases

### Phase 1: Backend Foundation

1. **Setup FastAPI project**
   - Initialize pyproject.toml with dependencies
   - Configure SQLModel and database connection
   - Set up CORS middleware

2. **Define data models**
   - User model (SQLModel table)
   - Task model (SQLModel table)
   - Pydantic schemas for API

3. **Implement JWT authentication**
   - Create auth.py with JWT verification
   - Dependency for extracting user from token
   - Protected route pattern

4. **Create task API endpoints**
   - GET /api/{user_id}/tasks - List tasks
   - POST /api/{user_id}/tasks - Create task
   - GET /api/{user_id}/tasks/{id} - Get task
   - PUT /api/{user_id}/tasks/{id} - Update task
   - PATCH /api/{user_id}/tasks/{id}/complete - Toggle
   - DELETE /api/{user_id}/tasks/{id} - Delete task

5. **Add error handling**
   - 401 for missing/invalid tokens
   - 403 for user ID mismatch
   - 404 for not found
   - 422 for validation errors

### Phase 2: Frontend Foundation

1. **Setup Next.js project**
   - Initialize with TypeScript and Tailwind
   - Configure better-auth client

2. **Create authentication pages**
   - Login page with form
   - Signup page with form
   - Protected route wrapper

3. **Build API client**
   - Fetch wrapper with JWT injection
   - Error handling
   - Types for responses

4. **Create UI components**
   - Header (logo, user info, sign out)
   - AddTaskForm (input, description)
   - TaskList (filter tabs, list)
   - TaskItem (checkbox, edit, delete)

5. **Implement dashboard**
   - Main page with task list
   - Responsive layout
   - Loading states

### Phase 3: Polish & Testing

1. **UI/UX improvements**
   - Modern color scheme (slate/indigo)
   - Smooth animations
   - Toast notifications
   - Empty states

2. **Testing**
   - Backend unit tests (pytest)
   - Frontend component tests (Vitest)
   - Integration tests

3. **Documentation**
   - Update README
   - API documentation
   - Deployment guide

---

## Key Technology Decisions

### Frontend (Next.js 16 + TypeScript + Tailwind)

| Decision | Rationale |
|----------|-----------|
| App Router | Modern Next.js routing with server components |
| Server Components | Default for data fetching, reduced bundle size |
| Client Components | Only where interactivity needed ("use client") |
| Tailwind CSS | Utility-first, responsive, modern look |
| Better Auth | JWT plugin, Next.js integration, easy setup |
| React Query | For data fetching and caching |

### Backend (FastAPI + SQLModel + PostgreSQL)

| Decision | Rationale |
|----------|-----------|
| FastAPI | High performance, automatic docs, type safety |
| SQLModel | Combines SQLAlchemy + Pydantic, FastAPI integration |
| Neon PostgreSQL | Serverless, no infrastructure management |
| JWT with HS256 | Stateless auth, shared secret with Better Auth |
| Dependency Injection | Clean auth and session management |

### Authentication Flow

1. User signs up via Better Auth (frontend)
2. Better Auth creates user and issues JWT
3. Frontend stores JWT and includes in API calls
4. FastAPI verifies JWT using BETTER_AUTH_SECRET
5. Backend extracts user_id from token
6. All queries filtered by user_id (enforced)

---

## UI Design Guidelines

### Color Palette

| Purpose | Color | Tailwind |
|---------|-------|----------|
| Primary | Indigo 600 | `bg-indigo-600` |
| Primary hover | Indigo 700 | `hover:bg-indigo-700` |
| Secondary text | Slate 600 | `text-slate-600` |
| Border | Slate 200 | `border-slate-200` |
| Background | Gray 50 | `bg-gray-50` |
| Card | White | `bg-white` |
| Success | Emerald 600 | `text-emerald-600` |
| Error | Rose 600 | `text-rose-600` |

### Layout Structure

```
┌─────────────────────────────────────────┐
│  Header (logo + user + sign out)        │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │  Add Task Form                  │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  Filter Tabs                    │    │
│  │  [All] [Pending] [Completed]    │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  Task List                      │    │
│  │  ┌───────────────────────────┐  │    │
│  │  │ [x] Task title        ✏️🗑  │  │    │
│  │  │     Description           │  │    │
│  │  └───────────────────────────┘  │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Responsive Breakpoints

- **Mobile** (< 768px): Single column, large touch targets
- **Tablet** (768px-1024px): Two columns, adjusted spacing
- **Desktop** (> 1024px): Full layout, comfortable spacing

---

## API Authentication

### JWT Token Format

```
Header: {
  "alg": "HS256",
  "typ": "JWT"
}
Payload: {
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iss": "https://example.com"
}
Signature: HMAC-SHA256(secret, header + "." + payload)
```

### Frontend Request Flow

```typescript
// Get token from Better Auth
const { data: { accessToken } } = await authClient.bearer.generate();

// Send request with token
fetch("http://localhost:8000/api/tasks", {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});
```

### Backend Verification

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    try:
        payload = jwt.decode(
            credentials.credentials,
            key=settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| API response time | < 200ms p95 | Backend logs |
| Page load time | < 2s | Lighthouse |
| Test coverage | > 80% | Coverage report |
| Auth flow | < 2 min | User testing |
| Mobile usability | 100% | Responsive tests |

---

## References

- Next.js Documentation: https://nextjs.org/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- Better Auth Documentation: https://www.better-auth.com/docs
- Tailwind CSS: https://tailwindcss.com/docs

---

*Plan generated with Context7 MCP research for latest best practices*
