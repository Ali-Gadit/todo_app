---
name: fullstack-integration
description: Integrates Next.js frontend with FastAPI backend. Covers CORS, environment variables, API proxies, and Docker Compose orchestration.
---

# Full-Stack Integration Skill

This skill integrates the Next.js frontend with the FastAPI backend for a complete todo application deployment.

## Usage

When integrating frontend and backend services, follow these patterns:

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  src/app/                                             │  │
│  │  ├── layout.tsx (Providers wrapper)                  │  │
│  │  ├── page.tsx (Dashboard with ProtectedRoute)        │  │
│  │  ├── login/page.tsx                                  │  │
│  │  └── signup/page.tsx                                 │  │
│  │                                                        │  │
│  │  src/components/                                      │  │
│  │  ├── AddTaskForm.tsx                                  │  │
│  │  ├── TaskList.tsx                                     │  │
│  │  ├── TaskItem.tsx                                     │  │
│  │  ├── Header.tsx                                       │  │
│  │  └── auth/AuthForm.tsx                                │  │
│  │                                                        │  │
│  │  src/lib/                                             │  │
│  │  ├── api.ts (Axios client with interceptors)         │  │
│  │  └── auth.ts (AuthProvider + useAuth)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                              │
│              JWT Token       │       REST API               │
│                              ▼                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  src/                                                │  │
│  │  ├── main.py (App, CORS, Routers)                   │  │
│  │  ├── auth.py (JWT, bcrypt, get_current_user)        │  │
│  │  ├── config.py (pydantic-settings)                  │  │
│  │  ├── db/ (AsyncSession, init_db)                    │  │
│  │  ├── models/ (User, Task SQLModel)                  │  │
│  │  ├── schemas/ (Pydantic validation)                 │  │
│  │  └── routes/ (auth, tasks, users)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            PostgreSQL (Neon/Local)                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Environment Variables Coordination

```bash
# .env - Shared configuration

# Backend
DATABASE_URL=postgresql://todo_user:todo_password@localhost:5432/todo_db
JWT_SECRET=your-secret-key-minimum-32-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION=7d
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### CORS Configuration

```python
# backend/src/main.py (CORS section)
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

app = FastAPI(...)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # ["http://localhost:3000"]
    allow_credentials=True,  # Required for cookies/auth
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend API Client

```typescript
// frontend/src/lib/api.ts
import axios, { AxiosInstance, InternalAxiosRequestConfig } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Token manager
export const tokenManager = {
  getToken: () => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("auth_token");
  },
  setToken: (token: string) => {
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", token);
    }
  },
  removeToken: () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
    }
  },
};

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_URL}`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenManager.getToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenManager.removeToken();
      // Redirect to login
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  auth: {
    register: "/auth/register",
    login: "/auth/login",
    logout: "/auth/logout",
    me: "/auth/me",
  },
  tasks: {
    list: "/tasks",
    create: "/tasks",
    get: (id: number) => `/tasks/${id}`,
    update: (id: number) => `/tasks/${id}`,
    delete: (id: number) => `/tasks/${id}`,
    stats: "/tasks/stats/summary",
  },
  users: {
    me: "/users/me",
  },
};

export default apiClient;
```

### Task Components Integration

```tsx
// frontend/src/components/AddTaskForm.tsx
"use client";

import { useState } from "react";
import apiClient, { endpoints } from "@/lib/api";

interface AddTaskFormProps {
  onTaskCreated: () => void;
}

export function AddTaskForm({ onTaskCreated }: AddTaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"low" | "medium" | "high">("medium");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    try {
      await apiClient.post(endpoints.tasks.create, {
        title,
        description,
        priority,
      });
      setTitle("");
      setDescription("");
      setPriority("medium");
      onTaskCreated();
    } catch (error) {
      console.error("Failed to create task:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow">
      <div className="space-y-3">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          required
        />

        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add a description (optional)"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          rows={2}
        />

        <div className="flex gap-3">
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as typeof priority)}
            className="px-3 py-2 border border-gray-300 rounded-lg"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50"
          >
            {isLoading ? "Adding..." : "Add Task"}
          </button>
        </div>
      </div>
    </form>
  );
}
```

```tsx
// frontend/src/components/TaskList.tsx
"use client";

