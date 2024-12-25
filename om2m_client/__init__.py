"""
om2m_client package

A Python client library for interacting with an OM2M-compatible CSE via RESTful APIs.
Follows oneM2M standards and emphasizes SOLID principles.

Modules:
- client: Main OM2MClient class for interacting with the CSE.
- models: Resource models for AE, Container, ContentInstance, Subscription, etc.
- enums: Enumerations for resource types and constants.
- exceptions: Custom exception classes for error handling.

Usage:
    from om2m_client import OM2MClient, AE, Container, ContentInstance, Subscription
    client = OM2MClient(
        base_url="http://127.0.0.1:8080",
        cse_id="in-cse",
        cse_name="in-name",
        username="admin",
        password="admin"
    )
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "Eclipse Public License 2.0"

# Import core components
from .client import OM2MClient
from .models import AE, Container, ContentInstance, Subscription
from .enums import ResourceType
from .exceptions import OM2MClientError, OM2MRequestError, OM2MValidationError
