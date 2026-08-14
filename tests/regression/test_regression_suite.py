"""Enterprise Regression Test Suite.

End-to-end integration and regression sanity checks ensuring all subsystems
(UI Auth, Catalog, Cart, Checkout, Session, REST API, Database) operate cohesively.
"""

from __future__ import annotations

import pytest
from src.base.base_test import BaseTest
from src.services.user_api import UserAPIService
from src.services.api_client import APIClient
from src.utils.db_utility import DBUtility
from src.utils.logger import get_logger

logger = get_logger("TestRegressionSuite")


@pytest.mark.regression
class TestRegressionSuite(BaseTest):
    """Broad regression test suite verifying cross-module system stability."""

    @pytest.mark.ui
    def test_regression_ui_auth_and_catalog_navigation(self, driver):
        """1. Regression check for user authentication and catalog discovery."""
        logger.info("Executing test_regression_ui_auth_and_catalog_navigation")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded()
        assert self.home_page.get_product_count() == 6

        self.home_page.sort_products("lohi")
        prices = self.home_page.get_product_prices()
        assert prices[0] == 7.99 and prices[-1] == 49.99
        logger.info("test_regression_ui_auth_and_catalog_navigation passed")

    @pytest.mark.ui
    def test_regression_ui_cart_and_checkout_integrity(self, driver):
        """2. Regression check for cart item management, overview calculations, and order confirmation."""
        logger.info("Executing test_regression_ui_cart_and_checkout_integrity")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        assert self.home_page.get_cart_count() == 2

        self.home_page.go_to_cart()
        assert self.cart_page.is_loaded()
        assert self.cart_page.calculate_subtotal() == round(29.99 + 9.99, 2)

        self.cart_page.checkout()
        self.checkout_page.complete_order("Regression", "Tester", "10001")

        assert self.checkout_page.verify_order()
        logger.info("test_regression_ui_cart_and_checkout_integrity passed")

    @pytest.mark.ui
    def test_regression_ui_session_termination_security(self, driver):
        """3. Regression check ensuring session is destroyed after logout and protected pages redirect."""
        logger.info("Executing test_regression_ui_session_termination_security")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded()

        self.home_page.logout()
        assert self.login_page.is_loaded()

        base_url = self.config.get_base_url().rstrip("/")
        driver.get(f"{base_url}/inventory.html")
        assert self.login_page.is_loaded()
        logger.info("test_regression_ui_session_termination_security passed")

    @pytest.mark.api
    def test_regression_api_service_lifecycle(self):
        """4. Regression check for REST API GET, POST, PUT, DELETE operations."""
        logger.info("Executing test_regression_api_service_lifecycle")
        api = UserAPIService()

        # 1. GET
        get_res = api.get_user_by_id(post_id=1)
        APIClient.validate_status_code(get_res, 200)

        # 2. POST
        post_res = api.create_user(title="Regression Test", body="Regression Payload", user_id=1)
        APIClient.validate_status_code(post_res, 201)

        # 3. PUT
        put_res = api.update_user(post_id=1, title="Updated Regression", body="Updated Payload", user_id=1)
        APIClient.validate_status_code(put_res, 200)

        # 4. DELETE
        del_res = api.delete_user(post_id=1)
        APIClient.validate_status_code(del_res, 200)
        logger.info("test_regression_api_service_lifecycle passed")

    @pytest.mark.database
    @pytest.mark.db
    def test_regression_database_catalog_consistency(self):
        """5. Regression check for DB schema constraints and catalog verification."""
        logger.info("Executing test_regression_database_catalog_consistency")
        db = DBUtility(db_type="sqlite", database=":memory:")
        db.execute_update(
            """CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                price_float REAL NOT NULL,
                sku TEXT UNIQUE NOT NULL
            );"""
        )
        db.execute_update(
            """INSERT INTO products (id, name, price, price_float, sku) VALUES
                (1, 'Sauce Labs Backpack', '$29.99', 29.99, 'SAUCE-BACKPACK-01');
            """
        )

        rows = db.execute_query("SELECT name, price FROM products WHERE sku = 'SAUCE-BACKPACK-01'")
        assert len(rows) == 1
        assert rows[0]["name"] == "Sauce Labs Backpack"
        assert rows[0]["price"] == "$29.99"
        logger.info("test_regression_database_catalog_consistency passed")
