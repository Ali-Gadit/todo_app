# Data Model: Frontend Container Configuration

This feature documents the configuration model for the frontend container.

## Configuration Entities

### Environment Variables
- **NEXT_PUBLIC_BACKEND_URL**: (Build-time/Runtime) The public URL of the backend API.
- **PORT**: (Runtime) The port the application listens on (default: 3000).
- **NODE_ENV**: (Runtime) Set to `production` for optimized execution.

### Build Artifacts
- **Standalone Server**: The bundled Next.js server code.
- **Static Assets**: Pre-rendered pages, CSS, and client-side JavaScript.
- **Public Folder**: Images and other static files served directly.

## Relationships
- **Next.js App** depends on **NEXT_PUBLIC_BACKEND_URL** to communicate with the API.
- **Docker Image** bundles the **Standalone Server** and **Static Assets**.
