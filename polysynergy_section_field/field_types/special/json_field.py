"""JSON field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="special", icon="braces.svg")
class JsonField(FieldType):
    """JSON field - stores structured data as JSONB"""

    handle = "json"
    label = "JSON"
    postgres_type = "JSONB"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "editorMode": {
                    "type": "string",
                    "enum": ["visual", "code", "both"],
                    "default": "both",
                    "title": "Editor Mode",
                    "description": "How to edit JSON data"
                },
                "schema": {
                    "type": "object",
                    "title": "JSON Schema",
                    "description": "JSON Schema for validation and form generation"
                },
                "defaultValue": {
                    "type": "object",
                    "title": "Default Value",
                    "description": "Default JSON object"
                },
                "prettify": {
                    "type": "boolean",
                    "default": True,
                    "title": "Pretty Print",
                    "description": "Format JSON with indentation"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "JsonCell",
            "props": {
                "value": value,
                "compact": True
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "JsonEditor",
            "props": {
                "editorMode": settings.get("editorMode", "both") if settings else "both",
                "schema": settings.get("schema") if settings else None,
                "defaultValue": settings.get("defaultValue") if settings else None,
                "prettify": settings.get("prettify", True) if settings else True
            }
        }
