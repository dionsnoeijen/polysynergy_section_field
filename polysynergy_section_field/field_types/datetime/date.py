"""Date field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="datetime", icon="calendar.svg")
class DateField(FieldType):
    """Date field - stores only date (no time)"""

    handle = "date"
    label = "Date"
    postgres_type = "DATE"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"],
                    "default": "YYYY-MM-DD",
                    "title": "Date Format",
                    "description": "Display format for the date"
                },
                "minDate": {
                    "type": "string",
                    "format": "date",
                    "title": "Minimum Date",
                    "description": "Earliest allowed date"
                },
                "maxDate": {
                    "type": "string",
                    "format": "date",
                    "title": "Maximum Date",
                    "description": "Latest allowed date"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "DateCell",
            "props": {
                "value": value,
                "format": settings.get("format", "YYYY-MM-DD") if settings else "YYYY-MM-DD"
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "DatePicker",
            "props": {
                "format": settings.get("format", "YYYY-MM-DD") if settings else "YYYY-MM-DD",
                "minDate": settings.get("minDate") if settings else None,
                "maxDate": settings.get("maxDate") if settings else None
            }
        }
