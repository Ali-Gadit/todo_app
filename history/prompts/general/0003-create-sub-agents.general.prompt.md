---
id: "0003"
title: "Create specialized sub-agents for chatbot development"
stage: "general"
date_iso: "2026-01-09"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "002-todo-web-app"
user: "User"
command: "now make sub agents who will have these skills and do the work like an agent for chatbot who will have all the chatbot with agent skills like openai-agents-creater for agent , chatkit for agent ui , fastapi-chatbot , sql model and postgresql-neon skill for storing chats there and agents for all the things"
labels:
  - "agents"
  - "sub-agents"
  - "chatbot"
  - "specialization"
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_created:
  - ".claude/agents/chatbot-agent/agent.yaml"
  - ".claude/agents/auth-agent/agent.yaml"
  - ".claude/agents/mcp-agent/agent.yaml"
  - ".claude/agents/database-agent/agent.yaml"
  - ".claude/agents/INDEX.md"
files_modified: []
tests_run: []
tests_added: []
prompt_text: |
  now make sub agents who will have these skills and do the work like an agent for chatbot who will have all the chatbot with agent skills like openai-agents-creater for agent , chatkit for agent ui , fastapi-chatbot , sql model and postgresql-neon skill for storing chats there and agents for all the things
response_text: |
  Created 4 specialized sub-agents with their domains:

  **1. chatbot-agent** - Main orchestrator
  - Creates complete chatbots using all skills
  - Coordinates: agents, UI, backend, database, auth
  - Uses: openai-agents-creater, chatkit, fastapi, sqlmodel, postgresql-neon, better-auth, mcp-python-sdk

  **2. auth-agent** - Authentication specialist
  - JWT tokens, password hashing, protected routes
  - Uses: better-auth, fastapi-sqlmodel, postgresql-neon

  **3. mcp-agent** - MCP server specialist
  - Creates FastMCP servers with tools/resources/prompts
  - Connects agents to MCP servers
  - Uses: mcp-python-sdk, openai-agents-creater

  **4. database-agent** - Database specialist
  - SQLModel models, async connections, Neon config
  - CRUD routes, schema design
  - Uses: fastapi-sqlmodel, postgresql-neon

  Created INDEX.md with agent usage guide and coordination patterns.
outcome: "success"
evaluation:
  objectives_met: true
  code_quality: "production-ready agent configurations"
  coverage: "All skill domains covered by specialized agents"
---
