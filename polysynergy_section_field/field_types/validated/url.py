"""URL field type with validation"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="validated", icon="link.svg")
class UrlField(FieldType):
    """URL field with validation"""

    handle = "url"
    label = "URL"
    postgres_type = "VARCHAR(500)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "requireProtocol": {
                    "type": "boolean",
                    "default": True,
                    "title": "Require Protocol",
                    "description": "URL must start with http:// or https://"
                },
                "allowedProtocols": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["http", "https", "ftp", "mailto", "tel"]
                    },
                    "default": ["http", "https"],
                    "title": "Allowed Protocols"
                },
                "openInNewTab": {
                    "type": "boolean",
                    "default": True,
                    "title": "Open in New Tab",
                    "description": "Open links in new browser tab"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "LinkCell",
            "props": {
                "value": value,
                "openInNewTab": settings.get("openInNewTab", True) if settings else True
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "UrlInput",
            "props": {
                "requireProtocol": settings.get("requireProtocol", True) if settings else True,
                "allowedProtocols": settings.get("allowedProtocols", ["http", "https"]) if settings else ["http", "https"],
                "validation": {
                    "type": "url"
                }
            }
        }
