# Architecture Review

**Project**: Context Assembly Framework (CAF)
**Phase**: Phase 1 — Conceptual Orientation

## 1. Modules and Components
CAF is decomposed into the following core modules:
1. **Presentation Layer (UI)**: Built with Streamlit, handling all user interactions, dynamic form rendering, and input capture.
2. **Question Engine**: Manages JSON-based question schemas, evaluation of conditional rules, and declarative UI configuration.
3. **Context Builder (Validation)**: Validates raw answers against Pydantic models to produce normalized, immutable Context Objects.
4. **Instruction Assembly Engine**: Uses deterministic template substitution to merge Context Objects with JSON templates.
5. **Version Control System**: Manages instruction lineage, immutability, timestamps, diffing, and version tracking.
6. **Variant Management Module**: Handles the creation and lineage tracking of structural alternatives of instructions.
7. **Feedback & Signal Capture**: Records external signals (ratings, tags) against specific instruction versions.
8. **Iteration & Loop Control**: Manages user-initiated workflows (regenerations) and maintains the audit trail.
9. **Persistence Layer**: Handles CRUD operations via SQLite and JSON, enforcing referential integrity.

## 2. Layer Separation & Responsibilities
Following Clean Architecture and SOLID principles, the layers are strictly separated:
- **UI Layer (`caf/ui/`, `caf/app.py`)**: Strictly presentation. Contains no business rules, no SQL, and no interpretation logic. It only renders what the services dictate and captures user input.
- **Service Layer (`caf/services/`)**: Contains the business logic (Question Engine, Assembly Engine, Versioning). Coordinates between models and repositories.
- **Domain Layer (`caf/models/`)**: Pydantic models defining the core data structures (Question, Context, Instruction, Version, Variant, Feedback).
- **Repository Layer (`caf/repositories/`)**: Abstracts the SQLite/JSON database interactions. Ensures that services are decoupled from the specific storage mechanism.
- **Configuration Layer (`caf/config/`, `caf/templates/`)**: Stores declarative JSON definitions for questions and structural templates.

## 3. Dependencies
- **UI**: Depends on Streamlit.
- **Validation**: Depends on Pydantic.
- **Storage**: Depends on standard library `sqlite3` and `json`.
- **Environment**: Depends on `python-dotenv`.
- **Code Quality**: `pytest`, `black`, `ruff`, `mypy`.
- *Crucially, modules depend inward. The UI depends on Services. Services depend on Models and Repositories. Models have no outward dependencies.*

## 4. Data Flow
1. **Load Configuration**: UI requests questions from QuestionService. QuestionService loads JSON schema via Config layer.
2. **Input Capture**: User submits answers via UI.
3. **Validation & Normalization**: UI passes raw dict to ContextService. ContextService uses Pydantic to validate and create a Context Model.
4. **Assembly**: Context Model is passed to InstructionService. InstructionService loads Template, performs deterministic substitution, and generates Instruction Model.
5. **Persistence**: InstructionService passes Instruction Model to InstructionRepository for SQLite insertion.
6. **Versioning/Iteration**: Any manual edit or regeneration passes through VersionService, which creates a new Version Model linked to the parent Instruction.
7. **Feedback**: User submits rating in UI, passed to FeedbackService, linked via foreign key to Version Model in DB.

## 5. Potential Implementation Risks
- **Scope Creep (High Risk)**: The temptation to add "smart" parsing or AI-driven generation into the assembly pipeline. *Mitigation: Strict enforcement of deterministic, template-based assembly during PR reviews.*
- **Tight Coupling (Medium Risk)**: UI logic mixing with business logic, especially in Streamlit where event loops can blur boundaries. *Mitigation: Rigid abstraction of UI state from service execution; passing only primitives/DTOs between UI and services.*
- **Referential Integrity (High Risk)**: Disconnected variants or feedback due to complex iteration chains. *Mitigation: SQLite Foreign Key enforcement and comprehensive integration tests for the repository layer.*
- **Configuration Complexity (Medium Risk)**: Managing deeply nested conditional rules in JSON for the Question Engine. *Mitigation: Keep the schema flat and use simple boolean/dependency arrays for visibility rules.*
