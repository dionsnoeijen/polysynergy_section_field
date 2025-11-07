"""Currency field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="special", icon="currency-dollar.svg")
class CurrencyField(FieldType):
    """Currency field - stores monetary values"""

    handle = "currency"
    label = "Currency"
    postgres_type = "NUMERIC(10,2)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "currency": {
                    "type": "string",
                    "enum": ["USD", "EUR", "GBP", "JPY", "CNY", "INR", "AUD", "CAD", "CHF", "NZD"],
                    "default": "USD",
                    "title": "Currency",
                    "description": "Currency code (ISO 4217)"
                },
                "displayFormat": {
                    "type": "string",
                    "enum": ["symbol", "code", "name"],
                    "default": "symbol",
                    "title": "Display Format",
                    "description": "How to display currency ($ vs USD vs US Dollar)"
                },
                "decimalPlaces": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 4,
                    "default": 2,
                    "title": "Decimal Places"
                },
                "allowNegative": {
                    "type": "boolean",
                    "default": False,
                    "title": "Allow Negative Values"
                },
                "minValue": {
                    "type": "number",
                    "title": "Minimum Value"
                },
                "maxValue": {
                    "type": "number",
                    "title": "Maximum Value"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "CurrencyCell",
            "props": {
                "value": value,
                "currency": settings.get("currency", "USD") if settings else "USD",
                "displayFormat": settings.get("displayFormat", "symbol") if settings else "symbol"
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "CurrencyInput",
            "props": {
                "currency": settings.get("currency", "USD") if settings else "USD",
                "displayFormat": settings.get("displayFormat", "symbol") if settings else "symbol",
                "decimalPlaces": settings.get("decimalPlaces", 2) if settings else 2,
                "allowNegative": settings.get("allowNegative", False) if settings else False,
                "minValue": settings.get("minValue") if settings else None,
                "maxValue": settings.get("maxValue") if settings else None
            }
        }
