# Module Responsibility Matrix

| Module | Purpose | Inputs | Outputs | Dependencies | Storage Requirements | Owner Layer |
|--------|---------|--------|---------|--------------|----------------------|-------------|
| **UI (Streamlit)** | Render forms, capture inputs, display comparisons and history. | User interactions, DTOs from Services. | User actions, Raw Input Dictionaries. | Streamlit, Services | None (Stateless) | Presentation |
| **Question Engine** | Provide declarative question schemas, evaluate visibility logic. | JSON Configuration | Question Models, Validation Rules. | Models, Config | Read-only (JSON) | Service |
| **Context Builder** | Validate raw inputs and construct normalized context structures. | Raw Input Dictionaries, Question schemas. | Validated Context Object (Model). | Models, Pydantic | SQLite (`contexts` table) | Service |
| **Instruction Assembly**| Map context values into templates deterministically. | Context Object, Template JSON. | Assembled Instruction Object. | Models, Config | SQLite (`instructions` table) | Service |
| **Version Control** | Track edits, maintain immutability, provide diffs. | Instruction Object, Manual Edits. | Version Object, Diff Data. | Models | SQLite (`instruction_versions`) | Service |
| **Variant Manager** | Create structural alternatives sharing the same context. | Context Object, Parent Instruction ID. | Variant Object. | Models | SQLite (`instruction_variants`)| Service |
| **Feedback Capture** | Log user ratings and tags against versions. | Version ID, Rating (1-5), Tags. | Feedback Signal Object. | Models | SQLite (`feedback_signals`) | Service |
| **Iteration Control** | Track the chain of regenerations and context modifications. | User Action, Context Object, Old Version ID. | Iteration Link Object. | Models, Version Control| SQLite (`iteration_links`) | Service |
| **Repositories** | Abstract SQLite database operations. | Domain Models | Domain Models, Booleans (Success) | `sqlite3`, Models | SQLite Database | Persistence |
