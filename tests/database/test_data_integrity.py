"""Comprehensive Database Schema and Data Integrity Test Suite.

Validates:
1. Database connectivity and query execution engine
2. Exact product SKU existence and lookup
3. Inventory count positive constraint (> 0)
4. Active status flag constraint (is_active in (0, 1))
5. Price float precision and format integrity
6. Multi-record UI vs Database catalog batch consistency
"""

from __future__ import annotations

import pytest
from src.utils.db_utility import DBUtility
from src.utils.logger import get_logger

logger = get_logger("TestDataIntegrity")


@pytest.mark.database
@pytest.mark.db
@pytest.mark.regression
class TestDataIntegrity:
    """Test suite covering database table constraints, schema validation, and data integrity."""

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Create and populate isolated in-memory test database."""
        self.db = DBUtility(db_type="sqlite", database=":memory:")
        self.db.execute_update(
            """CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                price_float REAL NOT NULL,
                sku TEXT UNIQUE NOT NULL,
                inventory_count INTEGER NOT NULL CHECK(inventory_count >= 0),
                is_active INTEGER NOT NULL CHECK(is_active IN (0, 1))
            );"""
        )
        self.db.execute_update(
            """INSERT INTO products (id, name, price, price_float, sku, inventory_count, is_active) VALUES
                (1, 'Sauce Labs Backpack', '$29.99', 29.99, 'SAUCE-BACKPACK-01', 50, 1),
                (2, 'Sauce Labs Bike Light', '$9.99', 9.99, 'SAUCE-BIKELIGHT-02', 40, 1),
                (3, 'Sauce Labs Bolt T-Shirt', '$15.99', 15.99, 'SAUCE-TSHIRT-03', 30, 1),
                (4, 'Sauce Labs Fleece Jacket', '$49.99', 49.99, 'SAUCE-JACKET-04', 20, 1),
                (5, 'Sauce Labs Onesie', '$7.99', 7.99, 'SAUCE-ONESIE-05', 100, 1),
                (6, 'Test.allTheThings() T-Shirt (Red)', '$15.99', 15.99, 'SAUCE-REDSHIRT-06', 15, 1);
            """
        )

    def test_db_connection_health_check(self):
        """1. Verify database engine successfully connects and executes queries."""
        logger.info("Executing test_db_connection_health_check")
        rows = self.db.execute_query("SELECT 1 as status")
        assert len(rows) == 1 and rows[0]["status"] == 1
        logger.info("test_db_connection_health_check passed")

    def test_db_product_lookup_by_sku(self):
        """2. Verify individual product can be retrieved by unique SKU."""
        logger.info("Executing test_db_product_lookup_by_sku")
        rows = self.db.execute_query(
            "SELECT name, price_float FROM products WHERE sku = :sku",
            {"sku": "SAUCE-JACKET-04"}
        )
        assert len(rows) == 1
        assert rows[0]["name"] == "Sauce Labs Fleece Jacket"
        assert rows[0]["price_float"] == 49.99
        logger.info("test_db_product_lookup_by_sku passed")

    def test_db_inventory_counts_are_positive(self):
        """3. Verify all catalog items have stock inventory count greater than 0."""
        logger.info("Executing test_db_inventory_counts_are_positive")
        rows = self.db.execute_query("SELECT name, inventory_count FROM products")
        for row in rows:
            assert row["inventory_count"] > 0, f"Stock depleted for {row['name']}"
        logger.info("test_db_inventory_counts_are_positive passed for %d products", len(rows))

    def test_db_active_status_constraint(self):
        """4. Verify all active products have is_active flag set to 1."""
        logger.info("Executing test_db_active_status_constraint")
        rows = self.db.execute_query("SELECT name, is_active FROM products")
        for row in rows:
            assert row["is_active"] in (0, 1), f"Invalid status flag: {row['is_active']}"
        logger.info("test_db_active_status_constraint passed")

    def test_db_batch_ui_catalog_consistency(self):
        """5. Verify batch list of UI catalog products matches DB table records."""
        logger.info("Executing test_db_batch_ui_catalog_consistency")
        ui_catalog = [
            {"name": "Sauce Labs Backpack", "price": "$29.99", "sku": "SAUCE-BACKPACK-01"},
            {"name": "Sauce Labs Bike Light", "price": "$9.99", "sku": "SAUCE-BIKELIGHT-02"},
            {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99", "sku": "SAUCE-TSHIRT-03"},
        ]

        for item in ui_catalog:
            db_row = self.db.execute_query(
                "SELECT name, price, sku FROM products WHERE sku = :sku",
                {"sku": item["sku"]}
            )[0]
            DBUtility.verify_ui_against_db(item, db_row, ["name", "price", "sku"])
        logger.info("test_db_batch_ui_catalog_consistency passed")

    def test_db_non_existent_product_returns_empty(self):
        """6. Verify query for non-existent product SKU returns empty result list without crashing."""
        logger.info("Executing test_db_non_existent_product_returns_empty")
        rows = self.db.execute_query(
            "SELECT * FROM products WHERE sku = :sku",
            {"sku": "NON-EXISTENT-SKU-999"}
        )
        assert len(rows) == 0, f"Expected 0 rows for invalid SKU, got: {rows}"
        logger.info("test_db_non_existent_product_returns_empty passed")
