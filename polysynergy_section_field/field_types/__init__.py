"""Field types for section field system"""

# Import all field type modules to trigger @field_type decorator registration
from .text import TextField, TextAreaField
from .number import NumberField
from .boolean import BooleanField
from .relation import RelationManyToOneField, RelationOneToManyField, RelationManyToManyField
from .datetime import DateField, TimeField, DateTimeField
from .selection import SelectField, MultiSelectField
from .validated import EmailField, UrlField, PhoneField, SlugField
from .media import ImageField, FileField
from .special import ColorField, JsonField, CurrencyField, PercentageField

__all__ = [
    # Basic types
    "TextField",
    "TextAreaField",
    "NumberField",
    "BooleanField",
    # Relations
    "RelationManyToOneField",
    "RelationOneToManyField",
    "RelationManyToManyField",
    # Date/Time
    "DateField",
    "TimeField",
    "DateTimeField",
    # Selection
    "SelectField",
    "MultiSelectField",
    # Validated
    "EmailField",
    "UrlField",
    "PhoneField",
    "SlugField",
    # Media
    "ImageField",
    "FileField",
    # Special
    "ColorField",
    "JsonField",
    "CurrencyField",
    "PercentageField"
]
