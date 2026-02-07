# Research: Containerize Backend (FastAPI + Agents)

## Unknowns & Investigations

### 1. Base Image Selection
- **Decision**: Use `python:3.12-slim` (matching project standards from GEMINI.md) or `python:3.13-slim`.
- **Rationale**: `slim` images provide a good balance between size and functionality. `alpine` is smaller but often causes issues with C-extensions (like `psycopg2` or `cryptography`).
- **Findings**: Project GEMINI.md specifies "Python 3.12+". Current Dockerfile uses 3.13. Will stick to 3.13-slim but ensure compatibility.

### 2. Database Driver (psycopg2)
- **Decision**: Continue using `psycopg2-binary` for ease of installation, or switch to `psycopg2` with build-time dependencies.
- **Rationale**: `psycopg2-binary` is recommended for development/testing but `psycopg2` from source is often preferred for production. However, given the "no boilerplate" and "simple" constitutional goal, `psycopg2-binary` is acceptable.
- **Findings**: The current Dockerfile installs `gcc` and `g++` which are necessary if we were building from source. For `psycopg2-binary`, they might not be strictly needed if wheels are available.

### 3. Multi-stage Build Optimization
- **Decision**: Refine the multi-stage build to minimize the final image size.
- **Rationale**: The current `builder` stage copies site-packages and then the whole app. The final stage copies everything from builder.
- **Best Practice**: 
  1. Build stage: Install deps into a virtualenv or specific path.
  2. Final stage: Copy the virtualenv/packages and the source code.

### 4. Port Exposure and Runtime Configuration
- **Decision**: Expose 8000 and use environment variables for secrets.
- **Rationale**: Standard practice for FastAPI. Secrets should NEVER be in the image.

## Best Practices for FastAPI in Docker
- Use `JSON` logging for production observability.
- Use `HEALTHCHECK` instruction to allow orchestration platforms to monitor container health.
- Use `.dockerignore` to keep image small.
- Use non-root user for security (already in current Dockerfile).

## Patterns for Agents/MCP
- Ensure the container has network access to Groq/OpenAI APIs.
- No special system libraries found for `openai-agents` or `chatkit` beyond standard Python ones.
