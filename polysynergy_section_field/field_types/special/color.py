"""Color field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="special", icon="palette.svg")
class ColorField(FieldType):
    """Color picker field - stores hex color code"""

    handle = "color"
    label = "Color"
    postgres_type = "VARCHAR(7)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["hex", "rgb", "rgba"],
                    "default": "hex",
                    "title": "Color Format",
                    "description": "Format to store color value"
                },
                "allowAlpha": {
                    "type": "boolean",
                    "default": False,
                    "title": "Allow Transparency",
                    "description": "Allow alpha channel (transparency)"
                },
                "presetColors": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^#[0-9A-Fa-f]{6}$"
                    },
                    "title": "Preset Colors",
                    "description": "Quick-select color palette"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "ColorCell",
            "props": {
                "value": value,
                "showValue": True
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "ColorPicker",
            "props": {
                "format": settings.get("format", "hex") if settings else "hex",
                "allowAlpha": settings.get("allowAlpha", False) if settings else False,
                "presetColors": settings.get("presetColors") if settings else None
            }
        }
