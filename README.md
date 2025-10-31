# PolySynergy Section Field

Dynamic content field types system for PolySynergy orchestrator.

## Overview

This package provides a plugin-based field type system for creating dynamic content sections, similar to Craft CMS's content modeling.

## Features

- **Field Types**: Extensible field type system with validation and UI configuration
- **Auto-Discovery**: Field types are automatically registered (like nodes)
- **Database Integration**: Field types map to PostgreSQL column types
- **Validation**: Built-in validation with custom rules
- **UI Components**: Each field type defines its UI rendering component

## Architecture

See the main [CONTENT_SYSTEM_ARCHITECTURE.md](../CONTENT_SYSTEM_ARCHITECTURE.md) for complete documentation.

## Basic Field Types

- **text**: Plain text field
- **textarea**: Multi-line text
- **number**: Integer or decimal numbers
- **boolean**: True/false toggle
- **date**: Date picker
- **datetime**: Date and time picker
- **select**: Dropdown selection
- **relation**: Relations to other sections

## Usage

```python
from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type

@field_type(category="basic", icon="text.svg")
class TextField(FieldType):
    handle = "text"
    label = "Plain Text"
    postgres_type = "TEXT"
    ui_component = "text-input"

    def validate(self, value, settings=None):
        if not isinstance(value, str):
            return (False, "Value must be a string")
        return (True, None)
```

## Development

Install dependencies:
```bash
poetry install
```

Run tests:
```bash
poetry run pytest
```

## License

Proprietary - Part of PolySynergy orchestrator system
