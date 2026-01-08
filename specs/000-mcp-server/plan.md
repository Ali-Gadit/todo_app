# Implementation Plan: SpecifyPlus MCP Server

**Branch**: `001-mcp-server` | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-server/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an MCP (Model Context Protocol) server in Python that exposes all 13 SpecifyPlus commands (sp.specify, sp.plan, sp.tasks, etc.) as prompts accessible from any MCP-compatible client. The server reads command definitions from `.claude/commands/*.md` files, parses YAML frontmatter for metadata, and enables prompt invocation with argument interpolation. This enables universal access to the Spec-Driven Development workflow from Claude Desktop, IDEs, or custom agents without requiring Claude Code CLI.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: mcp (Python MCP SDK), pyyaml (YAML parsing), python-frontmatter (markdown + frontmatter parsing)
**Storage**: File-based (read command templates from `.claude/commands/*.md` at startup)
**Testing**: pytest (unit and integration tests)
**Target Platform**: Cross-platform (Linux, macOS, Windows) - runs as stdio MCP server
**Project Type**: single (standalone MCP server application)
**Performance Goals**: <2s prompt invocation, <5s server startup, support 10+ concurrent clients
**Constraints**: Stateless server (no session storage), must preserve exact template content, argument sanitization required
**Scale/Scope**: 13 commands, local deployment initially, designed for single-user or small team usage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Clean Code & Testing Discipline (Constitution Principle V)

- ✅ **Type hints**: MANDATORY for all functions - will use Python type hints throughout
- ✅ **PEP 8 compliance**: Will use Ruff for linting and formatting
- ✅ **Docstrings**: REQUIRED for all public functions, classes, modules
- ✅ **Testing**: pytest for unit and integration tests

### Progressive Complexity with Justification (Constitution Principle IV)

- ✅ **Justified complexity**: MCP server adds complexity justified by universal access requirement
- ✅ **Simpler alternative rejected**: Claude Code CLI works but requires CLI environment; MCP server enables IDE/agent integration
- ✅ **No over-engineering**: Simple file-based command loading, no database, no caching (commands loaded at startup)

### Spec-Driven Development (Constitution Principle I)

- ✅ **Specification complete**: spec.md includes prioritized user stories (P1-P3), functional requirements (FR-001 to FR-012), success criteria
- ✅ **Planning phase**: This plan document following Spec-Driven workflow

