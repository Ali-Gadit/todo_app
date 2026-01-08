---
name: fastapi-sqlmodel
description: Creates FastAPI backends with SQLModel for PostgreSQL. Covers async SQLAlchemy, Pydantic schemas, JWT authentication, and modular route organization.
---

# FastAPI + SQLModel Backend Skill

This skill creates production-ready FastAPI backends using SQLModel for database operations with async PostgreSQL support.

## Usage

When building the todo app backend, follow these patterns:

### Project Structure

```
backend/src/
├── main.py                     # FastAPI app initialization, CORS, lifespan
├── config.py                   # Settings via pydantic-settings
├── auth.py                     # JWT token creation/verification
├── middleware.py               # Logging, rate limiting, validation
├── db/
│   ├── __init__.py             # Engine, session, init_db()
│   └── connection.py           # Async database connection
├── models/
│   ├── __init__.py             # Model exports
│   ├── user.py                 # User model
│   └── task.py                 # Task model
├── schemas/
│   ├── __init__.py             # Schema exports
│   ├── auth.py                 # Auth-related Pydantic models
│   └── task.py                 # Task-related Pydantic models
└── routes/
    ├── __init__.py             # Route exports
    ├── auth.py                 # Auth endpoints
    ├── tasks.py                # Task CRUD endpoints
    └── users.py                # User endpoints
```

### Main Application Entry Point

```python
# backend/src/main.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routes import auth, tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan context manager."""
    await init_db()
    yield


app = FastAPI(
    title="Todo API",
    description="Backend API for Todo application",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}
```

### Database Connection (Async)

```python
# backend/src/db/__init__.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    from ..models import User, Task
    from sqlalchemy import text

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### SQLModel Models

```python
# backend/src/models/task.py
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", index=True)
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow),
    )

    user: Optional["User"] = Relationship(back_populates="tasks")
```

```python
# backend/src/models/user.py
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow),
    )

    tasks: list["Task"] = Relationship(back_populates="user")
```

### Pydantic Schemas

```python
# backend/src/schemas/task.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.task import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Task Routes with CRUD

```python
# backend/src/routes/tasks.py
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..db import get_db
from ..models import Task, User
from ..schemas import TaskCreate, TaskUpdate, TaskResponse


router = APIRouter()


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    status_filter: Optional[TaskStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all tasks for current user, optionally filtered by status."""
    query = select(Task).where(Task.user_id == current_user.id)
    if status_filter:
        query = query.where(Task.status == status_filter)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task."""
    db_task = Task(**task.model_dump(), user_id=current_user.id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single task."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a task (partial update)."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
```

## Validation Checklist

- [ ] FastAPI server starts on port 8000
- [ ] `/docs` (Swagger UI) is accessible
- [ ] Database tables created on startup
- [ ] CORS allows frontend origin
- [ ] JWT authentication protects endpoints
- [ ] User isolation works (users see only own tasks)
- [ ] Async database operations complete without errors

## Common Errors

| Error | Fix |
|-------|-----|
| Connection refused | Check DATABASE_URL and PostgreSQL is running |
| 401 Unauthorized | Verify JWT token is valid and not expired |
| 404 Task not found | Ensure task belongs to current user |
| Duplicate key | Check unique constraints on email/username |

## Related Skills

- `nextjs-app-router` - Frontend integration
- `better-auth` - JWT authentication
- `postgresql-neon` - Database configuration
