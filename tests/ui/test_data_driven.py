"""Multi-Format Data-Driven UI Test Suite.

Demonstrates data-driven testing using:
- Excel (.xlsx) via ExcelReader / DataProvider
- JSON (.json) via DataProvider
- CSV (.csv) via DataProvider
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.data_provider import DataProvider
from src.utils.logger import get_logger

logger = get_logger("TestDataDriven")

# Load datasets for parametrization
LOGIN_JSON_PATH = Path("testdata/json/login_data.json")
CHECKOUT_JSON_PATH = Path("testdata/json/checkout_data.json")
USERS_CSV_PATH = Path("testdata/csv/users.csv")
SEARCH_JSON_PATH = Path("testdata/json/search_data.json")

VALID_USERS_JSON = DataProvider.load_data(LOGIN_JSON_PATH, key_or_sheet="valid_users")
INVALID_USERS_JSON = DataProvider.load_data(LOGIN_JSON_PATH, key_or_sheet="invalid_users")
CHECKOUT_CUSTOMERS_JSON = DataProvider.load_data(CHECKOUT_JSON_PATH, key_or_sheet="valid_customers")
SEARCH_SCENARIOS_JSON = DataProvider.load_data(SEARCH_JSON_PATH, key_or_sheet="search_scenarios")
CSV_USERS = DataProvider.load_data(USERS_CSV_PATH)


@pytest.mark.ui
@pytest.mark.regression
class TestDataDrivenUI(BaseTest):
    """Test suite demonstrating data-driven UI execution across multi-format datasets."""

    @pytest.mark.parametrize("user_data", VALID_USERS_JSON)
    def test_ddt_valid_login_json(self, driver, user_data):
        """Data-driven test for valid login credentials loaded from JSON."""
        logger.info("Executing test_ddt_valid_login_json for user '%s'", user_data["username"])
        self.init_pages(driver)
        
        self.login_page.login(user_data["username"], user_data["password"])
        assert self.home_page.is_loaded(), f"User {user_data['username']} should log in successfully"
        assert "inventory.html" in driver.current_url

    @pytest.mark.parametrize("user_data", INVALID_USERS_JSON)
    def test_ddt_invalid_login_json(self, driver, user_data):
        """Data-driven test for invalid login attempts loaded from JSON."""
        logger.info("Executing test_ddt_invalid_login_json for user '%s'", user_data["username"])
        self.init_pages(driver)
        
        self.login_page.login(user_data["username"], user_data["password"])
        error_msg = self.login_page.get_error_message()
        assert user_data["expected_error"] in error_msg, (
            f"Expected error '{user_data['expected_error']}', received '{error_msg}'"
        )

    @pytest.mark.parametrize("user_data", [u for u in CSV_USERS if u.get("expected_result") == "login_success"])
    def test_ddt_login_csv(self, driver, user_data):
        """Data-driven test for authentication loaded from CSV."""
        logger.info("Executing test_ddt_login_csv for user '%s'", user_data["username"])
        self.init_pages(driver)
        
        self.login_page.login(user_data["username"], user_data["password"])
        assert self.home_page.is_loaded(), f"CSV User {user_data['username']} should log in successfully"

    @pytest.mark.parametrize("customer", CHECKOUT_CUSTOMERS_JSON)
    def test_ddt_checkout_completion_json(self, driver, customer):
        """Data-driven test for checkout completion loaded from JSON."""
        logger.info("Executing test_ddt_checkout_completion_json for '%s %s'", customer["first_name"], customer["last_name"])
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.complete_order(customer["first_name"], customer["last_name"], customer["postal_code"])
        assert self.checkout_page.is_complete_page_loaded(), "Order must be completed successfully"
        assert self.checkout_page.get_complete_message() == "Thank you for your order!"

    @pytest.mark.parametrize("search_case", SEARCH_SCENARIOS_JSON)
    def test_ddt_search_and_discovery_json(self, driver, search_case):
        """Data-driven test for catalog filtering scenarios loaded from JSON."""
        logger.info("Executing test_ddt_search_and_discovery_json with query '%s'", search_case["query"])
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        matches = self.home_page.search_product(search_case["query"])
        
        assert len(matches) == search_case["expected_match_count"], (
            f"Query '{search_case['query']}': Expected {search_case['expected_match_count']} matches, found {len(matches)}"
        )
        if search_case["expected_product_name"]:
            assert search_case["expected_product_name"] in matches, (
                f"Expected '{search_case['expected_product_name']}' in search results: {matches}"
            )
