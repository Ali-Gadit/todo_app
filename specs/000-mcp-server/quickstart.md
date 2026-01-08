# Quickstart: SpecifyPlus MCP Server Testing

**Feature**: 001-mcp-server
**Date**: 2026-01-04
**Purpose**: End-to-end testing scenarios for validating MCP server functionality

## Prerequisites

- Python 3.11+ installed
- UV package manager installed
- `.claude/commands/*.md` files present (13 SpecifyPlus commands)
- MCP-compatible client (Claude Desktop, MCP test client, or custom client)

## Setup

```bash
# Navigate to mcp-server directory
cd mcp-server

# Install dependencies with UV
uv sync

# Verify installation
uv run python -m src.server --help
```

---

## Scenario 1: Server Startup & Connection (Priority: P1)

**Goal**: Verify server starts successfully and accepts MCP client connections.

**User Story**: US1 - Connect MCP Server to Any IDE

**Success Criteria**: SC-001 (connection within 5 seconds, all 13 commands listed)

### Test Steps

1. **Start the MCP server**:
   ```bash
   uv run python -m src.server
   ```

2. **Expected Output** (stderr):
   ```
   [2026-01-04 12:00:00] [INFO] [server] Starting SpecifyPlus MCP Server
   [2026-01-04 12:00:00] [INFO] [command_loader] Loading commands from .claude/commands/
   [2026-01-04 12:00:01] [INFO] [command_loader] Loaded 13 commands: sp.specify, sp.plan, sp.tasks, ...
   [2026-01-04 12:00:01] [INFO] [server] Server ready, listening on stdio
   ```

3. **Connect from Claude Desktop**:
   - Open Claude Desktop
   - Go to Settings → Developer → MCP Servers
   - Add server configuration:
     ```json
     {
       "specifyplus": {
         "command": "uv",
         "args": ["run", "python", "-m", "src.server"],
         "cwd": "/path/to/mcp-server"
       }
     }
     ```
   - Restart Claude Desktop
   - Verify "specifyplus" server appears in connected servers list

4. **List available prompts** (from Claude Desktop or MCP test client):
   - Send MCP request: `{"method": "prompts/list"}`
   - Verify response contains 13 prompts

5. **Expected Response**:
   ```json
   {
     "prompts": [
       {
         "name": "sp.specify",
         "description": "Create or update the feature specification from a natural language feature description",
         "arguments": [...]
       },
       {
         "name": "sp.plan",
         "description": "Execute the implementation planning workflow using the plan template to generate design artifacts",
         "arguments": [...]
       },
       ... (11 more commands)
     ]
   }
   ```

### Pass Criteria

- ✅ Server starts within 5 seconds
- ✅ No errors in stderr logs
- ✅ Client connects successfully
- ✅ `prompts/list` returns exactly 13 commands
- ✅ All command names start with "sp."

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Server fails to start | Python version < 3.11 | Upgrade Python: `uv python install 3.11` |
| "Command not found" | UV not installed | Install UV: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| No commands loaded | `.claude/commands/` missing | Verify directory exists with `ls .claude/commands/*.md` |
| Claude Desktop can't connect | Wrong cwd in config | Use absolute path in `cwd` field |

---

## Scenario 2: Prompt Invocation with Arguments (Priority: P2)

**Goal**: Verify prompt invocation with argument interpolation works correctly.

**User Story**: US2 - Execute SpecifyPlus Commands via Prompts

**Success Criteria**: SC-002 (invocation under 2 seconds), SC-004 (100% commands invocable)

### Test Steps

1. **Invoke sp.specify prompt**:
   - From Claude Desktop: Type `/specifyplus sp.specify`
   - Provide argument: "Add user authentication"
   - Alternatively, send MCP request:
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

2. **Verify response**:
   - Check that response contains full sp.specify template
   - Verify `$ARGUMENTS` replaced with "Add user authentication"
   - Verify YAML frontmatter preserved (description field present)

3. **Expected Response** (partial):
   ```json
   {
     "description": "Create or update the feature specification from a natural language feature description",
     "messages": [
       {
         "role": "user",
         "content": {
           "type": "text",
           "text": "## User Input\n\n```text\nAdd user authentication\n```\n\nYou **MUST** consider the user input before proceeding..."
         }
       }
     ]
   }
   ```

4. **Test with empty arguments**:
   - Invoke sp.plan with no arguments: `{}`
   - Verify template returns with `$ARGUMENTS` unchanged or as empty string

