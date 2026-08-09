-- Database schema for Context Assembly Framework (CAF)
-- Matches current Pydantic models EXACTLY
-- Only tables for models that are persisted via repositories: Instruction, Version, Variant

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Instructions table
-- Maps directly to Instruction model fields
DROP TABLE IF EXISTS instructions;
CREATE TABLE instructions (
    id TEXT PRIMARY KEY,                          -- Instruction.id
    template_name TEXT NOT NULL,                  -- Instruction.template_name
    context TEXT NOT NULL,                        -- Instruction.context (JSON)
    assembled_instruction TEXT NOT NULL,          -- Instruction.assembled_instruction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Instruction.created_at
    version INTEGER DEFAULT 1                     -- Instruction.version
);

-- Indexes for instructions
CREATE INDEX idx_instructions_created_at ON instructions(created_at);
CREATE INDEX idx_instructions_template_name ON instructions(template_name);

-- Versions table
-- Maps directly to Version model fields
DROP TABLE IF EXISTS versions;
CREATE TABLE versions (
    id TEXT PRIMARY KEY,                          -- Version.id
    instruction_id TEXT NOT NULL,                 -- Version.instruction_id
    version_number INTEGER NOT NULL,              -- Version.version_number
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Version.created_at
    created_by TEXT,                              -- Version.created_by
    change_summary TEXT NOT NULL,                 -- Version.change_summary
    parent_version_id TEXT,                       -- Version.parent_version_id
    FOREIGN KEY (instruction_id) REFERENCES instructions(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_version_id) REFERENCES versions(id) ON DELETE SET NULL,
    UNIQUE(instruction_id, version_number)
);

-- Indexes for versions
CREATE INDEX idx_versions_instruction_id ON versions(instruction_id);
CREATE INDEX idx_versions_parent_version_id ON versions(parent_version_id);
CREATE INDEX idx_versions_created_at ON versions(created_at);

-- Variants table
-- Maps directly to Variant model fields
DROP TABLE IF EXISTS variants;
CREATE TABLE variants (
    id TEXT PRIMARY KEY,                          -- Variant.id
    version_id TEXT NOT NULL,                     -- Variant.version_id
    variant_name TEXT NOT NULL,                   -- Variant.variant_name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Variant.created_at
    parent_variant_id TEXT,                       -- Variant.parent_variant_id
    description TEXT,                             -- Variant.description
    FOREIGN KEY (version_id) REFERENCES versions(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_variant_id) REFERENCES variants(id) ON DELETE SET NULL
);

-- Indexes for variants
CREATE INDEX idx_variants_version_id ON variants(version_id);
CREATE INDEX idx_variants_parent_variant_id ON variants(parent_variant_id);
CREATE INDEX idx_variants_created_at ON variants(created_at);