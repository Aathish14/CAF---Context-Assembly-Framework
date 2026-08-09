# Changelog

## v0.1.0 - Initial Release
**Date**: 2026-07-01

### Added
- Project structure
- SRS (Software Requirements Specification)
- PRD (Product Requirements Document)
- Architecture artifacts
- Technology Stack documentation
- Engineering documentation (this document, report.md, Tasks.md, Decision_Log.md)

## v0.2.0 - Foundation Engineering Complete
**Date**: 2026-07-01

### Added
- Complete Python package structure with __init__.py files
- Configuration management system (settings.py, constants.py)
- Database layer with SQLite connection management (db.py, schema.sql)
- Logging system with console and file output (logging.py)
- Environment variable template (.env.example)
- Enhanced .gitignore with additional patterns
- Comprehensive README with setup and usage instructions
- Fixed corrupted asyncio.queues.py file (critical Python 3.12.0 compatibility fix)
- Migration strategy documentation

### Changed
- Moved demo application to caf/ui/demo_app.py for proper structure
- Enhanced README with detailed project structure, setup instructions, and development workflow
- Updated Tasks.md to reflect completion of Phase 3 (Technology Familiarization)
- Added Decision 002 to Decision Log documenting foundation architecture approach

### Fixed
- Critical asyncio.queues.py corruption that was preventing import of streamlit and other asyncio-dependent packages
- Improved project organization to better match documented architecture

## v0.1.1 - Documentation Improvements
**Date**: 2026-07-01 (same day as v0.1.0 for tracking purposes)

### Added
- Decision_Log.md with initial documentation strategy decision
- Improved table of contents in README
- Better section organization in documentation files

### Known Issues
- None

---

## v0.3.0 - Sprint 1 Phase 2 Complete: Context Model & Builder
**Date**: 2026-07-03

### Added
- **Context Model** (`caf/models/context.py`): Pydantic BaseModel with 10 fields (objective, audience, tone, constraints, output_format, risk_level, language, word_limit, purpose, business_type)
- **Context Builder** (`caf/services/context_builder.py`): ContextBuilder class with build() method accepting validated answers dict, returning Context instance
- **Unit Tests** (`caf/tests/test_context_builder.py`): 11 tests covering successful creation, empty constraints, optional word_limit, invalid input handling, deterministic creation, field mapping, input preservation
- **Decision Log Entry**: Decision 004 documenting Context Model & Builder architecture

### Changed
- **UI Integration** (`caf/ui/demo_app.py`): Integrated ValidationService and ContextBuilder into form submission flow; displays validation errors, success message, Context object, and formatted JSON on success
- **Tasks.md**: Updated Phase 8 checkboxes - "Create context schema" and "Build context objects" marked complete
- **Report.md**: Added Session 3 documenting Sprint 1 Phase 2 completion

### Technical Details
- Flow: User Input → QuestionService → ValidationService → ContextBuilder → Context Object
- All validation errors shown before Context creation
- Deterministic Context creation with exact input preservation
- No persistence, no business logic in models, no UI coupling in services

---

## v0.4.0 - Sprint 2 Complete: Template Definition & Instruction Assembly
**Date**: 2026-07-03

### Added
- **Instruction Model** (`caf/models/instruction.py`): Pydantic BaseModel with 6 fields (id, template_name, context, assembled_instruction, created_at, version)
- **Template Model** (`caf/models/template.py`): Pydantic BaseModel with 8 fields (id, name, description, template_text, placeholders, category, version, created_at)
- **Template Repository** (`caf/config/templates/default_templates.json`): 3 templates (General Prompt, Business Analysis, Software Engineering) with placeholders
- **Template Service** (`caf/services/template_service.py`): TemplateService with load_templates(), get_all(), get_by_id(), get_by_category()
- **Instruction Builder** (`caf/services/instruction_builder.py`): InstructionBuilder with deterministic placeholder replacement via regex
- **Unit Tests** (`caf/tests/test_instruction_builder.py`): 11 tests covering creation, replacement, missing placeholders, invalid IDs, determinism, context inclusion, version defaults, created_at population
- **Decision Log Entries**: Decision 005 (Template & Instruction Architecture), Decision 006 (Placeholder Replacement Strategy)

### Changed
- **Tasks.md**: Updated Phase 9 and Phase 10 checkboxes - all template/instruction tasks marked complete
- **Report.md**: Added Session 4 documenting Sprint 2 completion
- **PROJECT_STATUS.md**: Updated sprint status, gates, pipeline, and progress

### Technical Details
- Flow: Context Object → TemplateService → InstructionBuilder → Instruction Object
- Placeholder replacement: regex `\{\{\{\{\{(\w+)\}\}} with context dict lookup, preserves missing keys
- Instruction captures full context snapshot + metadata for traceability
- Templates stored in JSON for non-developer modification
- No persistence, no AI generation, no optimization - pure deterministic assembly