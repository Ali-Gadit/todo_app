# REST API Endpoints: Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-06

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication

All endpoints require JWT authentication via Bearer token:

```
Authorization: Bearer <jwt_token>
```

### Token Validation Flow

1. Client sends request with `Authorization: Bearer <token>`
2. Server extracts token from header
3. Server verifies JWT signature using `BETTER_AUTH_SECRET`
4. Server extracts `user_id` from token payload
5. Server ensures `user_id` in URL matches token's user_id
6. Server filters all queries by `user_id`

### Error Responses (401 Unauthorized)

```json
{
  "detail": "Not authenticated"
}
```

```json
{
  "detail": "Invalid authentication credentials"
}
```

```json
{
  "detail": "Token expired"
}
```

---

## Task Endpoints

### GET /api/{user_id}/tasks

List all tasks for the authenticated user.

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | The authenticated user's ID (from JWT) |

**Query Parameters**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | String | No | "all" | Filter by status: "all", "pending", "completed" |
| `sort` | String | No | "created" | Sort field: "created", "title", "updated" |
| `order` | String | No | "desc" | Sort order: "asc", "desc" |

**Response (200 OK)**

```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_abc123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-06T10:00:00Z",
      "updated_at": "2026-01-06T10:00:00Z"
    }
  ],
  "total": 5,
  "pending": 3,
  "completed": 2
}
```

---

### POST /api/{user_id}/tasks

Create a new task for the authenticated user.

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | The authenticated user's ID (from JWT) |

**Request Body**

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation Rules**
| Field | Required | Type | Min | Max | Description |
|-------|----------|------|-----|-----|-------------|
| `title` | Yes | String | 1 | 200 | Task title (required) |
| `description` | No | String | 0 | 1000 | Optional description |

**Response (201 Created)**

```json
{
  "id": 6,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-06T12:00:00Z",
  "updated_at": "2026-01-06T12:00:00Z"
}
```

**Error Responses**

| Status | Detail |
|--------|--------|
| 400 | Validation error (missing title, title too long) |
| 401 | Not authenticated |
| 403 | User ID mismatch |
| 422 | Validation error |

---

### GET /api/{user_id}/tasks/{id}

Get a specific task by ID.

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | The authenticated user's ID (from JWT) |
| `id` | Integer | Yes | Task ID |

**Response (200 OK)**

```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z"
}
```

**Error Responses**

| Status | Detail |
|--------|--------|
| 401 | Not authenticated |
| 403 | User ID mismatch |
| 404 | Task not found |

---

### PUT /api/{user_id}/tasks/{id}

Update an existing task (full update).

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | The authenticated user's ID (from JWT) |
| `id` | Integer | Yes | Task ID |

**Request Body**

```json
{
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, butter, cheese"
}
```

**Validation Rules**
| Field | Required | Type | Min | Max | Description |
|-------|----------|------|-----|-----|-------------|
| `title` | No | String | 1 | 200 | Task title |
| `description` | No | String | 0 | 1000 | Optional description |
| `completed` | No | Boolean | - | - | Completion status |

**Response (200 OK)**

```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, butter, cheese",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T12:30:00Z"
}
```

**Error Responses**

| Status | Detail |
|--------|--------|
| 400 | Validation error (empty title) |
| 401 | Not authenticated |
| 403 | User ID mismatch |
| 404 | Task not found |

---

### PATCH /api/{user_id}/tasks/{id}/complete

Toggle task completion status.

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | The authenticated user's ID (from JWT) |
| `id` | Integer | Yes | Task ID |

**Request Body**

```json
{
  "completed": true
}
```

**Response (200 OK)**

```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T12:30:00Z"
}
```

---

### DELETE /api/{user_id}/tasks/{id}

Delete a task.

**Path Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | The authenticated user's ID (from JWT) |
| `id` | Integer | Yes | Task ID |

**Response (204 No Content)**

No content returned on successful deletion.

**Error Responses**

| Status | Detail |
|--------|--------|
| 401 | Not authenticated |
| 403 | User ID mismatch |
| 404 | Task not found |

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message describing the issue"
}
```

### Common Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | BAD_REQUEST | Invalid request data |
| 401 | UNAUTHORIZED | Missing or invalid JWT token |
| 403 | FORBIDDEN | User ID in URL doesn't match token |
| 404 | NOT_FOUND | Resource not found |
| 422 | UNPROCESSABLE_ENTITY | Validation error |
| 500 | INTERNAL_SERVER_ERROR | Server error |

---

## Rate Limiting

- Default: 100 requests per minute per user
- Include `X-RateLimit-Remaining` header in responses
- Return 429 Too Many Requests when limit exceeded

---

## OpenAPI/Swagger Documentation

Access interactive API docs at:
- Development: `http://localhost:8000/docs`
- Production: `https://api.yourdomain.com/docs`
