<!--
SYNC IMPACT REPORT
==================
Version change: None (NEW) → 1.0.0

Modified principles: N/A (new constitution)

Added sections:
- Core Principles: 5 principles (Spec-Driven, Agentic Implementation, Test-First, Clean Code, Simple Architecture)
- Technology Standards: Python 3.13+, UV, in-memory storage
- Development Workflow: Spec → Plan → Tasks → Implement
- Governance: Versioning, compliance review

Removed sections: N/A

Templates requiring updates:
✅ plan-template.md - No changes needed (generic structure works)
✅ spec-template.md - No changes needed (supports user stories and requirements)
✅ tasks-template.md - No changes needed (supports test-first approach)
✅ phr-template.prompt.md - No changes needed (structure works)

Follow-up TODOs: None
-->

# Todo App In-Memory Console Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

Every feature MUST be developed using the Spec-Driven Development methodology. The workflow is strictly enforced: write specification → generate plan → break into tasks → implement via Claude Code. No feature development begins without a complete specification and plan. Specifications MUST include user stories with priorities (P1, P2, P3...), functional requirements, acceptance scenarios, and success criteria. This ensures all requirements are understood before any code is written.

### II. Agentic Implementation

All code implementation MUST be performed by Claude Code using Spec-Kit Plus tools. Manual coding is strictly prohibited. The implementation follows the Red-Green-Refactor cycle: write failing tests first (Red), implement to make tests pass (Green), then improve code while maintaining functionality (Refactor). This ensures code quality and follows test-driven development principles. All prompts and iterations are recorded for process review and evaluation.

### III. Clean Code & Python Standards

Code MUST follow Python best practices and clean code principles. Type hints are MANDATORY for all function signatures and complex variables. Code MUST follow PEP 8 style guide enforced by linting tools. Functions should be small and have a single responsibility. Use descriptive names that reveal intent. Avoid deep nesting and complex conditionals. Docstrings are REQUIRED for all public functions, classes, and modules. All imports must be explicitly declared at the top of files with proper grouping.

### IV. Simple Architecture

The application uses in-memory storage with minimal complexity. No databases, frameworks, or external dependencies are permitted in Phase I. All task data is stored in Python data structures (lists, dicts) during runtime. The architecture follows a simple CLI pattern: command input → processing → output display. Error handling should be clear and user-friendly. The focus is on correctness and maintainability over premature optimization.

### V. Incremental Delivery

Features are delivered in priority order (P1 → P2 → P3...). Each user story MUST be independently testable and deliverable. Higher priority stories (P1) are implemented first to provide early value. After each priority level, implementation stops for validation and review. This ensures working functionality at each checkpoint and allows for early feedback. No lower priority features are started until higher priority features are complete and tested.

## Technology Standards

### Python Version

Python 3.13+ is the required runtime version. Type hints are mandatory and should use the standard `typing` module for type annotations. Where appropriate, use modern Python features like dataclasses, pattern matching, and structural pattern matching.

### Package Management

UV is the exclusive package manager for this project. All dependencies must be managed through UV's lockfile mechanism to ensure reproducible environments. Use `uv` commands for installing, running, and managing the project. No manual `pip` installations are permitted.

### Project Structure

The project follows a clean Python structure:
- `src/` - All source code organized by module
- `src/models/` - Data models and entities
- `src/services/` - Business logic
- `src/cli/` - Command-line interface components
- `tests/` - All test code organized by type (unit, integration, contract)

### Code Quality Tools

- **Linting**: Ruff for fast Python linting and formatting
- **Testing**: pytest for test execution
- **Type Checking**: pyright or mypy for static type checking
- All tools MUST be configured and run as part of development workflow

## Development Workflow

### Spec-Driven Development Lifecycle

1. **Specification**: Create feature spec with user stories, requirements, and acceptance criteria
2. **Planning**: Generate implementation plan with architecture, data models, and contracts
3. **Task Breakdown**: Create dependency-ordered tasks grouped by user story
4. **Implementation**: Execute tasks via Claude Code following Red-Green-Refactor
5. **Validation**: Test each user story independently before proceeding

### Prompt History Records (PHR)

Every user interaction MUST be recorded in a Prompt History Record (PHR). PHRs capture:
- Full user input (verbatim, no truncation)
- Assistant response summary
- Files created/modified
- Tests run/added
- Outcome and evaluation notes

PHRs are routed to:
- `history/prompts/constitution/` - Constitution-related prompts
- `history/prompts/<feature-name>/` - Feature-specific prompts
- `history/prompts/general/` - General development prompts

### Review & Evaluation

All development work is subject to process review. Prompts, iterations, and decisions are captured in PHRs for evaluation. This transparency allows for continuous improvement of the development workflow and agent effectiveness.

## Code Standards

### Testing Discipline

- Tests MUST be written before implementation (Red-Green-Refactor)
- Unit tests MUST be fast, isolated, and deterministic
- Integration tests MUST validate cross-component interactions
- Test names MUST clearly describe the scenario being tested
- Tests MUST be run before committing changes

### Documentation Standards

- All public functions MUST have docstrings
- Docstrings MUST describe purpose, parameters, return values, and exceptions
- README.md MUST include setup instructions and usage examples
- CLAUDE.md MUST include Claude Code-specific instructions for the project

### Error Handling

- Errors MUST be caught and handled gracefully at appropriate levels
- User-facing error messages MUST be clear and actionable
- Internal errors MUST be logged with sufficient context for debugging
- Use custom exception types for domain-specific errors

## Governance

### Constitution Versioning

The constitution follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Backward incompatible changes to principles or fundamental workflow changes
- **MINOR**: New principle or section added, or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Amendment Process

Amendments to the constitution MUST:
1. Update the version number according to semantic versioning rules
2. Document changes in the Sync Impact Report at the top of the file
3. Update dependent templates and command files to maintain consistency
4. Be reviewed for compliance with existing principles before approval

### Compliance Review

All development work MUST comply with constitution principles:
- Spec-Driven Development workflow MUST be followed
- Agentic Implementation via Claude Code MUST be used
- Clean Code standards MUST be maintained
- Tests MUST pass before completion
- PHRs MUST be created for all interactions

### Complexity Justification

Any deviation from simple architecture MUST be documented in the Complexity Tracking section of implementation plans. The justification MUST explain why the simpler alternative is insufficient and demonstrate that the complexity is necessary for the feature.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
