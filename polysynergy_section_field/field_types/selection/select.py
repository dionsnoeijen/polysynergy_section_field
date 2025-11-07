"""Select field type - single choice dropdown"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="selection", icon="list-dropdown.svg")
class SelectField(FieldType):
    """Select field - dropdown with single choice"""

    handle = "select"
    label = "Select (dropdown)"
    postgres_type = "VARCHAR(255)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "options": {
                    "type": "array",
                    "title": "Options",
                    "description": "Available choices",
                    "items": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "string",
                                "title": "Value"
                            },
                            "label": {
                                "type": "string",
                                "title": "Label"
                            }
                        },
                        "required": ["value", "label"]
                    },
                    "minItems": 1
                },
                "allowEmpty": {
                    "type": "boolean",
                    "default": True,
                    "title": "Allow Empty Selection",
                    "description": "Allow user to clear selection"
                },
                "searchable": {
                    "type": "boolean",
                    "default": False,
                    "title": "Searchable",
                    "description": "Enable search in dropdown"
                }
            },
            "required": ["options"]
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        # Find label for the value
        options = settings.get("options", []) if settings else []
        label = value
        for option in options:
            # Handle both dict format and string format
            if isinstance(option, dict):
                if option.get("value") == value:
                    label = option.get("label", value)
                    break
            elif isinstance(option, str):
                # If option is a string, use it directly
                if option == value:
                    label = option
                    break

        return {
            "component": "TextCell",
            "props": {
                "value": label
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "Select",
            "props": {
                "options": settings.get("options", []) if settings else [],
                "allowEmpty": settings.get("allowEmpty", True) if settings else True,
                "searchable": settings.get("searchable", False) if settings else False
            }
        }
