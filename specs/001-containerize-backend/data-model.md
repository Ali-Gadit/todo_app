# Data Model: Backend Entities

This feature documents the existing data model to ensure the containerized backend correctly handles all entities.

## Entities

### User
- **id**: Integer (Primary Key)
- **username**: String (Unique)
- **email**: String (Unique)
- **hashed_password**: String
- **created_at**: DateTime

### Task
- **id**: Integer (Primary Key)
- **title**: String
- **description**: String (Optional)
- **status**: Enum (pending, in_progress, completed)
- **priority**: Enum (low, medium, high)
- **user_id**: Integer (Foreign Key -> User)
- **created_at**: DateTime
- **updated_at**: DateTime

### Conversation
- **id**: String (Primary Key - ChatKit UUID)
- **user_id**: Integer (Foreign Key -> User)
- **created_at**: DateTime
- **updated_at**: DateTime

### Message
- **id**: String (Primary Key - ChatKit UUID)
- **conversation_id**: String (Foreign Key -> Conversation)
- **user_id**: Integer (Foreign Key -> User)
- **role**: String (user, assistant, tool_call)
- **content**: Text (Serialized JSON for tool calls)
- **created_at**: DateTime

## Relationships
- **User** has many **Tasks**
- **User** has many **Conversations**
- **Conversation** has many **Messages**
- **Message** belongs to a **User** and a **Conversation**
