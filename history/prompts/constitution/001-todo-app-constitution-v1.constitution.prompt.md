---
id: 001
title: todo-app-constitution-v1
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: n/a
command: /sp.constitution
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Phase I: Todo In-Memory Python Console App
Basic Level Functionality
Objective: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.
Development Approach: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will review the process, prompts, and iterations to judge each phase and project.
Requirements
Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
Use spec-driven development with Claude Code and Spec-Kit Plus
Follow clean code principles and proper Python project structure
Technology Stack
UV
Python 3.13+
Claude Code
Spec-Kit Plus
Deliverables
GitHub repository with:
Constitution file
specs history folder containing all specification files
/src folder with Python source code
README.md with setup instructions
CLAUDE.md with Claude Code instructions

Working console application demonstrating:
Adding tasks with title and description
Listing all tasks with status indicators
Updating task details
Deleting tasks by ID
Marking tasks as complete/incomplete

## Response snapshot

Created project constitution version 1.0.0 for Todo In-Memory Python Console App.

**Core Principles Established**:
1. Spec-Driven Development (SDD) - Spec → Plan → Tasks → Implement workflow
2. Agentic Implementation - All code via Claude Code using Spec-Kit Plus, no manual coding
3. Clean Code & Python Standards - Type hints, PEP 8, docstrings mandatory
4. Simple Architecture - In-memory storage, minimal complexity, CLI pattern
5. Incremental Delivery - Priority-based (P1 → P2 → P3) with independent testing

**Technology Standards Defined**:
- Python 3.13+ with type hints
- UV as exclusive package manager
- Project structure: src/{models,services,cli}, tests/{unit,integration,contract}
- Tools: Ruff (linting), pytest (testing), pyright/mypy (type checking)

**Governance Framework**:
- Semantic versioning for constitution amendments
- Compliance review for all development work
- Complexity justification for deviations
- PHR routing: constitution/, <feature>/, general/

Template validation: All existing templates (plan-template.md, spec-template.md, tasks-template.md, phr-template.prompt.md) remain compatible with the new constitution.

## Outcome

- Impact: Established foundational governance document for Todo App project with 5 core principles and complete development workflow
- Tests: N/A (constitution only)
- Files: .specify/memory/constitution.md created
- Next prompts: /sp.specify to create feature specification for todo app
- Reflection: Constitution successfully captures Agentic Dev Stack workflow and Spec-Driven Development methodology with appropriate Python-specific standards

## Evaluation notes (flywheel)

- Failure modes observed: N/A (initial constitution creation)
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor how principles apply during actual spec/planning phases
