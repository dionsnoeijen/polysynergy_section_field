"""Plain text field type"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type
from polysynergy_section_field.section_field_runner.validation.validators import (
    validate_string_length,
    validate_regex_pattern
)


@field_type(category="basic", icon="text.svg")
class TextField(FieldType):
    """
    Plain text field for short text input.

    Settings:
    - maxLength: Maximum number of characters
    - minLength: Minimum number of characters
    - pattern: Regex pattern for validation

    PostgreSQL: VARCHAR(n) or TEXT
    UI Component: text-input
    """

    handle = "text"
    label = "Plain Text"
    postgres_type = "TEXT"
    ui_component = "text-input"

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
                "pattern": {
                    "type": "string",
                    "title": "Regex Pattern",
                    "description": "Regular expression for validation"
                },
                "placeholder": {
                    "type": "string",
                    "title": "Placeholder",
                    "description": "Placeholder text shown when field is empty"
                }
            }
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate text value"""
        if value is None:
            return (True, None)  # NULL is valid unless field is required

        if not isinstance(value, str):
            return (False, "Value must be a string")

        if settings:
            # Validate length
            max_len = settings.get("maxLength")
            min_len = settings.get("minLength")

            is_valid, error = validate_string_length(value, min_len, max_len)
            if not is_valid:
                return (is_valid, error)

            # Validate pattern
            pattern = settings.get("pattern")
            if pattern:
                is_valid, error = validate_regex_pattern(value, pattern)
                if not is_valid:
                    return (is_valid, error)

        return (True, None)

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """Generate SQL for text field"""
        max_len = settings.get("maxLength") if settings else None

        if max_len:
            sql = f'"{field_name}" VARCHAR({max_len})'
        else:
            sql = f'"{field_name}" TEXT'

        if is_required:
            sql += ' NOT NULL'

        return sql

    def get_table_cell_config(
        self,
        value: Any,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for table cell display"""
        max_len = settings.get("maxLength") if settings else None

        return {
            "component": "TextCell",
            "props": {
                "value": value,
                "truncate": True,
                "maxLength": max_len or 50,
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
        pattern = settings.get("pattern") if settings else None
        placeholder = settings.get("placeholder") if settings else None

        return {
            "component": "TextInput",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "placeholder": placeholder,
                "helpText": field_config.get("help_text") if field_config else None,
                "maxLength": max_len,
            },
            "validation": {
                "required": field_config.get("is_required", False) if field_config else False,
                "minLength": min_len,
                "maxLength": max_len,
                "pattern": pattern,
            }
        }