**Gate Status**: ✅ PASSED - All constitutional principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-server/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Python MCP SDK research
├── data-model.md        # Phase 1 output - Entity models
├── quickstart.md        # Phase 1 output - Testing scenarios
├── contracts/           # Phase 1 output - MCP protocol contracts
│   └── mcp-prompts.yaml # Prompt definitions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py           # Main MCP server entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── command.py      # CommandDefinition model
│   │   ├── template.py     # PromptTemplate model
│   │   └── handoff.py      # Handoff model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── command_loader.py   # Load commands from .md files
│   │   ├── template_processor.py  # Argument interpolation
│   │   └── mcp_handler.py      # MCP protocol handlers
│   └── lib/
│       ├── __init__.py
│       ├── yaml_parser.py      # YAML frontmatter parsing
│       └── sanitizer.py        # Argument sanitization
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_command_loader.py
│   │   ├── test_template_processor.py
│   │   └── test_sanitizer.py
│   ├── integration/
│   │   ├── test_server.py
│   │   └── test_prompts.py
│   └── fixtures/
│       └── sample_commands/  # Test command files
├── pyproject.toml          # UV project config
├── README.md               # Setup and usage instructions
└── .env.example            # Environment variables template
```

**Structure Decision**: Single project structure (Option 1) selected. This is a standalone MCP server application, not a web or mobile app. The structure follows Python best practices with clear separation: models (data structures), services (business logic), lib (utilities), and tests organized by type (unit/integration).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations. Complexity is justified:

| Complexity Introduced | Why Needed | Simpler Alternative Rejected Because |
|-----------------------|------------|-------------------------------------|
| MCP Server | Enable universal access to SpecifyPlus commands from any MCP-compatible client (Claude Desktop, IDEs, custom agents) | Claude Code CLI requires CLI environment; direct command execution lacks IDE/agent integration; MCP standard enables broad compatibility |
| YAML Frontmatter Parsing | Extract metadata (description, handoffs) from command files for P3 discoverability | Hardcoding metadata duplicates information; parsing from source files ensures single source of truth |
| Argument Sanitization | Prevent template injection attacks (FR-009 security requirement) | Accepting raw user input without sanitization exposes security vulnerability |

---

## Phase 0: Research & Technology Selection ✅

### Technology Decisions

**Decision: Python 3.11+ with MCP SDK**
- **Rationale**: User specified "Technology selection (Python)" in command args. Python MCP SDK provides official support for building MCP servers.
- **Alternatives considered**: TypeScript MCP SDK (mature, official reference implementation), but Python selected per user requirement.

**Decision: python-frontmatter for YAML + Markdown parsing**
- **Rationale**: Mature library specifically designed for parsing files with YAML frontmatter + content. Simplifies extraction of metadata and template body.
- **Alternatives considered**: Manual parsing with pyyaml (more complex, error-prone).

**Decision: Stdio transport for MCP protocol**
- **Rationale**: Standard MCP transport mechanism, works with Claude Desktop and most MCP clients. Simple process-based communication.
- **Alternatives considered**: SSE transport (more complex, requires HTTP server), JSON-RPC over sockets (non-standard).

### Research Findings

*(Will be expanded after research agent completes)*

- Python MCP SDK: `mcp` package provides `Server` class and decorators for exposing prompts
- YAML frontmatter parsing: `python-frontmatter` library handles markdown + YAML extraction
- Concurrent connections: MCP protocol handles client multiplexing; Python asyncio for async handlers
- Argument interpolation: Simple string replacement ($ARGUMENTS → user input) with escaping for special chars

---

## Phase 1: Design & Data Models

### Entity Models (data-model.md)

#### CommandDefinition

Represents a SpecifyPlus command loaded from a `.md` file.

**Attributes**:
- `name: str` - Command name (e.g., "sp.specify", "sp.plan")
- `file_path: str` - Absolute path to command file (e.g., ".claude/commands/sp.specify.md")
- `description: str` - Command description from YAML frontmatter
- `handoffs: List[Handoff]` - Recommended next steps from YAML frontmatter
- `template: PromptTemplate` - The full prompt template content

**Validation Rules**:
- `name` must match filename pattern (sp.*.md)
- `file_path` must exist and be readable
- `template` must contain markdown content

**State Transitions**: N/A (immutable after loading)

#### PromptTemplate

The markdown content of a command file with argument placeholders.

**Attributes**:
- `content: str` - Full markdown content including YAML frontmatter and body
- `has_arguments: bool` - Whether template contains $ARGUMENTS placeholder

**Operations**:
- `interpolate(arguments: str) -> str` - Replace $ARGUMENTS with provided input
- `sanitize_arguments(arguments: str) -> str` - Escape special characters for safety

**Validation Rules**:
- `content` must be non-empty string
- Argument interpolation must preserve all other template content

#### Handoff

A recommended next step in the workflow.

**Attributes**:
- `label: str` - Display name (e.g., "Build Technical Plan")
- `agent: str` - Target command name (e.g., "sp.plan")
- `prompt: str` - Suggested prompt text for the next command
- `send: bool` - Whether to auto-send (optional, default False)

**Relationships**: Many handoffs per CommandDefinition (one command can suggest multiple next steps)

---

### API Contracts (contracts/mcp-prompts.yaml)

The MCP server exposes prompts via the MCP protocol. No REST API - communication via stdio transport using MCP JSON-RPC messages.

#### MCP Protocol Operations

**Operation**: `prompts/list`
- **Purpose**: List all available prompts
- **Request**: `{"method": "prompts/list"}`
- **Response**:
  ```json
  {
    "prompts": [
      {
        "name": "sp.specify",
        "description": "Create or update the feature specification from a natural language feature description",
        "arguments": [
          {
            "name": "feature_description",
            "description": "Natural language description of the feature to specify",
            "required": false
          }
        ]
      },
      ...
    ]
  }
  ```

**Operation**: `prompts/get`
- **Purpose**: Invoke a prompt with arguments
- **Request**:
  ```json
  {
    "method": "prompts/get",
    "params": {
      "name": "sp.specify",
      "arguments": {
        "feature_description": "Add user authentication"
      }
    }
  }
  ```
- **Response**:
  ```json
  {
    "description": "Create or update the feature specification...",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "[Full prompt template with $ARGUMENTS replaced by 'Add user authentication']"
        }
      }
    ]
  }
  ```

**Error Handling**:
- `CommandNotFound`: Prompt name doesn't match any loaded command (returns error with list of available prompts)
- `InvalidYAML`: Command file has malformed YAML frontmatter (returns error with file path)
- `TemplateError`: Argument interpolation fails (returns error with details)

---

### Quickstart Testing Scenarios (quickstart.md)

#### Scenario 1: Server Startup & Connection (P1)

**Goal**: Verify server starts and accepts MCP client connections

**Steps**:
1. Start MCP server: `python -m mcp_server.server`
2. Connect from Claude Desktop or MCP test client
3. Send `prompts/list` request
4. Verify response contains all 13 commands

**Expected Outcome**: Server responds within 5 seconds with complete prompt list

**Success Criteria**: SC-001 (connection within 5 seconds, all 13 commands listed)

#### Scenario 2: Prompt Invocation with Arguments (P2)

**Goal**: Verify prompt invocation and argument interpolation

**Steps**:
1. Connect to MCP server
2. Send `prompts/get` request for "sp.specify" with argument "Add user authentication"
3. Verify response contains full template with $ARGUMENTS replaced
4. Verify YAML frontmatter preserved in response

**Expected Outcome**: Template returned within 2 seconds with correct interpolation

**Success Criteria**: SC-002 (invocation under 2 seconds), SC-004 (100% commands invocable)

#### Scenario 3: Command Metadata Discovery (P3)

**Goal**: Verify description and handoffs accessible

**Steps**:
1. Send `prompts/list` request
2. Verify "sp.specify" prompt includes description field
3. Parse handoffs from response (if exposed via MCP metadata)
4. Verify handoffs point to valid next commands (sp.plan, sp.clarify)

**Expected Outcome**: All metadata accessible without external documentation

**Success Criteria**: SC-006 (self-documenting, no external docs needed)

#### Scenario 4: Special Characters Handling (P2)

**Goal**: Verify argument sanitization prevents injection

**Steps**:
1. Invoke "sp.specify" with arguments containing special chars: `"Test $VAR and {braces} and 'quotes'"`
2. Verify template returned without errors
3. Verify special characters escaped/sanitized appropriately
4. Verify original intent preserved (text readable)

**Expected Outcome**: No errors, no template corruption

**Success Criteria**: SC-005 (special characters handled without errors)

#### Scenario 5: Concurrent Connections (P1)

**Goal**: Verify server handles multiple clients

**Steps**:
1. Start 10 MCP client connections simultaneously
2. Each client sends `prompts/list` request
3. Each client invokes different prompts concurrently
4. Verify all responses successful

**Expected Outcome**: No errors, no degraded performance

**Success Criteria**: SC-003 (10+ concurrent connections without errors)

---

## Phase 2: Technical Implementation Notes

### Command Loading Strategy

**Startup Process**:
1. Scan `.claude/commands/` directory for `*.md` files
2. For each file:
   - Parse YAML frontmatter (description, handoffs)
   - Extract markdown body (template content)
   - Create CommandDefinition object
   - Store in-memory dictionary: `commands: Dict[str, CommandDefinition]`
3. Log loaded commands count and any errors

**Error Handling**:
- Missing `.claude/commands/` directory: Create empty server with warning log
- Invalid YAML: Log error, skip command, continue loading others
- Duplicate command names: Last loaded wins, log warning

### Argument Interpolation Algorithm

```python
def interpolate_arguments(template: str, arguments: str) -> str:
    """
    Replace $ARGUMENTS placeholder with user-provided input.

    Args:
        template: Command template content
        arguments: User input to interpolate

    Returns:
        Template with $ARGUMENTS replaced
    """
    # Sanitize arguments to prevent injection
    sanitized = sanitize_arguments(arguments)

    # Simple string replacement
    return template.replace("$ARGUMENTS", sanitized)

