# Quickstart: Frontend Container

## Prerequisites
- Docker installed locally.
- Frontend source code available.

## Build the Image
From the project root:
```bash
docker build -t todo-frontend -f frontend/Dockerfile frontend/
```

## Run the Container
```bash
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_BACKEND_URL="http://your-backend-api:8000" \
  todo-frontend
```

## Verify
Access the application at `http://localhost:3000`.
Check that the UI loads and can communicate with the backend.

