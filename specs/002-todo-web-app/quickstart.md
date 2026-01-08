# Quickstart Guide: Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-06

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Python 3.11+ and pip
- Git
- Neon PostgreSQL account (free tier)

---

## Environment Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git checkout 002-todo-web-app

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

### 2. Environment Variables

Create `.env` file in both frontend and backend directories:

**Backend (.env)**
```bash
# Database (Neon PostgreSQL)
DATABASE_URL="postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/DBNAME?sslmode=require"

# Authentication (shared secret)
BETTER_AUTH_SECRET="your-secret-key-min-32-chars"

# JWT Settings
JWT_ALGORITHM="HS256"
JWT_EXPIRATION="7d"

# CORS
CORS_ORIGINS="http://localhost:3000"
```

**Frontend (.env)**
```bash
# API URL
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Better Auth
BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_SECRET="your-secret-key-min-32-chars"
BETTER_AUTH_LOGGER="false"
```

---

## Running the Application

### Start the Backend (Terminal 1)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend runs at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Start the Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:3000

---

## Development Commands

### Backend

```bash
# Run development server
uvicorn main:app --reload --port 8000

# Run tests
pytest

# Type checking
pyright

# Linting
ruff check .
```

### Frontend

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Type checking
npx tsc --noEmit

# Linting
npm run lint
```

---

## Project Structure

```
todo_app/
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/                 # App Router pages
│   │   │   ├── page.tsx         # Dashboard
│   │   │   ├── layout.tsx       # Root layout
│   │   │   ├── globals.css      # Global styles
│   │   │   ├── login/           # Login page
│   │   │   └── signup/          # Signup page
│   │   ├── components/          # React components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── AddTaskForm.tsx
│   │   │   └── Header.tsx
│   │   └── lib/                 # Utilities
│   │       ├── api.ts           # API client
│   │       └── auth.ts          # Auth utilities
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                     # FastAPI application
│   ├── src/
│   │   ├── main.py              # Entry point
│   │   ├── models.py            # SQLModel models
│   │   ├── db.py                # Database connection
│   │   ├── auth.py              # JWT verification
│   │   └── routes/
│   │       └── tasks.py         # Task API routes
│   ├── requirements.txt
│   └── pyproject.toml
│
├── specs/                       # Specifications
│   └── 002-todo-web-app/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       └── contracts/
│           ├── rest-endpoints.md
│           └── service-interface.md
│
└── README.md
```

---

## Key Files Reference

### Backend Entry Point (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .db import create_db_and_tables
from .routes import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Todo API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Frontend API Client (lib/api.ts)

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getToken(): Promise<string> {
  const token = await authClient.getToken();
  if (!token) throw new Error("Not authenticated");
  return token;
}

export const api = {
  async listTasks(filters?: TaskFilters) {
    const token = await getToken();
    const params = new URLSearchParams(filters as Record<string, string>);
    const res = await fetch(`${API_URL}/api/tasks?${params}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch tasks");
    return res.json();
  },

  async createTask(data: CreateTaskRequest) {
    const token = await getToken();
    const res = await fetch(`${API_URL}/api/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create task");
    return res.json();
  },

  // ... other methods
};
```

---

## Database Schema Setup

The database tables are automatically created on startup:

```sql
-- Users table
CREATE TABLE "user" (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tasks table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_completed ON task(completed);
```

---

## Testing the Application

### 1. Sign Up

1. Open http://localhost:3000
2. Click "Sign Up"
3. Enter email and password (8+ characters)
4. Submit and verify email

### 2. Create Tasks

1. After signing in, you see the dashboard
2. Type a task title in the input field
3. Optionally add a description
4. Press Enter or click "Add"
5. Task appears in the list

### 3. Manage Tasks

- **Complete**: Click the checkbox or task
- **Edit**: Click the edit icon
- **Delete**: Click the delete icon
- **Filter**: Use the tabs (All/Pending/Completed)

---

## Troubleshooting

### Database Connection Failed

```
Error: Could not connect to database
```

**Solution**:
1. Check DATABASE_URL in .env
2. Verify Neon PostgreSQL credentials
3. Ensure SSL mode is "require"

### JWT Token Invalid

```
401 Unauthorized: Invalid authentication credentials
```

**Solution**:
1. Ensure BETTER_AUTH_SECRET matches in frontend and backend
2. Check that token hasn't expired
3. Verify token is being sent with requests

### CORS Error

```
Access to fetch blocked by CORS policy
```

**Solution**:
1. Add origin to CORS_ORIGINS in backend
2. Check that frontend URL matches exactly

### Frontend Build Failed

```
Module not found: Can't resolve 'better-auth'
```

**Solution**:
1. Run `npm install` in frontend directory
2. Check package.json has correct dependencies
3. Delete node_modules and reinstall

---

## Next Steps

1. **Implement P1 Features**: User auth + Task CRUD
2. **Run Tests**: Verify all functionality works
3. **Deploy**: Set up production environment
4. **Phase III**: Add AI chatbot integration
