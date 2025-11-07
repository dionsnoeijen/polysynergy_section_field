"""Boolean field type"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="basic", icon="toggle.svg")
class BooleanField(FieldType):
    """
    Boolean field for true/false values.

    Settings:
    - defaultValue: Default value (true/false)

    PostgreSQL: BOOLEAN
    UI Component: toggle-switch
    """

    handle = "boolean"
    label = "True/False"
    postgres_type = "BOOLEAN"
    ui_component = "toggle-switch"

    @property
    def settings_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "defaultValue": {
                    "type": "boolean",
                    "default": False,
                    "title": "Default Value",
                    "description": "Default value for new entries"
                }
            }
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate boolean value"""
        if value is None:
            return (True, None)

        if not isinstance(value, bool):
            return (False, "Value must be a boolean (true or false)")

        return (True, None)

    def get_default_value(self, settings: Optional[Dict] = None) -> bool:
        """Get default value"""
        if settings and "defaultValue" in settings:
            return settings["defaultValue"]
        return False

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """Generate SQL for boolean field"""
        sql = f'"{field_name}" BOOLEAN'

        # Add default if specified
        default = self.get_default_value(settings)
        sql += f" DEFAULT {str(default).upper()}"

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
        return {
            "component": "BooleanCell",
            "props": {
                "value": value,
                "iconTrue": "✓",  # or "check-circle"
                "iconFalse": "✗",  # or "x-circle"
                "colorTrue": "green",
                "colorFalse": "red",
            }
        }

    def get_form_input_config(
        self,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for form input"""
        default_value = self.get_default_value(settings)

        return {
            "component": "Toggle",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "helpText": field_config.get("help_text") if field_config else None,
                "defaultValue": default_value,
            },
            "validation": {
                "required": field_config.get("is_required", False) if field_config else False,
            }
        }
