"""PolySynergy Section Field - Dynamic content field types"""

from polysynergy_section_field.field_types.text import TextField, TextAreaField
from polysynergy_section_field.field_types.number import NumberField
from polysynergy_section_field.field_types.boolean import BooleanField

# Registered field types for auto-discovery
registered_field_types = [
    TextField,
    TextAreaField,
    NumberField,
    BooleanField,
]

__version__ = "0.1.0"
__all__ = [
    "TextField",
    "TextAreaField",
    "NumberField",
    "BooleanField",
    "registered_field_types"
]
