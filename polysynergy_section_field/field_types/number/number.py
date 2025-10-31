"""Number field type"""

from typing import Any, Dict, Optional, Tuple

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type
from polysynergy_section_field.section_field_runner.validation.validators import validate_number_range


@field_type(category="number", icon="number.svg")
class NumberField(FieldType):
    """
    Number field for integers and decimals.

    Settings:
    - min: Minimum value
    - max: Maximum value
    - step: Step increment
    - allowDecimals: Whether to allow decimal values

    PostgreSQL: INTEGER or DECIMAL
    UI Component: number-input
    """

    handle = "number"
    label = "Number"
    postgres_type = "DECIMAL"
    ui_component = "number-input"

    @property
    def settings_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "min": {
                    "type": "number",
                    "title": "Minimum Value",
                    "description": "Minimum allowed value"
                },
                "max": {
                    "type": "number",
                    "title": "Maximum Value",
                    "description": "Maximum allowed value"
                },
                "step": {
                    "type": "number",
                    "default": 1,
                    "minimum": 0.000001,
                    "title": "Step",
                    "description": "Step increment for input"
                },
                "allowDecimals": {
                    "type": "boolean",
                    "default": True,
                    "title": "Allow Decimals",
                    "description": "Allow decimal/float values"
                }
            }
        }

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """Validate number value"""
        if value is None:
            return (True, None)

        if not isinstance(value, (int, float)):
            return (False, "Value must be a number")

        if settings:
            min_val = settings.get("min")
            max_val = settings.get("max")
            allow_decimals = settings.get("allowDecimals", True)

            is_valid, error = validate_number_range(value, min_val, max_val, allow_decimals)
            if not is_valid:
                return (is_valid, error)

        return (True, None)

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """Generate SQL for number field"""
        allow_decimals = settings.get("allowDecimals", True) if settings else True

        if allow_decimals:
            sql = f'"{field_name}" DECIMAL'
        else:
            sql = f'"{field_name}" INTEGER'

        if is_required:
            sql += ' NOT NULL'

        return sql