import { useEffect, useImperativeHandle, forwardRef } from "react";
import apiClient, { endpoints } from "@/lib/api";
import { TaskItem } from "./TaskItem";

interface Task {
  id: number;
  title: string;
  description: string | null;
  status: "pending" | "in_progress" | "completed";
  priority: "low" | "medium" | "high";
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  ref?: React.Ref<{ refreshTasks: () => void }>;
}

export const TaskList = forwardRef<{ refreshTasks: () => void }, TaskListProps>(
  function TaskList(_, ref) {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [filter, setFilter] = useState<"all" | "pending" | "in_progress" | "completed">("all");
    const [isLoading, setIsLoading] = useState(true);

    const fetchTasks = async () => {
      setIsLoading(true);
      try {
        const params = filter !== "all" ? { status: filter } : {};
        const response = await apiClient.get(endpoints.tasks.list, { params });
        setTasks(response.data);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
      } finally {
        setIsLoading(false);
      }
    };

    useEffect(() => {
      fetchTasks();
    }, [filter]);

    useImperativeHandle(ref, () => ({
      refreshTasks: fetchTasks,
    }));

    const handleTaskUpdate = () => {
      fetchTasks();
    };

    const filteredTasks = filter === "all"
      ? tasks
      : tasks.filter((t) => t.status === filter);

    return (
      <div>
        {/* Filter tabs */}
        <div className="flex gap-2 mb-4">
          {(["all", "pending", "in_progress", "completed"] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-3 py-1 rounded-lg text-sm ${
                filter === status
                  ? "bg-primary-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {status.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())}
            </button>
          ))}
        </div>

        {/* Task list */}
        {isLoading ? (
          <div className="text-center py-8">Loading tasks...</div>
        ) : filteredTasks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No tasks found. Create one above!
          </div>
        ) : (
          <div className="space-y-3">
            {filteredTasks.map((task) => (
              <TaskItem key={task.id} task={task} onUpdate={handleTaskUpdate} />
            ))}
          </div>
        )}
      </div>
    );
  }
);
```

### Docker Compose Full Stack

```yaml
# docker-compose.yml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: todo_postgres
    environment:
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_password
      POSTGRES_DB: todo_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todo_user -d todo_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: todo_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://todo_user:todo_password@postgres:5432/todo_db
      JWT_SECRET: ${JWT_SECRET:-your-secret-key-minimum-32-characters-long}
      CORS_ORIGINS: http://localhost:3000
      DEBUG: "false"
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo_frontend
    ports:
      - "3000:3000
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

### Development vs Production

**Development (separate processes):**
```bash
# Terminal 1 - Backend
cd backend
uvicorn src.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - PostgreSQL (or use Docker)
docker run -d --name todo_postgres \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_PASSWORD=todo_password \
  -e POSTGRES_DB=todo_db \
  -p 5432:5432 postgres:16-alpine
```

**Production (Docker Compose):**
```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Health Check Endpoints

```python
# backend/src/main.py
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"  # Could add DB ping here
    }
```

```tsx
// frontend - Health check hook
"use client";

export function useBackendHealth() {
  const [isHealthy, setIsHealthy] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
        setIsHealthy(response.ok);
      } catch {
        setIsHealthy(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  return isHealthy;
}
```

## Validation Checklist

- [ ] Frontend builds successfully (`npm run build`)
- [ ] Backend starts without errors (`uvicorn src.main:app`)
- [ ] CORS allows frontend origin
- [ ] API calls from frontend reach backend
- [ ] JWT tokens are validated on backend
- [ ] Database operations work end-to-end
- [ ] Docker Compose starts all services
- [ ] Health endpoints respond correctly

## Common Integration Issues

| Issue | Fix |
|-------|-----|
| CORS error | Add frontend origin to CORS_ORIGINS |
| 404 on API call | Check baseURL matches backend prefix |
| Token not sent | Verify Axios interceptor runs |
| DB connection fail | Check DATABASE_URL format |
| Port conflicts | Ensure ports 3000, 8000, 5432 are free |

## Related Skills

- `nextjs-app-router` - Frontend implementation
- `fastapi-sqlmodel` - Backend implementation
- `better-auth` - Authentication
- `postgresql-neon` - Database
