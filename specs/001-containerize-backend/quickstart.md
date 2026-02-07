# Quickstart: Backend Container

## Prerequisites
- Docker installed locally.
- Backend source code available.

## Build the Image
From the project root:
```bash
docker build -t todo-backend -f backend/Dockerfile backend/
```

## Run the Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="your_db_url" \
  -e GROQ_API_KEY="your_key" \
  -e BETTER_AUTH_SECRET="your_secret" \
  todo-backend
```

## Verify
Access the API docs at `http://localhost:8000/docs`.

