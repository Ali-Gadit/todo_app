# Research: Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Purpose**: Resolve technical decisions for implementation planning

## Overview

Research conducted to determine optimal technical approach for in-memory Python console todo application. All decisions align with constitution requirements (Simple Architecture, Clean Code, Spec-Driven Development).

## Technical Decisions

### Language and Runtime

**Decision**: Python 3.13+

**Rationale**:
- Explicit requirement from constitution (Technology Standards)
- Type hints are mandatory - Python 3.13+ has improved type checking features
- Dataclass and pattern matching support for clean, modern code
- Wide platform compatibility (Linux, macOS, Windows)

**Alternatives Considered**:
- Python 3.11: Older, less robust type features
- Python 3.12: Intermediate, but 3.13+ specified in constitution

---

### Storage Strategy

**Decision**: In-memory storage using Python data structures (list, dict)

**Rationale**:
- Constitution Principle IV mandates: "No databases, frameworks, or external dependencies are permitted in Phase I"
- FR-012 specifies: "System MUST maintain all task data in memory during application runtime"
- Simplest possible solution aligning with success criteria
- Data persistence not required in Phase I scope
- Eliminates complexity of database setup, migrations, schema management

**Alternatives Considered**:
- SQLite: Too complex for Phase I, violates "no databases" constraint
- JSON file persistence: Not required, adds I/O complexity
- External database: Explicitly prohibited by constitution

---

### CLI Framework

**Decision**: Custom CLI using Python standard library (argparse + argparse)

**Rationale**:
- No external frameworks permitted (constitution Principle IV)
- argparse is built-in, mature, and sufficient for simple command parsing
- Maintains "Simple Architecture" principle
- Zero external dependencies aligns with independence goals

**Alternatives Considered**:
- Click: External framework, prohibited
- Typer: External framework, prohibited
- Python Fire: External framework, prohibited

---

### Testing Framework

**Decision**: pytest

**Rationale**:
- Constitution specifies pytest as testing tool
- Industry standard for Python testing
- Simple setup, clear test structure
- Supports fixtures, parameterization for comprehensive testing
- Fast execution suitable for unit tests

**Alternatives Considered**:
- unittest (built-in): More verbose, less feature-rich
- nose2: Deprecated, superseded by pytest

---

### Code Quality Tools

**Decision**: Ruff for linting/formatting, pyright for type checking

**Rationale**:
- Constitution specifies Ruff, pytest, pyright/mypy
- Ruff: Extremely fast, combines linting and formatting, PEP 8 compliance
- pyright: Microsoft's static type checker, fast, accurate, Python 3.13+ support

**Alternatives Considered**:
- Black + Flake8: Two separate tools, Ruff combines both faster
- mypy: Slower than pyright, less accurate in some cases

---

### Task ID Management

**Decision**: Sequential numeric IDs starting from 1

**Rationale**:
- FR-002: "System MUST generate a unique sequential numeric identifier for each new task"
- FR-008: "System MUST maintain stable task IDs (deleting a task does not renumber remaining tasks)"
- Simple integer counter (next_id++) is sufficient
- Stable IDs prevent confusion when tasks are deleted

**Alternatives Considered**:
- UUIDs: Overkill for in-memory storage, harder for users to reference
- Timestamps: Not user-friendly for CLI input

---

## Architecture Patterns

### Error Handling

**Decision**: Custom exception types in `src/lib/exceptions.py`

**Rationale**:
- FR-010: "System MUST display clear, user-friendly error messages for invalid operations"
- Custom exceptions provide domain-specific error context
- Enables try/except patterns with specific error handling
- Supports clear user feedback per constitution error handling standards

**Pattern**:
```python
class TaskNotFound(Exception):
    """Raised when task ID does not exist"""

class InvalidTitle(Exception):
    """Raised when task title is empty or invalid"""
```

---

### Data Model Pattern

**Decision**: Python dataclass for Task entity

**Rationale**:
- Python 3.13+ dataclass provides concise, type-safe data structure
- Built-in __eq__, __repr__ methods for testing
- Type hints mandatory per constitution
- Minimal boilerplate aligns with Clean Code principles

**Alternatives Considered**:
- Pydantic: External dependency, prohibited
- Plain class: More boilerplate, manual __init__

---

## Summary

All technical decisions resolved. No NEEDS CLARIFICATION markers remain. Technical Context is complete with clear rationale for each decision aligning with constitution principles.

**Decisions Documented**:
1. Python 3.13+ runtime with type hints
2. In-memory storage (list, dict)
3. Custom CLI using argparse (standard library)
4. pytest for testing
5. Ruff + pyright for code quality
6. Sequential numeric task IDs (stable on delete)
7. Custom exceptions for domain-specific errors
8. dataclass for Task entity

**Next Phase**: Phase 1 - Design data-model.md, contracts/, and quickstart.md
