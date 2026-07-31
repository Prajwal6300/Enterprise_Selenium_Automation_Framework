"""Database Validation Test Suite.

Demonstrates end-to-end data integrity validation comparing UI product & user data against DB tables.
"""

from __future__ import annotations

import pytest
from src.utils.db_utility import DBUtility
from src.utils.logger import get_logger

logger = get_logger("TestDBValidation")


@pytest.mark.db
class TestDatabaseValidation:
    """Test suite for verifying database records against UI values."""

    def test_ui_product_price_matches_database_record(self):
        """Verify product price extracted from UI matches the catalog table record in DB."""
        logger.info("Executing test_ui_product_price_matches_database_record")

        # Mock/Extracted UI Data
        ui_product = {
            "name": "Sauce Labs Backpack",
            "price": "$29.99",
            "sku": "SAUCE-BACKPACK-01"
        }

        # Mock DB Query Result (SQLite fallback for isolated test execution)
        db_utility = DBUtility(db_type="sqlite", database=":memory:")
        db_utility.execute_update(
            "CREATE TABLE products (name TEXT, price TEXT, sku TEXT);"
        )
        db_utility.execute_update(
            "INSERT INTO products VALUES ('Sauce Labs Backpack', '$29.99', 'SAUCE-BACKPACK-01');"
        )

        db_rows = db_utility.execute_query(
            "SELECT name, price, sku FROM products WHERE sku = :sku",
            {"sku": "SAUCE-BACKPACK-01"}
        )

        assert len(db_rows) == 1, "Exactly one product record should be returned from DB"
        db_product = db_rows[0]

        # Perform UI vs DB verification
        DBUtility.verify_ui_against_db(
            ui_data=ui_product,
            db_data=db_product,
            keys_to_compare=["name", "price", "sku"]
        )
        logger.info("UI vs DB product price verification passed successfully")
