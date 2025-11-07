"""Phone field type with validation"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="validated", icon="phone.svg")
class PhoneField(FieldType):
    """Phone number field with validation"""

    handle = "phone"
    label = "Phone Number"
    postgres_type = "VARCHAR(50)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["international", "national", "E.164"],
                    "default": "international",
                    "title": "Phone Format",
                    "description": "Expected phone number format"
                },
                "defaultCountry": {
                    "type": "string",
                    "title": "Default Country Code",
                    "description": "Default country for phone numbers (e.g., 'US', 'NL', 'GB')",
                    "pattern": "^[A-Z]{2}$"
                },
                "showCountrySelector": {
                    "type": "boolean",
                    "default": True,
                    "title": "Show Country Selector",
                    "description": "Allow user to select country"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "PhoneCell",
            "props": {
                "value": value
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "PhoneInput",
            "props": {
                "format": settings.get("format", "international") if settings else "international",
                "defaultCountry": settings.get("defaultCountry") if settings else None,
                "showCountrySelector": settings.get("showCountrySelector", True) if settings else True,
                "validation": {
                    "type": "phone"
                }
            }
        }
