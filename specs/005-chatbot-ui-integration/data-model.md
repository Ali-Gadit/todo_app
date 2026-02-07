# Data Model: Chatbot UI Integration

**Feature**: `005-chatbot-ui-integration`

## Entities

We are adding two new entities to handle chat history and session persistence.

### Conversation

Represents a single chat thread between a user and the AI agent.

- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key to User)
- `created_at`: DateTime
- `updated_at`: DateTime

**Relationships**:
- One-to-Many with **Message**.
- Many-to-One with **User**.

### Message

Represents a single turn (user prompt or agent response) within a conversation.

- `id`: Integer (Primary Key)
- `conversation_id`: Integer (Foreign Key to Conversation)
- `user_id`: Integer (Foreign Key to User)
- `role`: String (Enum: "user", "assistant")
- `content`: Text (The message body)
- `created_at`: DateTime

**Relationships**:
- Many-to-One with **Conversation**.
- Many-to-One with **User**.

## API Request/Response Models

### Chat Request (POST /api/{user_id}/chat)

```json
{
  "conversation_id": 123,
  "message": "Add a task to buy bread"
}
```

### Chat Response

```json
{
  "conversation_id": 123,
  "response": "Sure! I've added 'buy bread' to your tasks.",
  "tool_calls": [
    {
      "name": "add_task",
      "args": { "title": "buy bread" }
    }
  ]
}
```
