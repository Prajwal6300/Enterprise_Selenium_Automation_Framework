"""Random Test Data Generator Utility.

Generates realistic dynamic customer profile details (names, addresses, postal codes, emails)
using Python random utilities and fallback generators.
"""

from __future__ import annotations

import random
import string
from typing import Dict


class TestDataGenerator:
    """Random test data generation helper."""

    @staticmethod
    def get_random_string(length: int = 8) -> str:
        """Generate random alphanumeric string of given length."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def get_random_email(domain: str = "example.com") -> str:
        """Generate random user email address."""
        username = TestDataGenerator.get_random_string(10).lower()
        return f"testuser_{username}@{domain}"

    @staticmethod
    def get_random_customer_info() -> Dict[str, str]:
        """Generate full synthetic checkout customer info."""
        first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Sam"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        
        return {
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "postal_code": str(random.randint(10000, 99999)),
            "email": TestDataGenerator.get_random_email(),
        }
