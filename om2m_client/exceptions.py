"""
Defines custom exceptions for OM2M client errors.
"""

class OM2MClientError(Exception):
    """Base exception for OM2M client errors."""

class OM2MRequestError(OM2MClientError):
    """Raised when an HTTP request fails or returns an unexpected status code."""

class OM2MValidationError(OM2MClientError):
    """Raised when invalid parameters or resource representations are provided."""
