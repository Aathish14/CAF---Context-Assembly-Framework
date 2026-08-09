# Context Assembly Framework (CAF)
# AI Context Document

**Purpose**

This document is the primary bootstrap context for AI coding agents working on CAF.

Read this document BEFORE reading the repository.

This document summarizes:

- project purpose
- architecture
- engineering rules
- implementation status
- current milestone
- repository structure

The objective is to minimize repository exploration while preserving architectural consistency.

---

# Project Overview

Project Name

Context Assembly Framework (CAF)

Project Type

Internal Engineering Framework

Status

Active Development

Current Phase

Phase 5

Current Milestone

Validation Engine & Context Builder

---

# What CAF Is

CAF is an internal framework for:

1. Collecting structured user inputs.
2. Building normalized Context Objects.
3. Assembling deterministic instructions.
4. Managing instruction versions.
5. Supporting variants.
6. Capturing feedback.
7. Maintaining audit trails.

CAF is NOT a business application.

CAF is infrastructure.

---

# What CAF Is NOT

Never implement:

- AI
- Machine Learning
- LLM integration
- Recommendation systems
- Prompt optimization
- Autonomous decision making
- Automatic rewriting
- Automatic inference

CAF is deterministic.

---

# Technology Stack

Backend

Python

UI

Streamlit

Storage

SQLite

Configuration

JSON

Validation

Pydantic

Testing

pytest

Formatting

Black

Linting

Ruff

Type Checking

MyPy

Environment

python-dotenv

---

# Architecture

Follow Clean Architecture.

Presentation

↓

Services

↓

Repositories

↓

Database

Models remain data-only.

Business logic belongs only inside Services.

Repositories perform persistence only.

UI must never contain business logic.

---

# Repository Structure

caf/

config/

database/

models/

repositories/

services/

templates/

tests/

ui/

utils/

docs/

---

# Current Project Status

## Completed

✅ Foundation Engineering

- configuration
- logging
- database initialization
- package structure

✅ Question Engine

- JSON configuration
- dynamic rendering
- QuestionService
- Streamlit form
- answer collection

---

## Current Milestone

Validation Engine

Context Builder

Objective

Transform raw user answers into a normalized Context Object.

---

## Pending Milestones

Instruction Assembly Engine

↓

Version Management

↓

Variant Management

↓

Feedback System

↓

Iteration Manager

↓

Complete Streamlit UI

↓

Testing

↓

Documentation

---

# Current Working Files

For the current milestone, AI agents should primarily inspect:

caf/services/question_service.py

caf/config/questions/default_questions.json

caf/ui/demo_app.py

The following files are expected to be created or modified:

caf/services/validation_service.py

caf/models/context.py

caf/services/context_builder.py

Avoid inspecting unrelated modules.

---

# Documentation Rules

The following files are permanent.

Never recreate them.

Always preserve history.

report.md

Append one new session.

Tasks.md

Mark completed tasks only.

Decision_Log.md

Append new architectural decisions.

Change_Log.md

Update only for milestone-level changes.

---

# Coding Standards

Follow:

PEP 8

SOLID

DRY

KISS

Type hints

Docstrings

Meaningful names

Configuration-driven design

No duplicated logic.

---

# Engineering Rules

Never hardcode questions.

Never hardcode templates.

Always prefer configuration.

Never mix UI and business logic.

Never bypass validation.

Never introduce functionality outside the SRS.

If a requirement is missing:

State:

"Not specified in the SRS."

Do not invent behaviour.

---

# AI Workflow

When starting a new session:

Read ONLY:

1. AI_CONTEXT.md
2. report.md
3. Tasks.md
4. Decision_Log.md

Do NOT recursively inspect the repository.

Only inspect source files explicitly required for the current milestone.

Avoid repository-wide searches.

Avoid globbing *.py or *.md unless explicitly requested.

---

# Current Progress

Overall Completion

≈ 25–30%

Current Milestone Completion

Question Engine

100%

Validation Engine

0%

Context Builder

0%

---

# Next Objective

Implement:

ValidationService

↓

Context Model

↓

ContextBuilder

↓

Integrate into Question Engine

↓

Update Documentation

Nothing beyond this milestone should be implemented without explicit instruction.

---

# Last Updated

Update this document ONLY when:

- phase changes
- milestone changes
- architecture changes
- repository structure changes

Do NOT update after every coding session.

Use report.md for session history.