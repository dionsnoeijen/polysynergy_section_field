"""Image field type"""

from polysynergy_section_field.section_field_runner.base_field_type import FieldType
from polysynergy_section_field.section_field_runner.field_type_decorator import field_type


@field_type(category="media", icon="image.svg")
class ImageField(FieldType):
    """Image upload field - stores path/URL to image"""

    handle = "image"
    label = "Image"
    postgres_type = "VARCHAR(500)"

    @property
    def settings_schema(self):
        return {
            "type": "object",
            "properties": {
                "maxFileSize": {
                    "type": "integer",
                    "default": 5242880,
                    "title": "Max File Size (bytes)",
                    "description": "Maximum file size in bytes (default: 5MB)"
                },
                "allowedFormats": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["jpg", "jpeg", "png", "gif", "webp", "svg"]
                    },
                    "default": ["jpg", "jpeg", "png", "gif", "webp"],
                    "title": "Allowed Formats"
                },
                "maxWidth": {
                    "type": "integer",
                    "title": "Max Width (px)",
                    "description": "Maximum image width in pixels"
                },
                "maxHeight": {
                    "type": "integer",
                    "title": "Max Height (px)",
                    "description": "Maximum image height in pixels"
                },
                "generateThumbnails": {
                    "type": "boolean",
                    "default": True,
                    "title": "Generate Thumbnails",
                    "description": "Auto-generate thumbnail versions"
                },
                "thumbnailSizes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "width": {"type": "integer"},
                            "height": {"type": "integer"}
                        }
                    },
                    "default": [
                        {"name": "thumb", "width": 150, "height": 150},
                        {"name": "medium", "width": 300, "height": 300}
                    ],
                    "title": "Thumbnail Sizes"
                }
            }
        }

    def get_table_cell_config(self, value, settings, field_config):
        """How to display in table view"""
        return {
            "component": "ImageCell",
            "props": {
                "src": value,
                "size": "small"
            }
        }

    def get_form_input_config(self, settings, field_config):
        """How to render in form"""
        return {
            "component": "ImageUpload",
            "props": {
                "maxFileSize": settings.get("maxFileSize", 5242880) if settings else 5242880,
                "allowedFormats": settings.get("allowedFormats", ["jpg", "jpeg", "png", "gif", "webp"]) if settings else ["jpg", "jpeg", "png", "gif", "webp"],
                "maxWidth": settings.get("maxWidth") if settings else None,
                "maxHeight": settings.get("maxHeight") if settings else None,
                "generateThumbnails": settings.get("generateThumbnails", True) if settings else True,
                "thumbnailSizes": settings.get("thumbnailSizes") if settings else None
            }
        }
