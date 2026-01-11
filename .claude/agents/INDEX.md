# Claude Code Agents Index

This directory contains specialized sub-agents that can be invoked using the Task tool. Each agent focuses on a specific domain and has access to relevant skills.

## Available Agents

### 1. `chatbot-architect`
**Purpose:** Creates complete AI chatbots - orchestrates all skills

**What it does:**
- Builds end-to-end chatbot solutions
- Coordinates agent creation, UI, backend, database, and auth
- Uses: `openai-agents-creater.skill.md`, `chatkit-js-react.skill.md`, `chatkit-python-server.skill.md`, `fastapi-sqlmodel.skill.md`, `postgresql-neon.skill.md`, `better-auth.skill.md`, `mcp-python-sdk.skill.md`

**Invoke with:**
```bash
# Task tool (recommended)
task subagent_type:chatbot-architect
```

### 2. `auth-specialist`
**Purpose:** Implements authentication systems

**What it does:**
- JWT token management
- Password hashing with bcrypt
- User models with SQLModel
- Protected routes
- Registration/login flows

**Uses:** `better-auth.skill.md`, `fastapi-sqlmodel.skill.md`, `postgresql-neon.skill.md`

### 3. `mcp-architect`
**Purpose:** Creates MCP servers and connects them to agents

**What it does:**
- Builds FastMCP servers
- Exposes tools, resources, and prompts
- Connects agents to MCP servers
- Supports stdio and HTTP transports

**Uses:** `mcp-python-sdk.skill.md`, `openai-agents-creater.skill.md`

### 4. `database-architect`
**Purpose:** Designs and implements PostgreSQL databases

**What it does:**
- Creates SQLModel models with relationships
- Sets up async database connections
- Configures Neon Serverless for production
- Generates CRUD routes

**Uses:** `fastapi-sqlmodel.skill.md`, `postgresql-neon.skill.md`

## How to Use

### Using Task Tool
```python
from claude_code import Task

# Create a chatbot
task = Task(
    subagent_type="chatbot-architect",
    prompt="Create a customer support chatbot with auth and chat history"
)

# Create auth system
auth_task = Task(
    subagent_type="auth-specialist",
    prompt="Add JWT authentication with refresh tokens"
)

# Create MCP server
mcp_task = Task(
    subagent_type="mcp-architect",
    prompt="Create an MCP server for database operations"
)

# Design database
db_task = Task(
    subagent_type="database-architect",
    prompt="Design a schema for chat conversations with messages"
)
```

### Agent Coordination Example

```
User Request
     │
     ▼
┌──────────────────────┐
│ chatbot-architect    │  ← Main orchestrator
│ (orchestrates stack) │
└────────┬─────────────┘
         │
         ├──► auth-specialist ────────► Database
         │          │
         ├──► mcp-architect ────────► MCP Server
         │
         └──► database-architect ──► PostgreSQL
```

## Skill References

Each agent has access to skills in `.claude/skills/`:

| Skill | Used By | Purpose |
|-------|---------|---------|
| `chatkit-js-react.skill.md` | chatbot-architect | React/JS frontend with ChatKit |
| `chatkit-python-server.skill.md` | chatbot-architect | Python/FastAPI backend with ChatKit streaming |
| `openai-agents-creater.skill.md` | chatbot-architect, agent-builder, mcp-architect | Agent creation and configuration |
| `fastapi-sqlmodel.skill.md` | chatbot-architect, auth-specialist, database-architect | SQLModel ORM with FastAPI patterns |
| `postgresql-neon.skill.md` | chatbot-architect, auth-specialist, database-architect | PostgreSQL and Neon Serverless |
| `better-auth.skill.md` | chatbot-architect, auth-specialist | JWT authentication and user management |
| `mcp-python-sdk.skill.md` | chatbot-architect, agent-builder, mcp-architect | MCP server creation and integration |
| `skill-creater.skill.md` | All agents | Skill creation and packaging framework |

## Best Practices

1. **Start with chatbot-architect** for complete AI chatbot solutions
2. **Use specialists** for focused domain tasks:
   - `auth-specialist` for authentication and user management
   - `mcp-architect` for creating MCP tool servers
   - `database-architect` for schema design and async database setup
   - `agent-builder` for multi-agent systems with handoffs
3. **Agents reference skills explicitly** - each agent frontmatter lists recommended skills
4. **All generated code is production-ready** with proper error handling and patterns

## Creating New Agents

To add a new agent:
1. Create `agent.yaml` in `.claude/agents/{name}/`
2. Include:
   - `name`: Agent identifier
   - `description`: What it does
   - `system_prompt`: Detailed instructions with code patterns
3. Add skill references to `.claude/skills/`
