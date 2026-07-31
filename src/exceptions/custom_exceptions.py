"""Custom Exceptions for the Automation Framework.

Provides domain-specific exception types to distinguish framework infrastructure failures
from test assertion failures.
"""

from __future__ import annotations


class AutomationFrameworkError(Exception):
    """Base exception for all errors raised by the automation framework."""
    pass


class ElementNotFoundException(AutomationFrameworkError):
    """Raised when a UI element cannot be located within specified timeout."""
    pass


class ConfigurationException(AutomationFrameworkError):
    """Raised when configuration properties are missing or invalid."""
    pass


class DataReadException(AutomationFrameworkError):
    """Raised when test data files cannot be parsed or read."""
    pass


class APIClientException(AutomationFrameworkError):
    """Raised when REST API calls fail or return unexpected exceptions."""
    pass


class DatabaseException(AutomationFrameworkError):
    """Raised when database connection or SQL query execution fails."""
    pass
