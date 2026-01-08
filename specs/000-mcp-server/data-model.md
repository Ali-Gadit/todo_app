# Data Model: SpecifyPlus MCP Server

**Feature**: 001-mcp-server
**Date**: 2026-01-04
**Status**: Design Complete

## Overview

The SpecifyPlus MCP Server uses three core entities to represent command definitions, prompt templates, and workflow handoffs. All entities are immutable after loading from disk at server startup.

---

## Entity: CommandDefinition

Represents a SpecifyPlus command loaded from a `.md` file in `.claude/commands/`.

### Attributes

| Attribute | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `name` | str | Yes | Command name (e.g., "sp.specify") | Must match pattern `sp\\..*` |
| `file_path` | str | Yes | Absolute path to source file | Must exist and be readable |
| `description` | str | Yes | Human-readable command description | Max 500 chars |
| `handoffs` | List[Handoff] | No | Recommended next steps | Empty list if not specified |
| `template` | PromptTemplate | Yes | Full prompt template | Must contain valid markdown |

### Example

```python
CommandDefinition(
    name="sp.specify",
    file_path="/path/to/.claude/commands/sp.specify.md",
    description="Create or update the feature specification from a natural language feature description",
    handoffs=[
        Handoff(label="Build Technical Plan", agent="sp.plan", prompt="Create a plan for the spec", send=False),
        Handoff(label="Clarify Spec Requirements", agent="sp.clarify", prompt="Clarify specification requirements", send=True)
    ],
    template=PromptTemplate(content="...", has_arguments=True)
)
```

### Lifecycle

1. **Loading**: Created at server startup by parsing command files
2. **Storage**: Stored in-memory dictionary: `Dict[str, CommandDefinition]`
3. **Access**: Read-only access during prompt invocations
4. **Immutability**: Never modified after loading (restart server to reload)

### Relationships

- **One-to-Many with Handoff**: A command can have 0-N recommended next steps
- **One-to-One with PromptTemplate**: Each command has exactly one template

---

## Entity: PromptTemplate

Represents the markdown content of a command file with argument placeholders.

### Attributes

| Attribute | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| `content` | str | Yes | Full markdown including YAML frontmatter and body | Non-empty string |
| `has_arguments` | bool | Yes | Whether template contains $ARGUMENTS placeholder | Derived from content scan |

### Operations

#### `interpolate(arguments: str) -> str`

Replaces $ARGUMENTS placeholder with user-provided input.

**Parameters**:
- `arguments: str` - User input to interpolate (may be empty)

**Returns**:
- `str` - Template with $ARGUMENTS replaced by sanitized arguments

**Algorithm**:
```python
def interpolate(self, arguments: str) -> str:
    """Replace $ARGUMENTS with sanitized user input."""
    sanitized = self.sanitize_arguments(arguments)
    return self.content.replace("$ARGUMENTS", sanitized)
```

**Edge Cases**:
- Empty arguments: Replace $ARGUMENTS with empty string
- Multiple $ARGUMENTS: Replace all occurrences (if template has duplicates)
- No $ARGUMENTS: Return content unchanged

#### `sanitize_arguments(arguments: str) -> str`

Escapes special characters to prevent template injection.

**Parameters**:
- `arguments: str` - Raw user input

**Returns**:
- `str` - Sanitized input with escaped special chars

**Security Considerations**:
- Escapes `$` → `\$` (prevent variable expansion)
- Escapes `` ` `` → `` \` `` (prevent code execution)
- Preserves quotes, braces, brackets (safe in markdown)

### Example

```python
template = PromptTemplate(
    content="""---
description: Create a spec
---

## User Input

```text
$ARGUMENTS
```

Do this: generate a spec for the feature.""",
    has_arguments=True
)

# Interpolate with user input
result = template.interpolate("Add user authentication")

# Result:
# """---
# description: Create a spec
# ---
#
# ## User Input
#
# ```text
# Add user authentication
# ```
#
# Do this: generate a spec for the feature."""
```

### Validation Rules

- `content` must be non-empty string
- Argument interpolation must preserve all other template content (whitespace, formatting)
- Special characters in arguments must be escaped before interpolation

---

## Entity: Handoff

Represents a recommended next step in the Spec-Driven Development workflow.

### Attributes

| Attribute | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `label` | str | Yes | Display name for the handoff | N/A |
| `agent` | str | Yes | Target command name | Must match existing command |
| `prompt` | str | Yes | Suggested prompt text for next command | N/A |
| `send` | bool | No | Whether to auto-send the handoff | False |

### Example

```python
handoff = Handoff(
    label="Build Technical Plan",
    agent="sp.plan",
    prompt="Create a plan for the spec. I am building with...",
    send=False
)
```

### Parsing from YAML Frontmatter

Handoffs are defined in command files as:

```yaml
---
description: Create spec
handoffs:
  - label: Build Technical Plan
    agent: sp.plan
    prompt: Create a plan for the spec
    send: false
  - label: Clarify Spec Requirements
    agent: sp.clarify
    prompt: Clarify specification requirements
    send: true
