# Research: Containerize Frontend (Next.js + ChatKit)

## Unknowns & Investigations

### 1. Base Image Selection
- **Decision**: Use `node:20-alpine`.
- **Rationale**: Alpine-based Node.js images are significantly smaller and commonly used for Next.js applications. `libc6-compat` is often required for some native dependencies.
- **Findings**: The current Dockerfile already uses `node:20-alpine`, which is a good standard choice.

### 2. Next.js Standalone Output
- **Decision**: Leverage `output: "standalone"` in `next.config.ts`.
- **Rationale**: This feature automatically bundles only the necessary files for production, drastically reducing image size by excluding devDependencies and unnecessary source files.
- **Findings**: `next.config.ts` already has `output: "standalone"`, and the current Dockerfile is designed to use it (`COPY --from=builder /app/.next/standalone ./`).

### 3. Environment Variable Injection
- **Decision**: Use build-time arguments (`ARG`) for `NEXT_PUBLIC_*` variables and runtime environment variables (`ENV`) for server-side configurations.
- **Rationale**: `NEXT_PUBLIC_` variables are inlined at build time in Next.js. Server-side variables can be injected at runtime.
- **Findings**: We need to ensure `NEXT_PUBLIC_BACKEND_URL` (if used) is handled correctly during `npm run build`.

### 4. Package Manager Consistency
- **Decision**: Use `npm ci` for deterministic dependency installation.
- **Rationale**: Ensures the exact versions from `package-lock.json` are installed, preventing subtle bugs.
- **Findings**: Current Dockerfile uses `npm ci`, which is best practice.

## Best Practices for Next.js in Docker
- **Multi-stage builds**: Already implemented, separates build environment from runtime.
- **Non-root user**: Already implemented (`nextjs` user).
- **Standalone output**: Crucial for small images.
- **Caching**: Ensure `node_modules` are cached effectively by copying only `package.json` first.

## Patterns for ChatKit
- ChatKit-react components are client-side; they will be bundled during `next build`.
- Ensure the production container can reach the backend API (configurable via env var).
