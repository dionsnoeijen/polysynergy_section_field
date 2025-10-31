"""Common validation functions for field types"""

import re
import uuid as uuid_lib
from typing import Any, Optional, Tuple


def validate_string_length(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate string length constraints.

    Args:
        value: String to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(value, str):
        return (False, "Value must be a string")

    length = len(value)

    if min_length is not None and length < min_length:
        return (False, f"Text too short (minimum {min_length} characters)")

    if max_length is not None and length > max_length:
        return (False, f"Text too long (maximum {max_length} characters)")

    return (True, None)


def validate_number_range(
    value: Any,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allow_float: bool = True
) -> Tuple[bool, Optional[str]]:
    """
    Validate number range constraints.

    Args:
        value: Number to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_float: Whether to allow float values

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return (False, "Value must be a number")

    if not allow_float and isinstance(value, float):
        return (False, "Value must be an integer")

    if min_value is not None and value < min_value:
        return (False, f"Value too small (minimum {min_value})")

    if max_value is not None and value > max_value:
        return (False, f"Value too large (maximum {max_value})")

    return (True, None)


def validate_regex_pattern(value: str, pattern: str) -> Tuple[bool, Optional[str]]:
    """
    Validate string against regex pattern.

    Args:
        value: String to validate
        pattern: Regex pattern

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(value, str):
        return (False, "Value must be a string")

    try:
        if not re.match(pattern, value):
            return (False, "Value does not match required pattern")
    except re.error as e:
        return (False, f"Invalid regex pattern: {e}")

    return (True, None)


def validate_email(value: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format.

    Args:
        value: Email address to validate

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(value, str):
        return (False, "Value must be a string")

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, value):
        return (False, "Invalid email address format")

    return (True, None)


def validate_url(value: str, require_https: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate URL format.

    Args:
        value: URL to validate
        require_https: Whether to require HTTPS

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(value, str):
        return (False, "Value must be a string")

    # URL regex pattern
    if require_https:
        pattern = r'^https://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    else:
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    if not re.match(pattern, value):
        error_msg = "Invalid URL format"
        if require_https:
            error_msg += " (HTTPS required)"
        return (False, error_msg)

    return (True, None)


def validate_uuid(value: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate UUID format.

    Args:
        value: UUID to validate (str or uuid.UUID)

    Returns:
        (is_valid, error_message)
    """
    try:
        if isinstance(value, str):
            uuid_lib.UUID(value)
        elif not isinstance(value, uuid_lib.UUID):
            return (False, "Value must be a valid UUID")
    except ValueError:
        return (False, "Invalid UUID format")

    return (True, None)
