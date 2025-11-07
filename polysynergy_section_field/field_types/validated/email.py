"""Email field type with validation"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="validated", icon="at-sign.svg")
class EmailField(FieldType):
    """Email field with validation"""

    handle = "email"
    label = "Email"
    postgres_type = "VARCHAR(255)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "allowMultiple": {
                    "type": "boolean",
                    "default": False,
                    "title": "Allow Multiple Emails",
                    "description": "Allow comma-separated email addresses"
                },
                "domainRestriction": {
                    "type": "string",
                    "title": "Restrict Domain",
                    "description": "Only allow emails from this domain (e.g., 'company.com')",
                    "pattern": "^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\\.[a-zA-Z]{2,}$"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "EmailCell",
            "props": {
                "value": value
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "EmailInput",
            "props": {
                "allowMultiple": settings.get("allowMultiple", False) if settings else False,
                "domainRestriction": settings.get("domainRestriction") if settings else None,
                "validation": {
                    "type": "email"
                }
            }
        }
