"""Decorator for field type classes"""

from typing import Optional


def field_type(*, category: str = "general", icon: Optional[str] = None):
    """
    Decorator for field type classes.

    Adds metadata to field type classes for registration and UI display.

    Args:
        category: Category for grouping in UI (e.g., 'basic', 'number', 'relational')
        icon: Icon filename for UI display (e.g., 'text.svg')

    Example:
        >>> @field_type(category="basic", icon="text.svg")
        ... class TextField(FieldType):
        ...     handle = "text"
        ...     label = "Plain Text"
        ...     postgres_type = "TEXT"
        ...
        ...     def validate(self, value, settings=None):
        ...         if not isinstance(value, str):
        ...             return (False, "Value must be a string")
        ...         return (True, None)
    """
    def decorator(cls):
        # Add metadata as class attributes
        cls._field_type_category = category
        cls._field_type_icon = icon

        # Override category and icon properties if decorator provided values
        if category:
            cls.category = property(lambda self: category)
        if icon:
            cls.icon = property(lambda self: icon)

        return cls

    return decorator
