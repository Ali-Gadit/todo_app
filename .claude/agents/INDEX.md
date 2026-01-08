# Claude Code Agents Index

This directory contains specialized sub-agents that can be invoked using the Task tool. Each agent focuses on a specific domain and has access to relevant skills.

## Available Agents

### 1. `chatbot-agent`
**Purpose:** Creates complete AI chatbots - orchestrates all skills

**What it does:**
- Builds end-to-end chatbot solutions
- Coordinates agent creation, UI, backend, database, and auth
- Uses: `openai-agents-creater`, `chatkit-frontend`, `fastapi-chatbot`, `fastapi-sqlmodel`, `postgresql-neon`, `better-auth`, `mcp-python-sdk`

**Invoke with:**
```bash
# Task tool (recommended)
/task subagent_type:chatbot-agent
```

### 2. `auth-agent`
**Purpose:** Implements authentication systems

**What it does:**
- JWT token management
- Password hashing with bcrypt
- User models with SQLModel
- Protected routes
- Registration/login flows

**Uses:** `better-auth`, `fastapi-sqlmodel`, `postgresql-neon`

### 3. `mcp-agent`
**Purpose:** Creates MCP servers and connects them to agents

**What it does:**
- Builds FastMCP servers
- Exposes tools, resources, and prompts
- Connects agents to MCP servers
- Supports stdio and HTTP transports

**Uses:** `mcp-python-sdk`, `openai-agents-creater`

### 4. `database-agent`
**Purpose:** Designs and implements PostgreSQL databases

**What it does:**
- Creates SQLModel models with relationships
- Sets up async database connections
- Configures Neon Serverless for production
- Generates CRUD routes

**Uses:** `fastapi-sqlmodel`, `postgresql-neon`

## How to Use

### Using Task Tool
```python
from claude_code import Task

# Create a chatbot
task = Task(
    subagent_type="chatbot-agent",
    prompt="Create a customer support chatbot with auth and chat history"
)

# Create auth system
auth_task = Task(
    subagent_type="auth-agent",
    prompt="Add JWT authentication with refresh tokens"
)

# Create MCP server
mcp_task = Task(
    subagent_type="mcp-agent",
    prompt="Create an MCP server for database operations"
)

# Design database
db_task = Task(
    subagent_type="database-agent",
    prompt="Design a schema for chat conversations with messages"
)
```

### Agent Coordination Example

```
User Request
     │
     ▼
┌─────────────────┐
│  chatbot-agent  │  ← Main orchestrator
│  (uses skills)  │
└────────┬────────┘
         │
         ├──► auth-agent ──────► Database
         │        │
         ├──► mcp-agent ──────► MCP Server
         │
         └──► database-agent ─► PostgreSQL
```

## Skill References

Each agent has access to skills in `.claude/skills/`:

| Skill | Used By | Purpose |
|-------|---------|---------|
| `openai-agents-creater` | chatbot, mcp | Agent creation |
| `chatkit-frontend` | chatbot | UI components |
| `fastapi-chatbot` | chatbot | Backend API |
| `fastapi-sqlmodel` | chatbot, database | ORM patterns |
| `postgresql-neon` | chatbot, auth, database | Database |
| `better-auth` | chatbot, auth | Authentication |
| `mcp-python-sdk` | chatbot, mcp | MCP servers |

## Best Practices

1. **Start with chatbot-agent** for complete solutions
2. **Use specialists** for focused tasks:
   - auth-agent for auth-only features
   - mcp-agent for MCP tools
   - database-agent for schema design
3. **Agents can delegate** to each other for complex tasks
4. **All code is production-ready** with proper patterns

## Creating New Agents

To add a new agent:
1. Create `agent.yaml` in `.claude/agents/{name}/`
2. Include:
   - `name`: Agent identifier
   - `description`: What it does
   - `system_prompt`: Detailed instructions with code patterns
3. Add skill references to `.claude/skills/`