5. **Test all 13 commands** (automated):
   ```python
   import asyncio
   from mcp.client import Client

   async def test_all_commands():
       client = Client()
       prompts = await client.list_prompts()

       for prompt in prompts:
           result = await client.get_prompt(
               name=prompt.name,
               arguments={"feature_description": "Test feature"}
           )
           assert result.description == prompt.description
           assert "$ARGUMENTS" not in result.messages[0].content.text or "Test feature" in result.messages[0].content.text
           print(f"✅ {prompt.name} invoked successfully")

   asyncio.run(test_all_commands())
   ```

### Pass Criteria

- ✅ Prompt invocation completes within 2 seconds
- ✅ `$ARGUMENTS` replaced correctly
- ✅ Template content preserved (no corruption)
- ✅ YAML frontmatter preserved
- ✅ Empty arguments handled gracefully
- ✅ All 13 commands invocable without errors

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| "$ARGUMENTS not replaced" | Template missing placeholder | Check command file has `$ARGUMENTS` in body |
| "Command not found" | Typo in prompt name | Verify exact name from `prompts/list` |
| Slow response (>2s) | Large template file | Check file size, ensure <10KB |
| Template corrupted | Interpolation bug | Check logs for errors, verify sanitization logic |

---

## Scenario 3: Command Metadata Discovery (Priority: P3)

**Goal**: Verify command descriptions and handoffs are accessible for discoverability.

**User Story**: US3 - Discover Command Metadata and Handoffs

**Success Criteria**: SC-006 (self-documenting, no external docs needed)

### Test Steps

1. **List prompts with metadata**:
   ```json
   {"method": "prompts/list"}
   ```

2. **Verify each prompt includes**:
   - `name`: Command name (e.g., "sp.specify")
   - `description`: Human-readable description from YAML frontmatter
   - `arguments`: List of accepted arguments

3. **Check handoffs** (if exposed via MCP):
   - Verify sp.specify has handoffs to sp.plan and sp.clarify
   - Verify sp.plan has handoff to sp.tasks
   - Verify sp.tasks has handoffs to sp.analyze and sp.implement

4. **Test discoverability**:
   - User with no prior knowledge should understand:
     - What each command does (from description)
     - What arguments it accepts (from arguments list)
     - What to do next (from handoffs, if supported by MCP)

### Pass Criteria

- ✅ All 13 commands have descriptions
- ✅ Descriptions are clear and concise (< 200 chars)
- ✅ Handoffs available (either via MCP or in template)
- ✅ User can navigate workflow without external documentation

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Missing description | YAML frontmatter missing field | Add `description:` to command file |
| Empty description | Description field empty in YAML | Add meaningful description text |
| Handoffs not visible | MCP doesn't support handoff metadata | Document handoffs in template body |

---

## Scenario 4: Special Characters Handling (Priority: P2)

**Goal**: Verify argument sanitization prevents template injection while preserving user intent.

**User Story**: US2 - Execute SpecifyPlus Commands via Prompts

**Success Criteria**: SC-005 (special characters handled without errors)

### Test Steps

1. **Test dollar signs**:
   ```json
   {
     "method": "prompts/get",
     "params": {
       "name": "sp.specify",
       "arguments": {"feature_description": "Add $VAR variable support"}
     }
   }
   ```
   - Verify `$VAR` escaped as `\$VAR` in response
   - Verify template doesn't execute variable expansion

2. **Test backticks**:
   ```json
   {
     "arguments": {"feature_description": "Add `inline code` support"}
   }
   ```
   - Verify backticks escaped as `` \`inline code\` ``
   - Verify no code execution attempted

3. **Test braces and quotes**:
   ```json
   {
     "arguments": {"feature_description": "Add {braces} and 'quotes' and \"double quotes\""}
   }
   ```
   - Verify braces and quotes preserved (safe in markdown)
   - Verify text readable and intent preserved

4. **Test combined special characters**:
   ```json
   {
     "arguments": {"feature_description": "Test $VAR and `code` and {obj} and 'str'"}
   }
   ```
   - Verify `$` and `` ` `` escaped, braces and quotes preserved
   - Verify output: `"Test \$VAR and \`code\` and {obj} and 'str'"`

### Pass Criteria

