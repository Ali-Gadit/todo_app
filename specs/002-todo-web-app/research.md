# Research Findings: Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-06
**Source**: Context7 MCP Documentation

## Technology Stack Summary

| Layer | Technology | Version | Source |
|-------|------------|---------|--------|
| Frontend Framework | Next.js | 16+ | /vercel/next.js |
| Frontend Language | TypeScript | Latest | Next.js built-in |
| Frontend Styling | Tailwind CSS | Latest | Industry standard |
| Backend Framework | FastAPI | 0.128.0 | /fastapi/fastapi |
| ORM | SQLModel | 0.0.24 | /websites/sqlmodel_tiangolo |
| Database | Neon PostgreSQL | Serverless | Cloud provider |
| Authentication | Better Auth | 1.3.x | /better-auth/better-auth |

---

## Next.js 16 App Router Research

### Project Structure

Next.js 16 uses the App Router with a file-system based routing:

```
frontend/
├── src/
│   ├── app/              # App Router pages (file-system routing)
│   │   ├── page.tsx      # Homepage route
│   │   ├── layout.tsx    # Root layout
│   │   └── api/          # API routes
│   ├── components/       # React components
│   ├── lib/              # Utilities and API client
│   └── styles/           # Global styles (Tailwind)
├── package.json
└── tsconfig.json
```

### Server vs Client Components

**Server Components** (default):
- Render on the server
- Reduce bundle size
- Can access backend resources directly
- Use for: Initial page renders, data fetching

**Client Components**:
- Add `"use client"` directive at top
- Use for: User interactions, state, effects
- Can use hooks: useState, useEffect, useRouter

```typescript
// Server Component (default)
export default function Page() {
  return <h1>Hello, Next.js!</h1>;
}

// Client Component
"use client";
import { useState } from "react";
export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Authentication Flow

For Better Auth integration, use client-side components for forms:

```typescript
"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const email = formData.get("email");
    const password = formData.get("password");

    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      router.push("/dashboard");
    }
  }

  return <form onSubmit={handleSubmit}>{/* form fields */}</form>;
}
```

### UI/UX Best Practices for Modern Look

1. **Tailwind CSS**: Use utility-first styling for responsive design
2. **Colors**: Clean, modern color palettes (slate, gray, primary accent)
3. **Spacing**: Consistent spacing using Tailwind's scale
4. **Components**: Use shadcn/ui or similar for accessible components
5. **Feedback**: Loading states, success/error toasts

---

## FastAPI JWT Authentication Research

### JWT Authentication Setup

FastAPI supports JWT authentication via OAuth2PasswordBearer:

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(BaseModel):
    username: str
    email: str

# Dependency for getting current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = verify_token(token)  # Implement JWT verification
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Protected endpoint
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

### Reusable Dependencies Pattern

```python
# Define once, reuse everywhere
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/items/")
def read_items(user: CurrentUser):
    ...

@app.post("/items/")
def create_item(user: CurrentUser, item: Item):
    ...

@app.delete("/items/{item_id}")
def delete_item(user: CurrentUser, item_id: int):
    ...
```

### Security Best Practices

1. **Content-Type Validation**: FastAPI 0.65.2+ validates Content-Type header
2. **Password Hashing**: Use bcrypt or similar (never store plain text)
3. **Token Expiration**: Set reasonable expiration (7 days for this app)
4. **HTTPS**: Always use HTTPS in production

---

## SQLModel Research

### Model Definition Pattern

SQLModel combines SQLAlchemy and Pydantic:

```python
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# Base model (shared fields)
class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = False

# Table model (database)
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Relationship
    user: Optional["User"] = Relationship(back_populates="tasks")

# Create model (for POST requests)
class TaskCreate(TaskBase):
    pass

# Public model (for responses)
class TaskPublic(TaskBase):
    id: int

# Update model (for PUT/PATCH)
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

### Database Setup with FastAPI

```python
from sqlmodel import SQLModel, create_engine

# Neon PostgreSQL connection
DATABASE_URL = "postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/DBNAME?sslmode=require"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

### Relationships

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    hashed_password: str

    tasks: List["Task"] = Relationship(back_populates="user")
```

---

## Better Auth JWT Configuration Research

### Server-Side JWT Plugin Setup

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    jwt({
      algorithm: "HS256",
      expiresIn: "7d",
      issuer: "https://example.com",
      audience: ["https://api.example.com"],
    }),
  ],
});
```

### Bearer Token Plugin (Simpler Alternative)

```typescript
import { betterAuth } from "better-auth";
import { bearer } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    bearer({
      expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    }),
  ],
});
```

### Client-Side JWT Client

```typescript
import { createAuthClient } from "better-auth/client";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: "http://localhost:3000", // Your frontend URL
  plugins: [
    jwtClient()
  ]
});

// Get JWT token
const { data } = await authClient.jwt.getSession();
// or using bearer
const { data: tokenData } = await authClient.bearer.generate();

// Use in API calls
fetch("http://localhost:8000/api/tasks", {
  headers: {
    Authorization: `Bearer ${tokenData.accessToken}`,
  },
});
```

### API Authentication in FastAPI

The backend needs to verify JWT tokens from Better Auth:

```python
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token,
            key="YOUR_BETTER_AUTH_SECRET",  # Shared secret
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = await verify_jwt_token(credentials.credentials)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
```

---

## UI Design Guidelines for Modern Todo App

### Color Palette Recommendations

| Purpose | Color | Tailwind Class |
|---------|-------|----------------|
| Primary | Indigo | `bg-indigo-600` |
| Secondary | Slate | `text-slate-600` |
| Success | Emerald | `text-emerald-600` |
| Warning | Amber | `text-amber-600` |
| Error | Rose | `text-rose-600` |
| Background | Gray-50 | `bg-gray-50` |
| Card | White | `bg-white` |

### Component Layout

1. **Header**: Logo, user avatar, sign out button
2. **Main Content**:
   - Add Task form (prominent, easy access)
   - Task list (filter tabs: All/Pending/Completed)
   - Task items (clear status indicators)
3. **Responsive**: Single column on mobile, side-by-side on desktop

### UX Best Practices

1. **Empty States**: Show friendly message when no tasks
2. **Loading States**: Skeletons or spinners during fetch
3. **Error Handling**: Toast notifications for errors
4. **Optimistic Updates**: Update UI immediately, revert on error
5. **Keyboard Shortcuts**: Enter to submit, Escape to cancel

---

## Architecture Decision Summary

### Frontend (Next.js 16 + TypeScript + Tailwind)

- Use App Router for modern routing
- Server Components for data fetching
- Client Components for interactivity
- Better Auth for authentication
- Tailwind for clean, modern styling

### Backend (FastAPI + SQLModel + Neon PostgreSQL)

- RESTful API design
- JWT authentication with shared secret
- SQLModel for type-safe database operations
- Neon PostgreSQL for serverless persistence
- Dependency injection for auth and sessions

### Authentication Flow

1. User signs up/in via Better Auth on frontend
2. Better Auth issues JWT token
3. Frontend includes JWT in API requests
4. FastAPI verifies JWT using shared secret
5. Backend filters data by user ID from token

---

## References

1. Next.js Documentation: https://nextjs.org/docs
2. FastAPI Documentation: https://fastapi.tiangolo.com
3. SQLModel Documentation: https://sqlmodel.tiangolo.com
4. Better Auth Documentation: https://www.better-auth.com/docs
5. Tailwind CSS: https://tailwindcss.com/docs
