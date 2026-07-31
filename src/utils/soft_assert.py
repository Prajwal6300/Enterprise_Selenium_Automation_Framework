"""Enterprise Soft Assertion Utility.

Allows multiple assertions to execute within a test step without failing immediately.
Collects all failure messages and raises a consolidated AssertionError upon calling assert_all().
"""

from __future__ import annotations

from typing import List
from src.utils.logger import get_logger

logger = get_logger("SoftAssert")


class SoftAssert:
    """Soft assertion collector class."""

    def __init__(self) -> None:
        """Initialize empty failure list."""
        self._errors: List[str] = []

    def check(self, condition: bool, message: str) -> None:
        """Evaluate condition softly. Collect error message if condition evaluates to False."""
        if not condition:
            logger.error("Soft Assertion Failed: %s", message)
            self._errors.append(message)
        else:
            logger.info("Soft Assertion Passed: %s", message)

    def assert_all(self) -> None:
        """Assert that no soft failures occurred during test execution."""
        if self._errors:
            error_msg = f"Soft Assertions Failed ({len(self._errors)} errors):\n" + "\n".join(
                f" - {err}" for err in self._errors
            )
            self._errors = []  # Clear for subsequent calls
            raise AssertionError(error_msg)
        logger.info("All Soft Assertions PASSED successfully.")
