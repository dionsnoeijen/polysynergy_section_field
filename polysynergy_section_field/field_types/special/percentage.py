"""Percentage field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="special", icon="percent.svg")
class PercentageField(FieldType):
    """Percentage field - stores percentage values"""

    handle = "percentage"
    label = "Percentage"
    postgres_type = "NUMERIC(5,2)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "decimalPlaces": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 4,
                    "default": 2,
                    "title": "Decimal Places"
                },
                "minValue": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "default": 0,
                    "title": "Minimum Value"
                },
                "maxValue": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "default": 100,
                    "title": "Maximum Value"
                },
                "showSlider": {
                    "type": "boolean",
                    "default": False,
                    "title": "Show Slider",
                    "description": "Display as slider instead of input"
                },
                "step": {
                    "type": "number",
                    "default": 1,
                    "title": "Step",
                    "description": "Increment/decrement step"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "PercentageCell",
            "props": {
                "value": value,
                "decimalPlaces": settings.get("decimalPlaces", 2) if settings else 2
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "PercentageInput",
            "props": {
                "decimalPlaces": settings.get("decimalPlaces", 2) if settings else 2,
                "minValue": settings.get("minValue", 0) if settings else 0,
                "maxValue": settings.get("maxValue", 100) if settings else 100,
                "showSlider": settings.get("showSlider", False) if settings else False,
                "step": settings.get("step", 1) if settings else 1
            }
        }
