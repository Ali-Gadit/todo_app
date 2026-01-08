---
id: "0001"
title: "Create full-stack skills for todo app"
stage: "general"
date_iso: "2026-01-09"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "002-todo-web-app"
user: "User"
command: "we have implemented the phase 2 so you have to make skills for them all properly ensure adding everything properly : Frontend Next.js 16+ (App Router) Backend Python FastAPI ORM SQLModel Database Neon Serverless PostgreSQL Authentication Better Auth"
labels:
  - "skills"
  - "fullstack"
  - "nextjs"
  - "fastapi"
  - "sqlmodel"
  - "postgresql"
  - "better-auth"
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_created:
  - ".claude/skills/nextjs-app-router/SKILL.md"
  - ".claude/skills/fastapi-sqlmodel/SKILL.md"
  - ".claude/skills/better-auth/SKILL.md"
  - ".claude/skills/postgresql-neon/SKILL.md"
  - ".claude/skills/fullstack-integration/SKILL.md"
files_modified: []
tests_run: []
tests_added: []
prompt_text: |
  we have implemented the phase 2 so you have to make skills for them all properly ensure adding everything properly : Frontend
  Next.js 16+ (App Router)
  Backend
  Python FastAPI
  ORM
  SQLModel
  Database
  Neon Serverless PostgreSQL
  Authentication
  Better Auth
response_text: |
  Created 5 comprehensive skills for the todo app full-stack implementation:

  1. **nextjs-app-router** - Next.js 16+ App Router patterns including:
     - File-based routing structure
     - Root layout with Providers wrapper
     - ProtectedRoute component
     - Axios API client with interceptors
     - Tailwind configuration

  2. **fastapi-sqlmodel** - FastAPI + SQLModel backend patterns:
     - Async database connection with asyncpg
     - SQLModel models (User, Task)
     - Pydantic schemas for validation
     - JWT-protected CRUD routes
     - CORS middleware configuration

  3. **better-auth** - JWT authentication patterns:
     - Backend JWT creation/verification
     - Password hashing with bcrypt
     - Protected route dependencies
     - Frontend AuthProvider hook
     - Login/register/logout flows

  4. **postgresql-neon** - PostgreSQL with Neon:
     - Environment configuration
     - Async engine setup with SSL for Neon
     - Docker Compose for local dev
     - Backend/frontend Dockerfiles
     - Database initialization

  5. **fullstack-integration** - Frontend-backend integration:
     - Architecture diagram
     - Environment variable coordination
     - API client configuration
     - Task components (AddTaskForm, TaskList)
     - Docker Compose orchestration
     - Development vs production workflows

  All skills include validation checklists, common errors, and references to related skills.
outcome: "success"
evaluation:
  objectives_met: true
  code_quality: "complete and production-ready"
  coverage: "all Phase 2 technologies covered"
---
