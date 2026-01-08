# Data Model: Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-06

## Overview

This document defines the data models for the Todo application using SQLModel. The models are designed to work with Neon PostgreSQL and integrate with Better Auth for authentication.

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────────┐
│    User     │ 1:N   │      Task       │
│─────────────┐       │─────────────────│
│ id (PK)     │◄──────│ id (PK)         │
│ email       │       │ user_id (FK)    │
│ name        │       │ title           │
│ password    │       │ description     │
│ created_at  │       │ completed       │
└─────────────┘       │ created_at      │
                      │ updated_at      │
                      └─────────────────┘
```

---

## User Entity

### Description
Represents an authenticated user in the system. User management is primarily handled by Better Auth on the frontend, but we maintain a user record for task association.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID / String | Primary Key, Indexed | Unique identifier (matches Better Auth user ID) |
| `email` | String | Unique, Not Null, Indexed | User's email address |
| `name` | String | Nullable | User's display name |
| `hashed_password` | String | Not Null | Password hash (Better Auth manages this) |
| `created_at` | DateTime | Not Null | Account creation timestamp |
| `updated_at` | DateTime | Not Null | Last update timestamp |

### SQLModel Definition

```python
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, max_length=255)
    email: str = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
```

### API Models (Pydantic)

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str  # Plain text for registration, will be hashed

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
```

---

## Task Entity

### Description
Represents a todo item belonging to a specific user. Each task is associated with exactly one user.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique task identifier |
| `user_id` | UUID / String | Foreign Key, Indexed, Not Null | Reference to owning user |
| `title` | String | Not Null, Max 200 chars | Task title (required) |
| `description` | String | Nullable, Max 1000 chars | Optional task details |
| `completed` | Boolean | Default: False | Task completion status |
| `created_at` | DateTime | Not Null | Task creation timestamp |
| `updated_at` | DateTime | Not Null | Last modification timestamp |

### SQLModel Definition

```python
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id", index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
```

### API Models (Pydantic)

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    pending: int
    completed: int
```

---

## Validation Rules

### Title Validation
- Minimum length: 1 character
- Maximum length: 200 characters
- Cannot be empty or whitespace-only

### Description Validation
- Maximum length: 1000 characters
- Optional field (can be null/empty)

### Completion Status
- Boolean field (true = completed, false = pending)
- Toggle via PATCH endpoint

---

## Database Schema (PostgreSQL)

```sql
-- Users table (Better Auth integration)
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

-- Indexes for performance
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_completed ON task(completed);
CREATE INDEX idx_task_user_completed ON task(user_id, completed);
CREATE INDEX idx_user_email ON "user"(email);
```

---

## State Transitions

### Task Status Flow

```
┌─────────────┐
│  PENDING    │◄───────────────┐
│  (default)  │                │
└──────┬──────┘                │
       │                       │
       │ Mark Complete         │ Mark Incomplete
       ▼                       │
┌─────────────┐                │
│  COMPLETED  │────────────────┘
└─────────────┘
```

### Timestamp Updates

- `created_at`: Set once at record creation
- `updated_at`: Updated on any field modification (title, description, completed)

---

## Relationships

### User -> Tasks (One-to-Many)
- One User can have many Tasks
- Tasks are deleted when User is deleted (CASCADE)
- All queries must filter by user_id for data isolation

```python
# Example: Get all tasks for a user
async def get_user_tasks(user_id: str, session: Session):
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
```

---

## Integration Notes

### Better Auth Integration

- User IDs from Better Auth are strings/UUIDs
- Password hashing handled by Better Auth
- Session management via JWT tokens
- Frontend sends JWT with each API request

### JWT Token Claims

The JWT token from Better Auth should contain:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iss": "https://your-domain.com"
}
```

Backend extracts `sub` (user_id) from token for filtering.
