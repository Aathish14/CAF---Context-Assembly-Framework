Context Assembly Framework (CAF) — Project Initialization Context
Project Background

The project is Context Assembly Framework (CAF).

CAF is an internal engineering framework, not a business-domain application.

It is not comparable to projects like:

Coffee Shop Management System
Hospital Management System
E-Commerce Platform
CRM
Inventory Management

Instead, CAF is an internal infrastructure framework whose purpose is to standardize the lifecycle of structured instructions.

The project follows a strict Software Requirements Specification (SRS), and every implementation decision must remain aligned with that SRS.

The SRS is considered the highest authority in the repository.

What CAF Is

CAF stands for Context Assembly Framework.

It is an internal web application/framework that:

Collects structured user inputs.
Converts those inputs into normalized Context Objects.
Assembles deterministic instructions using templates.
Tracks versions.
Supports variants.
Captures feedback.
Maintains complete audit trails.
Enables manual iteration.

CAF is essentially an Instruction Lifecycle Management Framework.

The lifecycle is:

User Input
      ↓
Question Engine
      ↓
Context Builder
      ↓
Instruction Assembly
      ↓
Version Control
      ↓
Variants
      ↓
Feedback
      ↓
Iteration
      ↓
Audit Trail
What CAF Is NOT

The SRS explicitly states that CAF is NOT:

an AI system
a machine learning system
an LLM product
a recommendation engine
an optimization engine
a decision-making system
a reinforcement learning system
a business application

CAF must never:

infer information
optimize instructions
rewrite instructions automatically
rank variants
make autonomous decisions
apply business logic

Everything must be user-driven.

Project Philosophy

CAF follows these principles:

Deterministic behaviour
Transparency
Manual control
Auditability
Modular architecture
Configuration-driven design
Separation of concerns
Local-first development
Minimal dependencies
Technology Stack

Approved technologies:

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

Version Control

Git

No external AI services.

No cloud dependencies.

No SQLAlchemy.

No FastAPI.

No Docker (Phase 1).

Repository Structure

Current repository:

D:\CAF

│   .gitignore
│   README.md
│   requirements.txt
│
├── caf
│   │   app.py
│   │
│   ├── config
│   ├── database
│   ├── models
│   ├── repositories
│   ├── services
│   ├── templates
│   ├── tests
│   ├── ui
│   └── utils
│
└── docs
    │   PRD.md
    │   SRS.pdf
    │   Phase_Wise_Tasks.md
    │   Tech_Stack.md
    │
    ├── architecture
    ├── database
    └── artifacts

This structure has already been finalized.

Existing Documentation

The repository already contains:

Core Documents
SRS
PRD
Technology Stack
Phase Wise Tasks
Architecture
System Architecture
Folder Structure
Database
Database Design
Artifacts
Project Charter
API Contracts
Domain Models
User Stories
Use Cases
NFR
Roadmap
Test Plan
Risk Register
Phase Status

Phase 1 has been completed conceptually.

Artifacts produced include:

Requirement Understanding Report
Scope Validation Report
Architecture Review
Module Responsibility Matrix
Project Glossary

The project is now considered understood.

Ambiguities Found

Only a few items remain unspecified in the SRS.

Authentication

Not specified.

Storage boundary

Recommendation:

JSON

Question definitions
Templates
Configuration

SQLite

Contexts
Instructions
Versions
Variants
Feedback
Iterations

Retention policy

Not specified.

These are documented rather than assumed.

Development Philosophy

The project will be built exactly like a professional enterprise software project.

The implementation order is:

Environment

↓

Database

↓

Models

↓

Repositories

↓

Services

↓

UI

↓

Testing

↓

Documentation

The UI should never contain business logic.

Repositories should never contain business logic.

Services contain business logic.

Models contain only data.

Documentation Strategy

The repository will maintain living documentation.

The following files must always remain updated.

report.md

Engineering journal.

Append-only.

Every implementation session adds:

work completed
files created
files modified
architectural decisions
outstanding work
next task
completion percentage
Tasks.md

Master checklist.

Contains every phase.

Completed tasks become

[x]

Incomplete remain

[ ]

This file is continuously updated.

Decision_Log.md

Architecture Decision Record.

Every significant engineering decision is appended.

Never overwritten.

Change_Log.md

Repository history.

Updated only after meaningful milestones.

Examples:

new module completed
architectural changes
releases
Rules for Future AI Sessions

Every future prompt must:

Read existing documentation before making changes.

Priority:

SRS

↓

PRD

↓

Tech Stack

↓

Architecture

↓

Database

↓

Artifacts

Never contradict the SRS.

Never introduce AI features.

Never introduce autonomous behaviour.

Never assume missing requirements.

If missing,

state:

"Not specified in the SRS."

Follow:

SOLID
Clean Architecture
Separation of Concerns
DRY
KISS

Use:

Python
Streamlit
SQLite
JSON

Only.

Every implementation prompt must update:

report.md
Tasks.md
Decision_Log.md

Update Change_Log.md only for significant milestones.

Never overwrite project history.

Always append.

Treat documentation as part of the implementation.

Implementation is incomplete until documentation has been updated.

Prompt Engineering Strategy

Every implementation prompt should:

Assign the AI a senior engineering role.

Provide repository context.

Provide project structure.

Provide documentation priority.

Specify current phase.

Specify current milestone.

Define constraints.

Define expected outputs.

Require documentation updates.

Require engineering reasoning.

Never simply ask for code.