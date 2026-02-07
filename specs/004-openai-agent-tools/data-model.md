# Data Model: OpenAI Agent Tools

**Feature**: `004-openai-agent-tools`

## Entities

The primary entity is the **Task**, which already exists in the system. The tools will interact with this entity.

### Task (Existing)

- `id`: Integer (Primary Key)
- `user_id`: String (Indexed)
- `title`: String
- `description`: String (Optional)
- `completed`: Boolean (Mapped to 'status' in tool outputs)
- `created_at`: DateTime
- `updated_at`: DateTime

## Tool Interaction Models

These models define the structure of data exchanged between the Agent and the Tools.

### Add Task

**Input**:
- `user_id`: string
- `title`: string
- `description`: string (optional, default: "")

**Output**:
```json
{
  "task_id": 123,
  "status": "created",
  "title": "Buy milk"
}
```

### List Tasks

**Input**:
- `user_id`: string
- `status`: string (enum: "all", "pending", "completed", default: "all")

**Output**:
```json
[
  {
    "id": 1,
    "title": "Buy milk",
    "completed": false
  },
  {
    "id": 2,
    "title": "Call mom",
    "completed": true
  }
]
```

### Complete Task

**Input**:
- `user_id`: string
- `task_id`: integer

**Output**:
```json
{
  "task_id": 123,
  "status": "completed",
  "title": "Buy milk"
}
```

### Delete Task

**Input**:
- `user_id`: string
- `task_id`: integer

**Output**:
```json
{
  "task_id": 123,
  "status": "deleted",
  "title": "Buy milk"
}
```

### Update Task

**Input**:
- `user_id`: string
- `task_id`: integer
- `title`: string (optional)
- `description`: string (optional)

**Output**:
```json
{
  "task_id": 123,
  "status": "updated",
  "title": "New Title"
}
```
