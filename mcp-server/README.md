# SpecifyPlus MCP Server

**Version**: 0.1.0
**Feature**: 001-mcp-server
**Status**: In Development

## Overview

The SpecifyPlus MCP Server exposes all 13 SpecifyPlus commands (sp.specify, sp.plan, sp.tasks, sp.implement, sp.clarify, sp.analyze, sp.checklist, sp.adr, sp.phr, sp.constitution, sp.git.commit_pr, sp.reverse-engineer, sp.taskstoissues) as MCP prompts accessible from any MCP-compatible client (Claude Desktop, IDEs, custom agents).

This enables universal access to the Spec-Driven Development workflow without requiring Claude Code CLI.

## Features

- **Universal Access**: Connect from Claude Desktop, any IDE, or custom MCP client
- **All Commands Available**: All 13 SpecifyPlus commands exposed as prompts
- **Argument Interpolation**: User input dynamically replaces $ARGUMENTS placeholder
- **Metadata Discovery**: Command descriptions and handoffs accessible via MCP protocol
- **Fast Performance**: <2s prompt invocation, <5s server startup
- **Concurrent Connections**: Supports 10+ simultaneous clients

## Prerequisites

- Python 3.11+ installed
- UV package manager installed
- `.claude/commands/*.md` files present (13 SpecifyPlus commands)
- MCP-compatible client (Claude Desktop, MCP test client, or custom client)

## Installation

```bash
# Navigate to mcp-server directory
cd mcp-server

# Install dependencies with UV
uv sync

# Verify installation
uv run python -m src.server --help
```

## Usage

### Start the MCP Server

```bash
uv run python -m src.server
```

The server will:
1. Load all commands from `.claude/commands/*.md`
2. Start listening on stdio (JSON-RPC over stdin/stdout)
3. Accept connections from MCP clients

### Connect with Claude Code

Add the server to your `.mcp.json` file at your project root:

```json
{
  "mcpServers": {
    "specifyplus": {
      "command": "uv",
      "args": ["run", "python", "-m", "src"],
      "cwd": "/absolute/path/to/mcp-server",
      "env": {}
    }
  }
}
```

**Important**: Replace `/absolute/path/to/mcp-server` with the actual absolute path to your mcp-server directory.

For this project, the configuration has been created at the repository root as `.mcp.json`.

### Connect from Claude Desktop

Add server configuration to Claude Desktop settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "specifyplus": {
      "command": "uv",
      "args": ["run", "python", "-m", "src"],
      "cwd": "/absolute/path/to/mcp-server"
    }
  }
}
```

Restart Claude Desktop, and the "specifyplus" server will appear in connected servers.

### Invoke Commands

From Claude Desktop:
- Type `/specifyplus sp.specify` to invoke a command
- Provide arguments when prompted
- The server returns the full prompt template with arguments interpolated

## Architecture

### Project Structure

```
mcp-server/
├── src/
│   ├── server.py           # Main MCP server entry point
│   ├── models/             # Data models (CommandDefinition, PromptTemplate, Handoff)
│   ├── services/           # Business logic (command_loader, template_processor, mcp_handler)
│   └── lib/                # Utilities (yaml_parser, sanitizer)
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── pyproject.toml          # UV project config
└── README.md               # This file
```

### Core Components

- **CommandDefinition**: Represents a loaded command with metadata
- **PromptTemplate**: Handles argument interpolation ($ARGUMENTS replacement)
- **Handoff**: Workflow progression suggestions
- **Command Loader**: Scans `.claude/commands/*.md` and loads commands at startup
- **MCP Handler**: Implements MCP protocol operations (prompts/list, prompts/get)

## Development

### Run Tests

```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest tests/unit/

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### Linting and Formatting

```bash
# Run Ruff linter
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

## Configuration

No configuration required. The server automatically:
- Loads commands from `.claude/commands/*.md` at startup
- Uses stdio transport for MCP communication
- Logs to stderr (configurable log level)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server fails to start | Check Python version (>=3.11), verify UV installed |
| No commands loaded | Verify `.claude/commands/` directory exists with `.md` files |
| Claude Desktop can't connect | Use absolute path in `cwd` field of server config |
| Slow response (>2s) | Check command file sizes (<10KB recommended) |

## Performance

- **Startup Time**: <5 seconds (loads 13 commands)
- **Invocation Time**: <2 seconds per prompt
- **Concurrent Connections**: 10+ clients supported
- **Memory Usage**: ~65KB for in-memory command storage

## Specifications

For detailed technical specifications, see:
- [Feature Specification](../specs/001-mcp-server/spec.md)
- [Implementation Plan](../specs/001-mcp-server/plan.md)
- [Data Model](../specs/001-mcp-server/data-model.md)
- [Quickstart Guide](../specs/001-mcp-server/quickstart.md)

## License

See repository root for license information.

## Related

- [SpecifyPlus Commands](../.claude/commands/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
