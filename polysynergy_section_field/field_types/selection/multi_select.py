"""Multi-select field type - multiple choice"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="selection", icon="list-checks.svg")
class MultiSelectField(FieldType):
    """Multi-select field - multiple choices stored as JSON array"""

    handle = "multi_select"
    label = "Multi Select"
    postgres_type = "JSONB"

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
                "minSelections": {
                    "type": "integer",
                    "minimum": 0,
                    "title": "Minimum Selections",
                    "description": "Minimum number of required selections"
                },
                "maxSelections": {
                    "type": "integer",
                    "minimum": 1,
                    "title": "Maximum Selections",
                    "description": "Maximum number of allowed selections"
                },
                "searchable": {
                    "type": "boolean",
                    "default": True,
                    "title": "Searchable",
                    "description": "Enable search in options"
                }
            },
            "required": ["options"]
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        if not value or not isinstance(value, list):
            return {
                "component": "TextCell",
                "props": {"value": ""}
            }

        # Find labels for selected values
        options = settings.get("options", []) if settings else []
        labels = []
        for val in value:
            for option in options:
                if option.get("value") == val:
                    labels.append(option.get("label", val))
                    break

        return {
            "component": "TagsCell",
            "props": {
                "tags": labels
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "MultiSelect",
            "props": {
                "options": settings.get("options", []) if settings else [],
                "minSelections": settings.get("minSelections") if settings else None,
                "maxSelections": settings.get("maxSelections") if settings else None,
                "searchable": settings.get("searchable", True) if settings else True
            }
        }
