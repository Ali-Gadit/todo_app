# Service Interface: Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-06

## Backend Service Interface (Python/FastAPI)

### TaskService Class

```python
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# ====================
# Request/Response Models
# ====================

class TaskCreate(BaseModel):
    """Request model for creating a task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    """Request model for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    """Response model for a task"""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    """Response for list of tasks"""
    tasks: List[TaskResponse]
    total: int
    pending: int
    completed: int

class ToggleCompleteRequest(BaseModel):
    """Request model for toggling completion"""
    completed: bool

# ====================
# Service Interface
# ====================

class TaskServiceProtocol:
    """
    Protocol defining the Task Service interface.
    All implementations must conform to this interface.
    """

    async def list_tasks(
        self,
        user_id: str,
        status: Optional[str] = "all",
        sort: str = "created",
        order: str = "desc"
    ) -> TaskListResponse:
        """
        List all tasks for a user with optional filtering and sorting.

        Args:
            user_id: The authenticated user's ID
            status: Filter by "all", "pending", or "completed"
            sort: Sort field - "created", "title", or "updated"
            order: Sort order - "asc" or "desc"

        Returns:
            TaskListResponse with tasks and counts
        """
        ...

    async def get_task(self, user_id: str, task_id: int) -> Optional[TaskResponse]:
        """
        Get a specific task by ID.

        Args:
            user_id: The authenticated user's ID
            task_id: The task ID to retrieve

        Returns:
            TaskResponse if found, None otherwise
        """
        ...

    async def create_task(self, user_id: str, data: TaskCreate) -> TaskResponse:
        """
        Create a new task for a user.

        Args:
            user_id: The authenticated user's ID
            data: Task creation data

        Returns:
            Created TaskResponse

        Raises:
            ValueError: If title is empty or too long
        """
        ...

    async def update_task(
        self,
        user_id: str,
        task_id: int,
        data: TaskUpdate
    ) -> Optional[TaskResponse]:
        """
        Update an existing task.

        Args:
            user_id: The authenticated user's ID
            task_id: The task ID to update
            data: Update data (all fields optional)

        Returns:
            Updated TaskResponse if found, None otherwise

        Raises:
            ValueError: If title is provided but empty
        """
        ...

    async def toggle_complete(
        self,
        user_id: str,
        task_id: int,
        completed: bool
    ) -> Optional[TaskResponse]:
        """
        Toggle task completion status.

        Args:
            user_id: The authenticated user's ID
            task_id: The task ID
            completed: New completion status

        Returns:
            Updated TaskResponse if found, None otherwise
        """
        ...

    async def delete_task(self, user_id: str, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            user_id: The authenticated user's ID
            task_id: The task ID to delete

        Returns:
            True if deleted, False if not found
        """
        ...
```

### AuthService Protocol

```python
from typing import Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

class AuthServiceProtocol:
    """
    Protocol for authentication service.
    Handles JWT verification for API requests.
    """

    async def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token and return payload.

        Args:
            token: JWT token from Authorization header

        Returns:
            Decoded token payload if valid, None otherwise
        """
        ...

    async def get_user_from_token(self, token: str) -> Optional[UserResponse]:
        """
        Get user from JWT token.

        Args:
            token: JWT token from Authorization header

        Returns:
            UserResponse if valid, None otherwise
        """
        ...
```

---

## Frontend API Client Interface (TypeScript)

### API Client Interface

```typescript
// Task types
interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListResponse {
  tasks: Task[];
  total: number;
  pending: number;
  completed: number;
}

interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

// API Client Protocol
interface TaskAPIClient {
  // List tasks with optional filters
  listTasks(params?: {
    status?: 'all' | 'pending' | 'completed';
    sort?: 'created' | 'title' | 'updated';
    order?: 'asc' | 'desc';
  }): Promise<TaskListResponse>;

  // Get single task
  getTask(id: number): Promise<Task>;

  // Create task
  createTask(data: CreateTaskRequest): Promise<Task>;

  // Update task (full update)
  updateTask(id: number, data: UpdateTaskRequest): Promise<Task>;

  // Toggle completion
  toggleComplete(id: number, completed: boolean): Promise<Task>;

  // Delete task
  deleteTask(id: number): Promise<void>;
}

// Auth Client Protocol
interface AuthClient {
  // Get current JWT token
  getToken(): Promise<string | null>;

  // Check if authenticated
  isAuthenticated(): boolean;

  // Get current user
  getCurrentUser(): Promise<User | null>;

  // Sign in
  signIn(email: string, password: string): Promise<void>;

  // Sign up
  signUp(email: string, password: string, name?: string): Promise<void>;

  // Sign out
  signOut(): Promise<void>;
}
```

### React Query Hooks Interface

```typescript
// Hooks interface for data fetching
interface UseTasksOptions {
  status?: 'all' | 'pending' | 'completed';
  sort?: 'created' | 'title' | 'updated';
  order?: 'asc' | 'desc';
}

interface TaskHooks {
  // List tasks
  useTasks(options: UseTasksOptions): {
    data: TaskListResponse | undefined;
    isLoading: boolean;
    error: Error | null;
  };

  // Single task
  useTask(id: number): {
    data: Task | undefined;
    isLoading: boolean;
    error: Error | null;
  };

  // Create task
  useCreateTask(): {
    mutate: (data: CreateTaskRequest) => void;
    isPending: boolean;
    error: Error | null;
  };

  // Update task
  useUpdateTask(): {
    mutate: (params: { id: number; data: UpdateTaskRequest }) => void;
    isPending: boolean;
    error: Error | null;
  };

  // Delete task
  useDeleteTask(): {
    mutate: (id: number) => void;
    isPending: boolean;
    error: Error | null;
  };
}
```

---

## Component Interface (React)

```typescript
// Task item component props
interface TaskItemProps {
  task: Task;
  onToggle: (id: number, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

// Task list component props
interface TaskListProps {
  tasks: Task[];
  onToggle: (id: number, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

// Add task form props
interface AddTaskFormProps {
  onSubmit: (data: CreateTaskRequest) => void;
  isLoading: boolean;
}

// Filter tabs props
interface FilterTabsProps {
  currentFilter: 'all' | 'pending' | 'completed';
  onFilterChange: (filter: 'all' | 'pending' | 'completed') => void;
  counts: {
    all: number;
    pending: number;
    completed: number;
  };
}

// Main dashboard props
interface DashboardProps {
  // All data loaded from hooks
}
```
