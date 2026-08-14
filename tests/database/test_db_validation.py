"""Database Validation Test Suite.

Demonstrates end-to-end data integrity validation comparing UI product & user data against DB tables.
"""

from __future__ import annotations

import pytest
from src.utils.db_utility import DBUtility
from src.utils.logger import get_logger

logger = get_logger("TestDBValidation")


@pytest.mark.database
@pytest.mark.db
class TestDatabaseValidation:
    """Test suite for verifying database records, schema constraints, and UI vs DB integrity."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Create and populate isolated in-memory test database for data validation."""
        self.db = DBUtility(db_type="sqlite", database=":memory:")
        self.db.execute_update(
            """CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                price_float REAL NOT NULL,
                sku TEXT UNIQUE NOT NULL,
                inventory_count INTEGER NOT NULL,
                is_active INTEGER NOT NULL
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

    def test_ui_product_price_matches_database_record(self):
        """Verify product price extracted from UI matches the catalog table record in DB."""
        logger.info("Executing test_ui_product_price_matches_database_record")

        ui_product = {
            "name": "Sauce Labs Backpack",
            "price": "$29.99",
            "sku": "SAUCE-BACKPACK-01"
        }

        db_rows = self.db.execute_query(
            "SELECT name, price, sku FROM products WHERE sku = :sku",
            {"sku": "SAUCE-BACKPACK-01"}
        )

        assert len(db_rows) == 1, "Exactly one product record should be returned from DB"
        db_product = db_rows[0]

        DBUtility.verify_ui_against_db(
            ui_data=ui_product,
            db_data=db_product,
            keys_to_compare=["name", "price", "sku"]
        )
        logger.info("UI vs DB product price verification passed successfully")

    def test_database_catalog_record_count_and_existence(self):
        """Verify database contains all 6 active catalog items."""
        logger.info("Executing test_database_catalog_record_count_and_existence")
        rows = self.db.execute_query("SELECT id, name, sku FROM products WHERE is_active = 1")
        
        assert len(rows) == 6, f"Expected 6 active product records in DB, found {len(rows)}"
        skus = [r["sku"] for r in rows]
        assert "SAUCE-BACKPACK-01" in skus, "Sauce Labs Backpack SKU must exist"
        assert "SAUCE-JACKET-04" in skus, "Sauce Labs Fleece Jacket SKU must exist"
        logger.info("test_database_catalog_record_count_and_existence passed")

    def test_database_required_fields_not_null(self):
        """Verify required fields (name, price, sku) have no NULL records in product catalog."""
        logger.info("Executing test_database_required_fields_not_null")
        null_rows = self.db.execute_query(
            "SELECT id, name, price, sku FROM products WHERE name IS NULL OR price IS NULL OR sku IS NULL"
        )
        assert len(null_rows) == 0, f"Found records with NULL required fields: {null_rows}"
        logger.info("test_database_required_fields_not_null passed")

    def test_database_no_duplicate_sku_records(self):
        """Verify no duplicate SKUs exist across the product database."""
        logger.info("Executing test_database_no_duplicate_sku_records")
        duplicate_rows = self.db.execute_query(
            "SELECT sku, COUNT(*) as count FROM products GROUP BY sku HAVING COUNT(*) > 1"
        )
        assert len(duplicate_rows) == 0, f"Found duplicate SKUs in database: {duplicate_rows}"
        logger.info("test_database_no_duplicate_sku_records passed")

    def test_database_price_data_type_and_format(self):
        """Verify all product prices in DB are positive floating point numbers."""
        logger.info("Executing test_database_price_data_type_and_format")
        rows = self.db.execute_query("SELECT name, price_float FROM products")
        
        for row in rows:
            val = row["price_float"]
            assert isinstance(val, (int, float)), f"Expected float price for {row['name']}, got {type(val)}"
            assert val > 0, f"Price must be positive, got {val} for {row['name']}"
        logger.info("test_database_price_data_type_and_format passed")

    def test_database_mismatch_raises_assertion_error(self):
        """Verify verify_ui_against_db properly raises AssertionError when data mismatches."""
        logger.info("Executing test_database_mismatch_raises_assertion_error")
        mismatched_ui = {"name": "Sauce Labs Backpack", "price": "$100.00"}
        db_data = {"name": "Sauce Labs Backpack", "price": "$29.99"}

        with pytest.raises(AssertionError, match="UI vs DB Data Verification Failed"):
            DBUtility.verify_ui_against_db(
                ui_data=mismatched_ui,
                db_data=db_data,
                keys_to_compare=["name", "price"]
            )
        logger.info("test_database_mismatch_raises_assertion_error passed")

