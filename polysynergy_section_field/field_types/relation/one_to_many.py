"""One-to-Many Relation field type"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="relation", icon="list-tree.svg")
class RelationOneToManyField(FieldType):
    """
    One-to-Many relation field (virtual/computed field).

    Example: Author → Blog Posts (one author has many posts)

    This is a VIRTUAL field - it doesn't store data in a column.
    Instead, it shows related entries from another section that reference this entry.

    Settings:
    - relatedSection: UUID of the section with the many-to-one relation
    - relatedField: Handle of the field in that section that points back
    - displayField: Which field to display in the list
    - limit: Maximum number of items to show

    PostgreSQL: No column (virtual field)
    UI Component: relation-list
    """

    handle = "relation_one_to_many"
    label = "Relation (One-to-Many)"
    postgres_type = "VIRTUAL"  # Special marker - no actual column
    ui_component = "relation-list"

    @property
    def settings_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "relatedSection": {
                    "type": "string",
                    "format": "uuid",
                    "title": "Related Section",
                    "description": "The section that contains the many-to-one field"
                },
                "relatedField": {
                    "type": "string",
                    "title": "Related Field Handle",
                    "description": "The handle of the many-to-one field in the related section"
                },
                "displayField": {
                    "type": "string",
                    "default": "title",
                    "title": "Display Field",
                    "description": "Which field to show in the list"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 10,
                    "title": "Display Limit",
                    "description": "Maximum number of related items to show"
                },
                "sortBy": {
                    "type": "string",
                    "default": "created_at",
                    "title": "Sort By",
                    "description": "Field to sort by"
                },
                "sortOrder": {
                    "type": "string",
                    "enum": ["ASC", "DESC"],
                    "default": "DESC",
                    "title": "Sort Order"
                }
            },
            "required": ["relatedSection", "relatedField"]
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Virtual fields don't store values, always valid"""
        return (True, None)

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """Virtual fields don't create columns"""
        return ""  # Empty SQL - no column needed

    def get_table_cell_config(
        self,
        value: Any,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for table cell - show count"""
        return {
            "component": "RelationCountCell",
            "props": {
                "relatedSection": settings.get("relatedSection") if settings else None,
                "relatedField": settings.get("relatedField") if settings else None,
                "showCount": True,
            }
        }

    def get_form_input_config(
        self,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for form - list of related entries with actions"""
        display_field = settings.get("displayField", "title") if settings else "title"
        limit = settings.get("limit", 10) if settings else 10

        return {
            "component": "RelationList",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "helpText": field_config.get("help_text") if field_config else None,
                "relatedSection": settings.get("relatedSection") if settings else None,
                "relatedField": settings.get("relatedField") if settings else None,
                "displayField": display_field,
                "limit": limit,
                "sortBy": settings.get("sortBy", "created_at") if settings else "created_at",
                "sortOrder": settings.get("sortOrder", "DESC") if settings else "DESC",
                "allowAdd": True,
                "allowRemove": True,
                "allowReorder": False,
            },
            "validation": {}  # Virtual field has no validation
        }
