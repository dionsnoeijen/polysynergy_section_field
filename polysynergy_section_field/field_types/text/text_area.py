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
