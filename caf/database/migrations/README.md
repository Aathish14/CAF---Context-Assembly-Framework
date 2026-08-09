# Database Migrations

## Migration Strategy

For the Context Assembly Framework (CAF), we use a simple SQL-based migration approach:

1. **Initial Schema**: The initial database schema is defined in `schema.sql`
2. **Versioned Migrations**: Schema changes are managed via numbered SQL migration files
3. **Applied Tracking**: Applied migrations are tracked in a `schema_migrations` table

## Migration File Naming Convention

Migration files should be named as:
```
V{version}__description.sql
```

Examples:
- `V1__initial_schema.sql`
- `V2__add_feedback_column_comment: Adding a migration1. Create the migration file

Let me complete this thought and then continue with the migration README.

I'll write a proper README for migrations explaining the versioned approach.

<tool_call>
<function=write>
<parameter=content>
# Database Migrations

## Migration Strategy

For the Context Assembly Framework (CAF), we use a simple SQL-based migration approach:

1. **Initial Schema**: The initial database schema is defined in `schema.sql`
2. **Versioned Migrations**: Schema changes are managed via numbered SQL migration files
3. **Applied Tracking**: Applied migrations are tracked in a `schema_migrations` table

## Migration File Naming Convention

Migration files should be named as:
```
V{version}__<description>.sql
```

Examples:
- `V1__initial_schema.sql`
- `V2__add_feedback_table.sql`
- `V3__add_indexes_performance.sql`

## Migration Process

1. Create a new SQL migration file with the next version number
2. Add the SQL statements needed for the schema change
3. The migration system will automatically apply unapplied migrations on startup
4. Each migration is wrapped in a transaction and recorded in the `schema_migrations` table

## Initial Setup

On first application startup:
1. The `schema_migrations` table is created if it doesn't exist
2. The initial schema from `schema.sql` is applied
3. Any pending migrations are applied in version order

## Example Migration

```sql
-- V2__add_feedback_table.sql
-- Add feedback table for user ratings and comments

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instruction_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instruction_id) REFERENCES instructions(id) ON DELETE CASCADE
);

-- Insert migration record
INSERT INTO schema_migrations (version, applied_at) 
VALUES (2, CURRENT_TIMESTAMP);
```