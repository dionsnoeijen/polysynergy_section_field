"""HTML field type for rich HTML content"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="basic", icon="code.svg")
class HtmlField(FieldType):
    """
    HTML editor field with Monaco editor and preview mode.

    Settings:
    - defaultMode: Default mode when opening editor ("edit" or "preview")
    - theme: Monaco editor theme (vs-dark, vs-light, etc.)

    PostgreSQL: TEXT
    UI Component: html-editor
    """

    handle = "html"
    label = "HTML Editor"
    postgres_type = "TEXT"
    ui_component = "html-editor"

    @property
    def settings_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "defaultMode": {
                    "type": "string",
                    "enum": ["edit", "preview"],
                    "default": "edit",
                    "title": "Default Mode",
                    "description": "Default mode when opening the editor"
                },
                "theme": {
                    "type": "string",
                    "enum": ["vs-dark", "vs-light"],
                    "default": "vs-dark",
                    "title": "Editor Theme",
                    "description": "Monaco editor color theme"
                },
                "maxLength": {
                    "type": "integer",
                    "minimum": 1,
                    "title": "Maximum Length",
                    "description": "Maximum number of characters allowed"
                }
            }
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate HTML value - no sanitization, allow all HTML"""
        if value is None:
            return (True, None)

        if not isinstance(value, str):
            return (False, "Value must be a string")

        # Check max length if specified
        if settings:
            max_len = settings.get("maxLength")
            if max_len and len(value) > max_len:
                return (False, f"HTML content exceeds maximum length of {max_len} characters")

        return (True, None)

    def get_table_cell_config(
        self,
        value: Any,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for table cell display - show HTML preview or code snippet"""
        return {
            "component": "HtmlCell",
            "props": {
                "value": value,
                "mode": "preview",  # Show rendered preview in table
                "maxHeight": 100,  # Limit height in table view
                "truncate": True,
            }
        }

    def get_form_input_config(
        self,
        settings: Optional[Dict] = None,
        field_config: Optional[Dict] = None
    ) -> Dict:
        """UI config for form input - Monaco editor with preview toggle"""
        default_mode = settings.get("defaultMode", "edit") if settings else "edit"
        theme = settings.get("theme", "vs-dark") if settings else "vs-dark"
        max_len = settings.get("maxLength") if settings else None

        return {
            "component": "HtmlEditor",
            "props": {
                "label": field_config.get("label") if field_config else None,
                "placeholder": field_config.get("placeholder") if field_config else None,
                "helpText": field_config.get("help_text") if field_config else None,
                "defaultMode": default_mode,  # edit or preview
                "theme": theme,  # Monaco theme
                "language": "html",  # Monaco language mode
                "maxLength": max_len,
                "showToggle": True,  # Show edit/preview toggle button
            },
            "validation": {
                "required": field_config.get("is_required", False) if field_config else False,
                "maxLength": max_len,
            }
        }