- ✅ Dollar signs escaped to prevent variable expansion
- ✅ Backticks escaped to prevent code execution
- ✅ Quotes and braces preserved (safe in markdown)
- ✅ User intent preserved (text remains readable)
- ✅ No errors or template corruption
- ✅ Invocation completes successfully for all test cases

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Variable expansion occurs | Sanitization not applied | Check `sanitize_arguments()` called before replacement |
| Text unreadable | Over-escaping | Review escaping rules, preserve safe characters |
| Template corrupted | Escaping breaks markdown | Test with markdown parser, adjust escaping |

---

## Scenario 5: Concurrent Connections (Priority: P1)

**Goal**: Verify server handles multiple simultaneous client connections without errors.

**User Story**: US1 - Connect MCP Server to Any IDE

**Success Criteria**: SC-003 (10+ concurrent connections without errors)

### Test Steps

1. **Launch 10 concurrent clients** (automated test):
   ```python
   import asyncio
   from mcp.client import Client

   async def client_session(client_id: int):
       client = Client()
       await client.connect()

       # Each client lists prompts
       prompts = await client.list_prompts()
       assert len(prompts) == 13

       # Each client invokes different prompt
       prompt_name = prompts[client_id % 13].name
       result = await client.get_prompt(
           name=prompt_name,
           arguments={"feature_description": f"Test from client {client_id}"}
       )
       assert result is not None

       print(f"✅ Client {client_id} completed successfully")

   async def main():
       tasks = [client_session(i) for i in range(10)]
       await asyncio.gather(*tasks)
       print("✅ All 10 clients completed successfully")

   asyncio.run(main())
   ```

2. **Monitor server logs** (stderr):
   - Check for errors or warnings
   - Verify each connection logged
   - Verify no race conditions or deadlocks

3. **Verify responses**:
   - All 10 clients receive valid responses
   - No timeouts or connection errors
   - Response times remain consistent (<2s per invocation)

### Pass Criteria

- ✅ 10+ clients connect simultaneously
- ✅ All clients receive valid responses
- ✅ No errors or warnings in server logs
- ✅ No performance degradation
- ✅ Response times consistent across all clients

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Connection timeouts | Server overloaded | Check CPU/memory usage, verify asyncio not blocking |
| Race conditions | Shared mutable state | Verify commands dict is read-only after load |
| Deadlocks | Blocking I/O in async context | Replace blocking calls with async equivalents |
| Errors in logs | Concurrent access bugs | Add locks if needed (shouldn't be for read-only) |

---

## Complete Test Suite

### Automated Test Runner

```bash
# Run all quickstart scenarios
cd mcp-server
uv run pytest tests/integration/test_quickstart.py -v

# Expected output:
# test_scenario_1_startup ✅ PASSED
# test_scenario_2_invocation ✅ PASSED
# test_scenario_3_metadata ✅ PASSED
# test_scenario_4_special_chars ✅ PASSED
# test_scenario_5_concurrent ✅ PASSED
```

### Manual Testing Checklist

- [ ] Server starts within 5 seconds
- [ ] All 13 commands load successfully
- [ ] Claude Desktop connection works
- [ ] `prompts/list` returns all commands
- [ ] Prompt invocation with arguments works
- [ ] `$ARGUMENTS` replaced correctly
- [ ] Empty arguments handled gracefully
- [ ] Command descriptions visible
- [ ] Handoffs accessible (if supported)
- [ ] Special characters escaped correctly
- [ ] User intent preserved after escaping
- [ ] 10 concurrent clients handled successfully
- [ ] No errors or warnings in logs

---

## Success Summary

| Scenario | Priority | Success Criteria | Status |
|----------|----------|------------------|--------|
| Server Startup & Connection | P1 | SC-001 | ⏳ Pending |
| Prompt Invocation | P2 | SC-002, SC-004 | ⏳ Pending |
| Metadata Discovery | P3 | SC-006 | ⏳ Pending |
| Special Characters | P2 | SC-005 | ⏳ Pending |
| Concurrent Connections | P1 | SC-003 | ⏳ Pending |

**Overall Status**: ⏳ Ready for implementation and testing

---

## Next Steps

1. ✅ Quickstart scenarios defined
2. ⏭️ Run `/sp.tasks` to break plan into implementation tasks
3. ⏭️ Run `/sp.implement` to execute tasks following Red-Green-Refactor
4. ⏭️ Execute quickstart scenarios to validate implementation
5. ⏭️ Update status table above as scenarios pass testing
