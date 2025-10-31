"""Base class for all field types"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class FieldType(ABC):
    """
    Base class for all field types in the section field system.

    Each field type defines:
    - How data is validated
    - How it's stored in PostgreSQL
    - How it's rendered in UI
    - What settings are available
    """

    @property
    @abstractmethod
    def handle(self) -> str:
        """
        Unique identifier for this field type.
        Must be lowercase with underscores only.

        Examples: 'text', 'number', 'relation'
        """
        pass

    @property
    @abstractmethod
    def label(self) -> str:
        """
        Human-readable label for UI.

        Examples: 'Plain Text', 'Number', 'Relation'
        """
        pass

    @property
    @abstractmethod
    def postgres_type(self) -> str:
        """
        PostgreSQL column type for this field.

        Examples: 'TEXT', 'INTEGER', 'TIMESTAMP WITH TIME ZONE', 'UUID'
        """
        pass

    @property
    def ui_component(self) -> str:
        """
        Frontend UI component identifier.
        Used by frontend to determine which component to render.

        Examples: 'text-input', 'number-input', 'date-picker', 'relation-select'
        """
        return "text-input"  # default fallback

    @property
    def category(self) -> str:
        """
        Field type category for UI grouping.

        Examples: 'basic', 'number', 'date', 'relational', 'advanced'
        """
        return "general"

    @property
    def icon(self) -> Optional[str]:
        """
        Icon filename for UI.

        Example: 'text.svg', 'number.svg'
        """
        return None

    @property
    def settings_schema(self) -> Optional[Dict]:
        """
        JSON Schema defining field-specific settings.

        Example for text field:
        {
            "type": "object",
            "properties": {
                "maxLength": {"type": "integer", "minimum": 1},
                "minLength": {"type": "integer", "minimum": 0},
                "pattern": {"type": "string"}
            }
        }

        Returns:
            JSON Schema dict or None if no settings needed
        """
        return None

    def validate(self, value: Any, settings: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate a value for this field type.

        Args:
            value: The value to validate
            settings: Field-specific settings from settings_schema

        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if valid
            - (False, "Error message") if invalid

        Example:
            >>> field = TextField()
            >>> field.validate("hello", {"maxLength": 10})
            (True, None)
            >>> field.validate("hello world!", {"maxLength": 10})
            (False, "Text too long (maximum 10 characters)")
        """
        return (True, None)

    def serialize(self, value: Any) -> Any:
        """
        Convert Python value to database-storable format.
        Called before INSERT/UPDATE operations.

        Args:
            value: Python value to serialize

        Returns:
            Database-storable value

        Example:
            >>> from datetime import datetime
            >>> field = DateTimeField()
            >>> field.serialize(datetime.now())
            '2025-10-31T10:30:00Z'
        """
        return value

    def deserialize(self, value: Any) -> Any:
        """
        Convert database value to Python format.
        Called after SELECT operations.

        Args:
            value: Database value to deserialize

        Returns:
            Python value

        Example:
            >>> field = DateTimeField()
            >>> field.deserialize('2025-10-31T10:30:00Z')
            datetime(2025, 10, 31, 10, 30, 0)
        """
        return value

    def get_migration_sql(
        self,
        field_name: str,
        settings: Optional[Dict] = None,
        is_required: bool = False
    ) -> str:
        """
        Generate SQL column definition for migrations.

        Args:
            field_name: Column name for the field
            settings: Field-specific settings
            is_required: Whether field is required (NOT NULL)

        Returns:
            SQL column definition (without trailing comma)

        Example:
            >>> field = TextField()
            >>> field.get_migration_sql("company_name", {"maxLength": 200}, True)
            '"company_name" VARCHAR(200) NOT NULL'
        """
        sql = f'"{field_name}" {self.postgres_type}'

        if is_required:
            sql += ' NOT NULL'

        return sql

    def get_index_sql(
        self,
        table_name: str,
        field_name: str,
        settings: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Generate optional index SQL for this field.

        Override this method if your field type benefits from indexing.

        Args:
            table_name: Name of the table
            field_name: Name of the field/column
            settings: Field-specific settings

        Returns:
            SQL CREATE INDEX statement or None

        Example:
            >>> field = RelationField()
            >>> field.get_index_sql("research_companies", "primary_contact")
            'CREATE INDEX idx_research_companies_primary_contact ON custom.research_companies("primary_contact");'
        """
        return None

    def get_default_value(self, settings: Optional[Dict] = None) -> Optional[Any]:
        """
        Get default value for this field type.

        Args:
            settings: Field-specific settings

        Returns:
            Default value or None
        """
        return None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(handle='{self.handle}')>"
