"""Many-to-Many Relation field type"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="relation", icon="network.svg")
class RelationManyToManyField(FieldType):
    """
    Many-to-Many relation field.

    Example: Blog Posts ↔ Tags (posts have many tags, tags have many posts)

    This field requires a junction table to store the relationships.
    The junction table is automatically created with the field.

    Settings:
    - relatedSection: UUID of the related section
    - displayField: Which field to display (e.g., "name", "title")
    - junctionTableName: Custom name for junction table (optional)
    - allowDuplicates: Whether same entry can be linked multiple times
    - sortBy: Field to sort related items by
    - limit: Maximum number of relations allowed

    PostgreSQL: Creates junction table with two UUID foreign keys
    UI Component: relation-multi-select
    """

    handle = "relation_many_to_many"
    label = "Relation (Many-to-Many)"
    postgres_type = "JUNCTION_TABLE"  # Special marker
    ui_component = "relation-multi-select"

    @property
    def settings_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "relatedSection": {
                    "type": "string",
                    "format": "uuid",
                    "title": "Related Section",
                    "description": "The section this field links to"
                },
                "displayField": {
                    "type": "string",
                    "default": "title",
                    "title": "Display Field",
                    "description": "Which field to show in the selector"
                },
                "junctionTableName": {
                    "type": "string",
                    "title": "Junction Table Name (optional)",
                    "description": "Custom name for the linking table (auto-generated if empty)"
                },
                "allowDuplicates": {
                    "type": "boolean",
                    "default": False,
                    "title": "Allow Duplicates",
                    "description": "Whether the same entry can be linked multiple times"
                },
                "sortBy": {
                    "type": "string",
                    "default": "sort_order",
                    "title": "Sort By",
                    "description": "Field to sort related items by"
                },
                "sortOrder": {
                    "type": "string",
                    "enum": ["ASC", "DESC"],
                    "default": "ASC",
                    "title": "Sort Order"
                },
                "maxRelations": {
                    "type": "integer",
                    "minimum": 1,
                    "title": "Maximum Relations",
                    "description": "Maximum number of items that can be linked (optional)"
                }
            },
            "required": ["relatedSection", "displayField"]
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate many-to-many value (must be list of UUIDs)"""
        if value is None or value == []:
            return (True, None)

        if not isinstance(value, list):
            return (False, "Value must be a list of UUIDs")

        # Check max relations
        if settings:
            max_relations = settings.get("maxRelations")
            if max_relations and len(value) > max_relations:
                return (False, f"Maximum {max_relations} relations allowed")

        # Validate each UUID
        import uuid
        for item in value:
            if not isinstance(item, str):
                return (False, "Each relation must be a UUID string")
            try:
                uuid.UUID(item)
            except (ValueError, AttributeError):
                return (False, f"Invalid UUID format: {item}")

        # Check duplicates
        if settings and not settings.get("allowDuplicates", False):
            if len(value) != len(set(value)):
                return (False, "Duplicate relations are not allowed")

        return (True, None)

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """
        Generate SQL to create junction table.

        Junction table schema:
        - id (UUID primary key)
        - {source_table}_id (UUID foreign key)
        - {related_section}_id (UUID foreign key)
        - sort_order (INTEGER for ordering)
        - created_at (TIMESTAMP)
        """
        junction_table = settings.get("junctionTableName") if settings else None
        if not junction_table:
            # Auto-generate: {section}_{field_name}_relations
            junction_table = f"{{section}}_{field_name}_relations"

        # Note: {section} and {related_section} are placeholders
        # that will be replaced by the migration generator
        sql = f'''
-- Junction table for {field_name} many-to-many relation
CREATE TABLE IF NOT EXISTS "{junction_table}" (
    "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "source_id" UUID NOT NULL,
    "target_id" UUID NOT NULL,
    "sort_order" INTEGER DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY ("source_id") REFERENCES "{{section}}"("id") ON DELETE CASCADE,
    FOREIGN KEY ("target_id") REFERENCES "{{related_section}}"("id") ON DELETE CASCADE
);

-- Index for performance
CREATE INDEX "idx_{junction_table}_source" ON "{junction_table}"("source_id");
CREATE INDEX "idx_{junction_table}_target" ON "{junction_table}"("target_id");
'''

        # Add unique constraint if duplicates not allowed
        if settings and not settings.get("allowDuplicates", False):
            sql += f'''
-- Prevent duplicate relations
CREATE UNIQUE INDEX "idx_{junction_table}_unique" ON "{junction_table}"("source_id", "target_id");
'''

        return sql.strip()

    def get_table_cell_config(
        self,
        value: Any,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for table cell - show count with tags preview"""
        display_field = settings.get("displayField", "title") if settings else "title"

        return {
            "component": "RelationTagsCell",
            "props": {
                "value": value,  # List of UUIDs
                "relatedSection": settings.get("relatedSection") if settings else None,
                "displayField": display_field,
                "maxDisplay": 3,  # Show max 3 tags, then "+N more"
                "showCount": True,
            }
        }

    def get_form_input_config(
        self,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for form - multi-select with drag-drop reordering"""
        display_field = settings.get("displayField", "title") if settings else "title"
        max_relations = settings.get("maxRelations") if settings else None

        return {
            "component": "RelationMultiSelect",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "helpText": field_config.get("help_text") if field_config else None,
                "relatedSection": settings.get("relatedSection") if settings else None,
                "displayField": display_field,
                "searchable": True,
                "sortable": True,  # Drag-drop reordering
                "maxRelations": max_relations,
                "allowClear": True,
            },
            "validation": {
                "required": field_config.get("is_required", False) if field_config else False,
                "maxItems": max_relations,
            }
        }
