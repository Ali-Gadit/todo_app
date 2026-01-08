---
name: postgresql-neon
description: Configures PostgreSQL with Neon Serverless for production deployments. Covers asyncpg driver, connection pooling, and environment-based configuration.
---

# PostgreSQL + Neon Serverless Skill

This skill configures PostgreSQL database connections for the todo app using Neon Serverless or local PostgreSQL with async support.

## Usage

When setting up database connections, follow these patterns:

### Environment Configuration

```bash
# .env

# Local PostgreSQL
DATABASE_URL=postgresql://todo_user:todo_password@localhost:5432/todo_db

# Neon Serverless PostgreSQL (production)
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_db?sslmode=require

# Connection pool settings
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

### Neon-Specific Connection

For Neon Serverless, use the asyncpg driver with proper SSL configuration:

```python
# backend/src/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False

    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: str = "7d"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
```

### Async Database Engine

```python
# backend/src/db/connection.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from ..config import settings


def create_database_engine() -> AsyncEngine:
    """Create async database engine with connection pooling."""
    # For Neon, ssl is required
    if "neon.tech" in settings.DATABASE_URL:
        # Neon requires SSL
        engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            echo=settings.DEBUG,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
    else:
        # Local PostgreSQL
        engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            echo=settings.DEBUG,
            pool_size=5,
            max_overflow=10,
        )

    return engine


# Global engine instance
engine = create_database_engine()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

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

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
```

### Docker Compose for Local Development

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
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://todo_user:todo_password@postgres:5432/todo_db
      JWT_SECRET: your-secret-key-minimum-32-characters-long
      CORS_ORIGINS: http://localhost:3000
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY ./src ./src

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production image
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy built assets
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

### Frontend next.config.ts

```ts
// frontend/next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/:path*`,
      },
    ];
  },
};

export default nextConfig;
```

### Database Initialization Script

```python
# backend/src/db/init.py
"""Database initialization and migration utilities."""

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def init_database(database_url: str) -> None:
    """Initialize database with required extensions."""
    engine = create_async_engine(
        database_url.replace("postgresql://", "postgresql+asyncpg://"),
        echo=True,
    )

    async with engine.begin() as conn:
        # Enable UUID extension (useful for future features)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))

        # Create enums if using PostgreSQL enums
        await conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))

        await conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE task_priority AS ENUM ('low', 'medium', 'high');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))

    await engine.dispose()
    print("Database initialized successfully!")


if __name__ == "__main__":
    import sys
    database_url = sys.argv[1] if len(sys.argv) > 1 else "postgresql://todo_user:todo_password@localhost:5432/todo_db"
    asyncio.run(init_database(database_url))
```

## Validation Checklist

- [ ] PostgreSQL connects successfully (local or Neon)
- [ ] SSL works for Neon connections
- [ ] Connection pooling is configured
- [ ] Tables are created on startup
- [ ] Foreign key relationships work
- [ ] Docker compose starts all services

## Common Errors

| Error | Fix |
|-------|-----|
| Connection refused | Check PostgreSQL is running |
| SSL required for Neon | Add `?sslmode=require` to URL |
| Role does not exist | Create user in PostgreSQL |
| Database does not exist | Create database first |

## Related Skills

- `fastapi-sqlmodel` - Backend API
- `nextjs-app-router` - Frontend
- `better-auth` - User authentication
