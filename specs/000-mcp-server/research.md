# Research: Python MCP SDK for SpecifyPlus MCP Server

**Date**: 2026-01-04
**Feature**: 001-mcp-server
**Status**: Complete

## Research Questions

1. How to create an MCP server in Python?
2. How to expose prompts via the MCP protocol?
3. How to handle prompt arguments and template interpolation?
4. Best practices for YAML frontmatter parsing in Python?
5. Recommended Python version and dependencies?
6. How to handle concurrent client connections?
7. Standard MCP server patterns for stdio transport?

## Technology Decisions

### Decision 1: Python MCP SDK (mcp package)

**Rationale**: Official Python SDK for building MCP servers, provides standard implementations of the MCP protocol.

**Implementation Details**:
- Package: `mcp` (Python MCP SDK)
- Core classes: `Server`, `Prompt`, `PromptArgument`, `GetPromptResult`
- Decorators: `@server.list_prompts()`, `@server.get_prompt()`
- Transport: `stdio_server()` for standard input/output communication

**Example Usage**:
```python
from mcp.server import Server
from mcp.server.models.prompts import Prompt, PromptArgument, GetPromptResult

server = Server("my-server-name")

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [Prompt(name="example", description="Example prompt")]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
    # Return populated prompt template
    pass
```

**Alternatives Considered**:
- TypeScript MCP SDK: More mature, reference implementation, but user requested Python
- Custom MCP implementation: Too complex, reinventing the wheel

**Best Practices**:
- Use async/await throughout (MCP SDK is async-first)
- Handle errors gracefully with appropriate MCP error responses
- Log to stderr (stdout reserved for MCP protocol messages)

---

### Decision 2: python-frontmatter for YAML + Markdown Parsing

**Rationale**: Specialized library for parsing files with YAML frontmatter, handles both metadata extraction and content preservation.

**Implementation Details**:
- Package: `python-frontmatter`
- Usage: `frontmatter.load(file)` returns object with `.metadata` dict and `.content` string
- Handles YAML parsing errors gracefully

**Example Usage**:
```python
import frontmatter

# Load command file
with open('.claude/commands/sp.specify.md', 'r') as f:
    post = frontmatter.load(f)

description = post.metadata.get('description', '')
handoffs = post.metadata.get('handoffs', [])
template_content = post.content  # Markdown without frontmatter
```

**Alternatives Considered**:
- Manual parsing with pyyaml: More error-prone, must handle --- delimiters manually
- regex-based extraction: Fragile, doesn't handle edge cases

**Best Practices**:
- Validate YAML structure after parsing
- Provide default values for missing metadata fields
- Preserve exact template content (whitespace, formatting)

---

### Decision 3: Stdio Transport with Asyncio

**Rationale**: Standard MCP transport mechanism, works with Claude Desktop and most MCP clients. Uses process stdin/stdout for communication.

**Implementation Details**:
- Transport: `stdio_server()` from `mcp.server.stdio`
- Async I/O: Python asyncio for handling concurrent connections
- Protocol: JSON-RPC messages over stdio

**Example Usage**:
```python
from mcp.server.stdio import stdio_server
import asyncio

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Alternatives Considered**:
- SSE (Server-Sent Events) transport: Requires HTTP server, more complex
- WebSocket transport: Non-standard for MCP, added complexity

**Best Practices**:
- Use asyncio for all I/O operations
- Handle process termination gracefully (SIGINT, SIGTERM)
- Log all errors to stderr, not stdout

---

### Decision 4: Argument Sanitization Strategy

**Rationale**: Prevent template injection attacks while preserving user intent.

**Implementation Details**:
- Escape special characters: `$` (except in $ARGUMENTS), `` ` `` (backticks)
- Preserve safe characters: quotes, braces, brackets (safe in markdown)
- Simple string replacement: `template.replace("$ARGUMENTS", sanitized_input)`

**Security Considerations**:
- Dollar signs could reference environment variables: escape as `\$`
- Backticks could execute code in some contexts: escape as `` \` ``
- Other markdown syntax (bold, italic, links) is safe: preserve as-is

**Example**:
```python
def sanitize_arguments(arguments: str) -> str:
    """Escape special characters to prevent injection."""
    # Escape potential injection vectors
    sanitized = arguments.replace("$", "\\$")  # Prevent variable expansion
    sanitized = sanitized.replace("`", "\\`")  # Prevent code execution
    return sanitized
```

---

## Dependencies Summary

**Required Packages**:
- `mcp` - Python MCP SDK (core server functionality)
- `python-frontmatter` - YAML frontmatter + markdown parsing
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support

**Development Packages**:
- `ruff` - Linting and formatting (PEP 8 compliance)
- `mypy` or `pyright` - Type checking

**Python Version**: 3.11+ (for modern async features and type hints)

**UV Configuration** (pyproject.toml):
```toml
[project]
name = "specifyplus-mcp-server"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "mcp>=0.1.0",
    "python-frontmatter>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

---

## Concurrent Connection Handling

**Research Finding**: MCP protocol and Python asyncio handle concurrent connections naturally.

**How It Works**:
1. Each MCP client connection spawns an async task
2. Python asyncio scheduler manages task execution
3. Stdio transport uses async I/O (non-blocking reads/writes)
4. Command dictionary (in-memory) is read-only after startup → thread-safe

**Best Practices**:
- Load commands once at startup (immutable after load)
- Avoid shared mutable state across connections
- Use asyncio locks only if state must be shared (not needed for our case)
- Log each connection and disconnection for debugging

**Concurrency Pattern**:
```python
# Server automatically handles multiple connections
# Each connection gets its own async context
@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
    # This handler runs concurrently for multiple clients
    # No locks needed - commands dict is read-only
    cmd = commands[name]  # Safe: read-only access
    return cmd.template.interpolate(arguments.get("input", ""))
```

---

## Performance Considerations

**Startup Performance**:
- Load all 13 commands at startup: <1 second (small files)
- Parse YAML frontmatter: <10ms per file
- Total startup time: <5 seconds (well within SC-001 requirement)

**Invocation Performance**:
- String replacement (`$ARGUMENTS`): <1ms
- Template return: <10ms
- Total invocation time: <2 seconds (well within SC-002 requirement)

**Memory Usage**:
- 13 commands × ~5KB per template = ~65KB total
- Python overhead: ~10MB base
- Total memory footprint: <20MB (negligible)

---

## Error Handling Patterns

**Command Loading Errors**:
```python
for file_path in command_files:
    try:
        post = frontmatter.load(file_path)
        commands[name] = CommandDefinition(...)
    except yaml.YAMLError as e:
        logger.warning(f"Invalid YAML in {file_path}: {e}")
        # Skip command, continue loading others
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        # Skip command, continue loading others
```

**Invocation Errors**:
```python
@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
    if name not in commands:
        raise ValueError(f"Command '{name}' not found. Available: {list(commands.keys())}")

    try:
        content = commands[name].template.interpolate(arguments.get("input", ""))
        return GetPromptResult(description=commands[name].description, messages=[...])
    except Exception as e:
        logger.error(f"Interpolation failed for {name}: {e}")
        raise RuntimeError(f"Failed to process prompt: {e}")
```

---

## Conclusion

All research questions answered. Technology stack selected and justified:
- Python 3.11+ with MCP SDK for server implementation
- python-frontmatter for YAML + markdown parsing
- Stdio transport for standard MCP communication
- Asyncio for concurrent connection handling
- Simple argument sanitization for security

Ready to proceed with implementation. All decisions documented with rationale, alternatives considered, and best practices identified.
