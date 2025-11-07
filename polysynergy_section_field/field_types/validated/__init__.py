"""Validated text field types"""

from .email import EmailField
from .url import UrlField
from .phone import PhoneField
from .slug import SlugField

__all__ = ['EmailField', 'UrlField', 'PhoneField', 'SlugField']
