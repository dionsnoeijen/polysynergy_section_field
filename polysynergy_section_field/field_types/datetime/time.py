"""Time field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="datetime", icon="clock.svg")
class TimeField(FieldType):
    """Time field - stores only time (no date)"""

    handle = "time"
    label = "Time"
    postgres_type = "TIME"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["HH:mm", "HH:mm:ss", "hh:mm A"],
                    "default": "HH:mm",
                    "title": "Time Format",
                    "description": "Display format for the time"
                },
                "step": {
                    "type": "integer",
                    "enum": [1, 5, 15, 30, 60],
                    "default": 15,
                    "title": "Step (minutes)",
                    "description": "Minutes increment in picker"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "TimeCell",
            "props": {
                "value": value,
                "format": settings.get("format", "HH:mm") if settings else "HH:mm"
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "TimePicker",
            "props": {
                "format": settings.get("format", "HH:mm") if settings else "HH:mm",
                "step": settings.get("step", 15) if settings else 15
            }
        }
