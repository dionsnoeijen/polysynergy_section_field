"""Text area field type for multi-line text"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type
from polysynergy_section_field.section_field_runner.validation.validators import validate_string_length


@field_type(category="basic", icon="text_area.svg")
class TextAreaField(FieldType):
    """
    Multi-line text area field.

    Settings:
    - maxLength: Maximum number of characters
    - minLength: Minimum number of characters
    - rows: Number of rows to display in UI

    PostgreSQL: TEXT
    UI Component: textarea
    """

    handle = "textarea"
    label = "Text Area"
    postgres_type = "TEXT"
    ui_component = "textarea"

    @property
    def settings_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "maxLength": {
                    "type": "integer",
                    "minimum": 1,
                    "title": "Maximum Length",
                    "description": "Maximum number of characters allowed"
                },
                "minLength": {
                    "type": "integer",
                    "minimum": 0,
                    "title": "Minimum Length",
                    "description": "Minimum number of characters required"
                },
                "rows": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 5,
                    "title": "Rows",
                    "description": "Number of rows to display in UI"
                },
                "editorType": {
                    "type": "string",
                    "enum": ["plain", "rich", "markdown"],
                    "default": "plain",
                    "title": "Editor Type",
                    "description": "Type of editor to use (plain text, rich text, or markdown)"
                }
            }
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate textarea value"""
        if value is None:
            return (True, None)

        if not isinstance(value, str):
            return (False, "Value must be a string")

        if settings:
            max_len = settings.get("maxLength")
            min_len = settings.get("minLength")

            is_valid, error = validate_string_length(value, min_len, max_len)
            if not is_valid:
                return (is_valid, error)

        return (True, None)

    def get_table_cell_config(
        self,
        value: Any,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for table cell display - show preview of first line"""
        return {
            "component": "TextCell",
            "props": {
                "value": value,
                "truncate": True,
                "maxLength": 100,  # Show more for multiline preview
                "singleLine": True,  # Collapse to single line in table
            }
        }

    def get_form_input_config(
        self,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for form input"""
        max_len = settings.get("maxLength") if settings else None
        min_len = settings.get("minLength") if settings else None
        rows = settings.get("rows", 5) if settings else 5
        editor_type = settings.get("editorType", "plain") if settings else "plain"

        return {
            "component": "TextArea",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "placeholder": field_config.get("placeholder") if field_config else None,
                "helpText": field_config.get("help_text") if field_config else None,
                "rows": rows,
                "maxLength": max_len,
                "editorType": editor_type,  # plain, rich, or markdown
            },
            "validation": {
                "required": field_config.get("is_required", False) if field_config else False,
                "minLength": min_len,
                "maxLength": max_len,
            }
        }
