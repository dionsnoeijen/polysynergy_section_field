"""File field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="media", icon="file.svg")
class FileField(FieldType):
    """File upload field - stores path/URL to file"""

    handle = "file"
    label = "File"
    postgres_type = "VARCHAR(500)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "maxFileSize": {
                    "type": "integer",
                    "default": 10485760,
                    "title": "Max File Size (bytes)",
                    "description": "Maximum file size in bytes (default: 10MB)"
                },
                "allowedExtensions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "default": ["pdf", "doc", "docx", "xls", "xlsx", "txt", "zip"],
                    "title": "Allowed Extensions",
                    "description": "Allowed file extensions (without dot)"
                },
                "allowedMimeTypes": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "title": "Allowed MIME Types",
                    "description": "Additional MIME type restrictions"
                },
                "multipleFiles": {
                    "type": "boolean",
                    "default": False,
                    "title": "Allow Multiple Files",
                    "description": "Allow uploading multiple files (stores as JSON array)"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "FileCell",
            "props": {
                "value": value,
                "showIcon": True
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "FileUpload",
            "props": {
                "maxFileSize": settings.get("maxFileSize", 10485760) if settings else 10485760,
                "allowedExtensions": settings.get("allowedExtensions", ["pdf", "doc", "docx", "xls", "xlsx", "txt", "zip"]) if settings else ["pdf", "doc", "docx", "xls", "xlsx", "txt", "zip"],
                "allowedMimeTypes": settings.get("allowedMimeTypes") if settings else None,
                "multipleFiles": settings.get("multipleFiles", False) if settings else False
            }
        }
