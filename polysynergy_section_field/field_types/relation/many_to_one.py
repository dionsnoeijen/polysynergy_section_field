"""Many-to-One Relation field type"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="relation", icon="link.svg")
class RelationManyToOneField(FieldType):
    """
    Many-to-One relation field.

    Example: Blog Post → Author (many posts belong to one author)

    This field stores a UUID reference to a single entry in another section.

    Settings:
    - relatedSection: UUID of the related section
    - displayField: Which field to display (e.g., "title", "name")
    - allowNull: Whether the relation can be null
    - onDelete: What to do when related entry is deleted (CASCADE, SET_NULL, RESTRICT)

    PostgreSQL: UUID with FOREIGN KEY
    UI Component: relation-select
    """

    handle = "relation_many_to_one"
    label = "Relation (Many-to-One)"
    postgres_type = "UUID"
    ui_component = "relation-select"

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
                    "description": "Which field to show in the selector (e.g., 'title', 'name')"
                },
                "allowNull": {
                    "type": "boolean",
                    "default": True,
                    "title": "Allow Empty",
                    "description": "Whether this relation can be empty"
                },
                "onDelete": {
                    "type": "string",
                    "enum": ["CASCADE", "SET_NULL", "RESTRICT"],
                    "default": "SET_NULL",
                    "title": "On Delete",
                    "description": "What happens when the related entry is deleted"
                }
            },
            "required": ["relatedSection", "displayField"]
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate relation value (must be UUID or None)"""
        if value is None:
            allow_null = settings.get("allowNull", True) if settings else True
            if not allow_null:
                return (False, "This relation is required")
            return (True, None)

        # Check if it's a valid UUID format (string check)
        if not isinstance(value, str):
            return (False, "Relation value must be a UUID string")

        # Basic UUID format validation
        try:
            import uuid
            uuid.UUID(value)
            return (True, None)
        except (ValueError, AttributeError):
            return (False, "Invalid UUID format")

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """Generate SQL for many-to-one relation with FOREIGN KEY constraint"""
        sql = f'"{field_name}" UUID'

        allow_null = settings.get("allowNull", True) if settings else True
        if is_required or not allow_null:
            sql += ' NOT NULL'

        # Add FOREIGN KEY constraint if relatedSection is specified
        # Note: This requires the related table to exist first
        # The migration service should handle dependency order
        if settings and 'relatedSection' in settings:
            # We'll need to get the table name from the section
            # For now, we'll add a note that FK should be added separately
            # via ALTER TABLE after both tables exist
            pass

        return sql

    def get_index_sql(
        self,
        table_name: str,
        field_name: str,
        settings: Optional[Dict] = None
    ) -> Optional[str]:
        """Create index on foreign key"""
        return f'CREATE INDEX idx_{table_name}_{field_name} ON {table_name}("{field_name}");'

    def get_foreign_key_sql(
        self,
        schema_name: str,
        table_name: str,
        field_name: str,
        related_schema: str,
        related_table: str,
        settings: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Generate FOREIGN KEY constraint SQL.

        This should be called separately after both tables exist.

        Args:
            schema_name: Current table's schema
            table_name: Current table name
            field_name: Current field/column name
            related_schema: Related table's schema
            related_table: Related table name
            settings: Field settings (contains onDelete behavior)

        Returns:
            ALTER TABLE SQL with FOREIGN KEY constraint
        """
        if not settings or 'relatedSection' not in settings:
            return None

        on_delete = settings.get('onDelete', 'SET NULL')

        # Build constraint name
        constraint_name = f"fk_{table_name}_{field_name}"

        # Build FOREIGN KEY SQL
        sql = f"""
ALTER TABLE "{schema_name}"."{table_name}"
ADD CONSTRAINT "{constraint_name}"
FOREIGN KEY ("{field_name}")
REFERENCES "{related_schema}"."{related_table}" (id)
ON DELETE {on_delete};
        """.strip()

        return sql

    def get_table_cell_config(
        self,
        value: Any,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for table cell - show related entry title"""
        display_field = settings.get("displayField", "title") if settings else "title"
        related_section = settings.get("relatedSection") if settings else None

        return {
            "component": "RelationCell",
            "props": {
                "value": value,  # UUID
                "relatedSection": related_section,
                "displayField": display_field,
                "linkable": True,  # Can click to navigate
            }
        }

    def get_form_input_config(
        self,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for form input - searchable dropdown"""
        display_field = settings.get("displayField", "title") if settings else "title"
        related_section = settings.get("relatedSection") if settings else None
        allow_null = settings.get("allowNull", True) if settings else True

        return {
            "component": "RelationSelect",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "helpText": field_config.get("help_text") if field_config else None,
                "relatedSection": related_section,
                "displayField": display_field,
                "searchable": True,
                "allowClear": allow_null,
            },
            "validation": {
                "required": field_config.get("is_required", False) if field_config else False,
            }
        }
