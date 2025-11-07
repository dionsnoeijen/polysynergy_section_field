"""Slug field type - URL-friendly identifier"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="validated", icon="hash.svg")
class SlugField(FieldType):
    """Slug field - URL-friendly string (lowercase, hyphens, no spaces)"""

    handle = "slug"
    label = "Slug"
    postgres_type = "VARCHAR(255)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "autoGenerate": {
                    "type": "boolean",
                    "default": True,
                    "title": "Auto-Generate from Title",
                    "description": "Automatically create slug from title field"
                },
                "sourceField": {
                    "type": "string",
                    "title": "Source Field",
                    "description": "Field to generate slug from (usually 'title' or 'name')"
                },
                "allowEdit": {
                    "type": "boolean",
                    "default": True,
                    "title": "Allow Manual Edit",
                    "description": "Allow user to manually edit the slug"
                },
                "prefix": {
                    "type": "string",
                    "title": "Prefix",
                    "description": "Prefix to add to all slugs",
                    "pattern": "^[a-z0-9-]*$"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "CodeCell",
            "props": {
                "value": value,
                "monospace": True
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "SlugInput",
            "props": {
                "autoGenerate": settings.get("autoGenerate", True) if settings else True,
                "sourceField": settings.get("sourceField") if settings else None,
                "allowEdit": settings.get("allowEdit", True) if settings else True,
                "prefix": settings.get("prefix") if settings else None,
                "validation": {
                    "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
                    "message": "Only lowercase letters, numbers, and hyphens allowed"
                }
            }
        }
