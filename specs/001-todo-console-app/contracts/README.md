# Contracts: Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Purpose**: Define CLI command interfaces and service contracts

## Overview

This directory contains interface contracts for the Todo Console App. Since this is a command-line application with in-memory storage, contracts define:
- CLI command syntax and parameters
- Service method signatures
- Expected return types
- Exception contracts

## Contract Files

| File | Purpose |
|-------|---------|
| cli-commands.md | CLI command syntax, parameters, output format |
| service-interface.md | Task service method signatures and contracts |

## Notes

- No REST/GraphQL contracts (this is CLI application)
- No database schema (in-memory storage)
- Contracts serve as implementation guide and validation criteria
