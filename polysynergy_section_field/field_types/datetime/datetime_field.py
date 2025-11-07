"""DateTime field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="datetime", icon="calendar-clock.svg")
class DateTimeField(FieldType):
    """DateTime field - stores date and time"""

    handle = "datetime"
    label = "Date Time"
    postgres_type = "TIMESTAMP WITH TIME ZONE"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "dateFormat": {
                    "type": "string",
                    "enum": ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"],
                    "default": "YYYY-MM-DD",
                    "title": "Date Format"
                },
                "timeFormat": {
                    "type": "string",
                    "enum": ["HH:mm", "HH:mm:ss", "hh:mm A"],
                    "default": "HH:mm",
                    "title": "Time Format"
                },
                "timezone": {
                    "type": "boolean",
                    "default": True,
                    "title": "Show Timezone",
                    "description": "Display timezone information"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        date_format = settings.get("dateFormat", "YYYY-MM-DD") if settings else "YYYY-MM-DD"
        time_format = settings.get("timeFormat", "HH:mm") if settings else "HH:mm"
        return {
            "component": "DateTimeCell",
            "props": {
                "value": value,
                "format": f"{date_format} {time_format}"
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "DateTimePicker",
            "props": {
                "dateFormat": settings.get("dateFormat", "YYYY-MM-DD") if settings else "YYYY-MM-DD",
                "timeFormat": settings.get("timeFormat", "HH:mm") if settings else "HH:mm",
                "showTimezone": settings.get("timezone", True) if settings else True
            }
        }
