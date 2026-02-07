# Quickstart: Chatbot UI Integration

**Feature**: `005-chatbot-ui-integration`

## Prerequisites

1.  **Backend Dependencies**:
    ```bash
    cd backend
    uv pip install chatkit-python
    ```
2.  **Frontend Dependencies**:
    ```bash
    cd frontend
    npm install @openai/chatkit-react
    ```
3.  **Database**: Ensure `Conversation` and `Message` tables are created (run migrations).

## Testing the API

You can test the chat endpoint using `curl`:

```bash
curl -X POST http://localhost:8000/api/1/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What tasks do I have?"}'
```

## Running the Frontend

1.  Start the backend: `cd backend && uvicorn src.main:app --reload`
2.  Start the frontend: `cd frontend && npm run dev`
3.  Look for the agent icon in the bottom right corner of the browser.

```