---
```

### Relationships

- **Many-to-One with CommandDefinition**: Multiple handoffs belong to one command
- **Reference to CommandDefinition**: `agent` field references another command by name

### Validation Rules

- `label` must be non-empty string (max 100 chars)
- `agent` must match an existing command name (validated at runtime, not load time)
- `prompt` must be non-empty string (max 500 chars)
- `send` defaults to False if not specified

---

## Data Flow

### Server Startup

```
1. Scan .claude/commands/*.md files
   ↓
2. For each file:
   - Parse YAML frontmatter → extract description, handoffs
   - Parse markdown body → extract template content
   ↓
3. Create CommandDefinition objects
   ↓
4. Store in commands dictionary: Dict[str, CommandDefinition]
   ↓
5. Log loaded commands (count, names)
```

### Prompt Invocation

```
1. MCP client sends prompts/get request
   ↓
2. Extract prompt name and arguments from request
   ↓
3. Look up CommandDefinition in commands dict
   ↓
4. Call template.interpolate(arguments)
   ↓
5. Return GetPromptResult with interpolated content
```

---

## Storage Strategy

**In-Memory Storage**: All entities stored in memory after loading at startup.

**Data Structure**:
```python
commands: Dict[str, CommandDefinition] = {
    "sp.specify": CommandDefinition(...),
    "sp.plan": CommandDefinition(...),
    "sp.tasks": CommandDefinition(...),
    # ... 10 more commands
}
```

**Justification**:
- 13 commands × ~5KB per template = ~65KB total (negligible memory)
- Fast lookup: O(1) dictionary access
- No persistence needed: commands are read-only after load
- Reload strategy: Restart server to pick up file changes

**Alternative Considered**: Database storage (rejected due to unnecessary complexity for read-only data)

---

## Validation Summary

### At Load Time

- **File Exists**: Verify `.md` file exists before loading
- **Valid YAML**: Parse frontmatter without errors
- **Required Fields**: Ensure description present in YAML
- **Valid Markdown**: Ensure body is non-empty

### At Runtime

- **Command Exists**: Verify prompt name in commands dict before invocation
- **Arguments Valid**: Sanitize arguments before interpolation
- **Template Integrity**: Verify template content preserved after interpolation

---

## Error Handling

### Loading Errors

| Error | Handling | User Impact |
|-------|----------|-------------|
| File not found | Skip command, log warning | Command unavailable in prompt list |
| Invalid YAML | Skip command, log error | Command unavailable in prompt list |
| Missing description | Use empty string, log warning | Command shows with no description |
| Malformed handoffs | Use empty list, log warning | Command has no suggested next steps |

### Invocation Errors

| Error | Handling | User Impact |
|-------|----------|-------------|
| Command not found | Return error with available commands list | Client receives helpful error message |
| Interpolation fails | Return error with details | Client receives error (rare - simple string replacement) |
| Sanitization fails | Use raw arguments, log warning | Possible security risk (should not happen) |

---

## Testing Scenarios

### Unit Tests

1. **CommandDefinition creation**: Verify all fields populated correctly
2. **PromptTemplate interpolation**: Verify $ARGUMENTS replaced correctly
3. **Argument sanitization**: Verify special chars escaped ($ → \$, ` → \`)
4. **Handoff parsing**: Verify YAML frontmatter parsed to Handoff objects

### Integration Tests

1. **Load all 13 commands**: Verify all `.claude/commands/*.md` files load successfully
2. **Invoke each command**: Verify all 13 commands invocable with sample arguments
3. **Edge cases**: Verify empty arguments, special characters, missing handoffs handled

---

## Conclusion

Data model designed with three core entities:
1. **CommandDefinition**: Represents loaded command with metadata
2. **PromptTemplate**: Handles argument interpolation and sanitization
3. **Handoff**: Represents workflow progression suggestions

All entities immutable after loading. In-memory storage sufficient for 13 commands. Validation at load time and runtime ensures robustness.
