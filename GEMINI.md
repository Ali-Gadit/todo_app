# todo_app Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-02

## Active Technologies
- Python 3.12+, TypeScript (Next.js 16+) (005-chatbot-ui-integration)
- Neon Serverless PostgreSQL. (005-chatbot-ui-integration)
- Python 3.13 + FastAPI, uvicorn, sqlmodel, asyncpg, psycopg2-binary, openai-agents, chatkit (001-containerize-backend)
- Neon PostgreSQL (runtime config via DATABASE_URL) (001-containerize-backend)
- TypeScript / Node.js 20 + Next.js 15.1.6, React 19, Tailwind CSS, Better Auth, ChatKit (006-containerize-frontend)
- N/A (Stateless) (006-containerize-frontend)

- Python 3.12+ (to match `openai-agents-python` requirements and project standards) (004-openai-agent-tools)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.12+ (to match `openai-agents-python` requirements and project standards): Follow standard conventions

## Recent Changes
- 006-containerize-frontend: Added TypeScript / Node.js 20 + Next.js 15.1.6, React 19, Tailwind CSS, Better Auth, ChatKit
- 006-containerize-frontend: Added [if applicable, e.g., PostgreSQL, CoreData, files or N/A]
- 001-containerize-backend: Added Python 3.13 + FastAPI, uvicorn, sqlmodel, asyncpg, psycopg2-binary, openai-agents, chatkit


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