def sanitize_arguments(arguments: str) -> str:
    """
    Escape special characters that could break template.

    Preserves user intent while preventing injection attacks.
    """
    # Escape dollar signs (except $ARGUMENTS itself)
    # Escape backticks (prevent code execution)
    # Preserve quotes, braces (they're safe in markdown)
    return arguments.replace("$", "\\$").replace("`", "\\`")
```

### MCP Server Implementation Pattern

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Create server instance
server = Server("specifyplus-mcp-server")

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List all available SpecifyPlus commands as prompts."""
    return [
        Prompt(
            name=cmd.name,
            description=cmd.description,
            arguments=[
                PromptArgument(
                    name="feature_description",
                    description="Input for the command",
                    required=False
                )
            ]
        )
        for cmd in commands.values()
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str]) -> GetPromptResult:
    """Invoke a prompt with arguments."""
    cmd = commands.get(name)
    if not cmd:
        raise ValueError(f"Command not found: {name}")

    # Get arguments (default to empty string)
    user_input = arguments.get("feature_description", "")

    # Interpolate template
    content = cmd.template.interpolate(user_input)

    return GetPromptResult(
        description=cmd.description,
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]
    )

# Run server with stdio transport
async def main():
    async with stdio_server() as streams:
        await server.run(
            streams[0], streams[1],
            server.create_initialization_options()
        )
```

### Logging Strategy

- Log to stderr (stdout reserved for MCP protocol)
- Log levels:
  - INFO: Server startup, command loading summary
  - DEBUG: Individual command loads, prompt invocations
  - WARNING: Invalid YAML, missing files, edge cases
  - ERROR: Critical failures (server startup fails)
- Log format: `[TIMESTAMP] [LEVEL] [MODULE] Message`
- Include context: command name, argument preview (first 100 chars), client info (if available)

---

## Next Steps

1. ✅ Phase 0 complete - Technology and architecture decisions documented
2. ⏳ Phase 1 in progress - Data models and contracts defined, quickstart scenarios created
3. ⏭️ Phase 2 pending - Run `/sp.tasks` to break plan into dependency-ordered implementation tasks
4. ⏭️ Phase 3 pending - Run `/sp.implement` to execute tasks following Red-Green-Refactor cycle

---

## Notes

- This MCP server is separate from the Todo app phases (Phase I-V). It's a supporting tool that exposes SpecifyPlus commands universally.
- The server is stateless - each prompt invocation is independent. No session or conversation state.
- Command files are loaded once at startup. To reload, restart the server (or add a reload mechanism in future iterations).
- Testing will verify all 13 commands load correctly and that argument interpolation preserves template integrity.
- The server follows the single project structure from constitution (Option 1), not the web/mobile patterns.
