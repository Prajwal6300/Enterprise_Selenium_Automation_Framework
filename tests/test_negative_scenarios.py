"""Dedicated Negative Test Suite for Enterprise Automation Framework.

Validates:
- UI Negative: Invalid credentials, locked accounts, blank fields, incomplete checkout forms, unauthorized page access
- API Negative: 404 resource errors, invalid endpoints, invalid payloads, missing authorization tokens
- Database Negative: Mismatch failure handling and query error safety
"""

from __future__ import annotations

import pytest
from src.base.base_test import BaseTest
from src.services.api_client import APIClient
from src.services.user_api import UserAPIService
from src.utils.db_utility import DBUtility
from src.utils.logger import get_logger

logger = get_logger("TestNegativeScenarios")


@pytest.mark.negative
class TestNegativeUI(BaseTest):
    """Negative UI test scenarios covering authentication, form validation, and access control."""

    @pytest.mark.ui
    def test_negative_login_locked_user_blocked(self, driver):
        """1. Verify locked-out user is prevented from signing in."""
        logger.info("Executing test_negative_login_locked_user_blocked")
        self.init_pages(driver)
        self.login_page.login("locked_out_user", "secret_sauce")

        error_msg = self.login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_msg, (
            f"Expected locked-out error message, received: '{error_msg}'"
        )
        assert "inventory.html" not in driver.current_url, "Locked user must not access inventory"

    @pytest.mark.ui
    def test_negative_login_invalid_password(self, driver):
        """2. Verify signing in with invalid password fails with descriptive error."""
        logger.info("Executing test_negative_login_invalid_password")
        self.init_pages(driver)
        self.login_page.login("standard_user", "wrong_password_xyz")

        error_msg = self.login_page.get_error_message()
        assert "Username and password do not match" in error_msg, (
            f"Expected invalid password message, received: '{error_msg}'"
        )

    @pytest.mark.ui
    def test_negative_login_empty_username_and_password(self, driver):
        """3. Verify submitting blank login form displays Username is required."""
        logger.info("Executing test_negative_login_empty_username_and_password")
        self.init_pages(driver)
        self.login_page.login("", "")

        error_msg = self.login_page.get_error_message()
        assert "Username is required" in error_msg, f"Expected required username error, got: '{error_msg}'"

    @pytest.mark.ui
    def test_negative_checkout_missing_postal_code(self, driver):
        """4. Verify checkout submission without postal code is rejected."""
        logger.info("Executing test_negative_checkout_missing_postal_code")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()

        self.checkout_page.enter_first_name("Jane")
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.enter_postal_code("")
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: Postal Code is required" in error_msg, (
            f"Expected Postal Code required error, received: '{error_msg}'"
        )

    @pytest.mark.ui
    def test_negative_checkout_missing_first_and_last_name(self, driver):
        """5. Verify submitting checkout form with only postal code triggers First Name is required."""
        logger.info("Executing test_negative_checkout_missing_first_and_last_name")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        self.home_page.go_to_cart()
        self.cart_page.checkout()

        self.checkout_page.enter_postal_code("90210")
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: First Name is required" in error_msg

    @pytest.mark.ui
    def test_negative_unauthorized_cart_access_after_logout(self, driver):
        """6. Verify navigating to /cart.html without active session redirects to login page."""
        logger.info("Executing test_negative_unauthorized_cart_access_after_logout")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.logout()

        base_url = self.config.get_base_url().rstrip("/")
        driver.get(f"{base_url}/cart.html")

        assert self.login_page.is_loaded(), "Unauthorized cart access must redirect to login"
        error_msg = self.login_page.get_error_message()
        assert "You can only access '/cart.html' when you are logged in" in error_msg, (
            f"Expected unauthorized cart access message, received: '{error_msg}'"
        )

    @pytest.mark.ui
    def test_negative_unauthorized_checkout_access_after_logout(self, driver):
        """7. Verify navigating to /checkout-step-one.html without auth redirects to login page."""
        logger.info("Executing test_negative_unauthorized_checkout_access_after_logout")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.logout()

        base_url = self.config.get_base_url().rstrip("/")
        driver.get(f"{base_url}/checkout-step-one.html")

        assert self.login_page.is_loaded()
        error_msg = self.login_page.get_error_message()
        assert "You can only access '/checkout-step-one.html' when you are logged in" in error_msg


@pytest.mark.negative
@pytest.mark.api
class TestNegativeAPI:
    """Negative REST API test scenarios validating error status codes and fault handling."""

    def test_negative_api_get_non_existent_resource_404(self):
        """8. Verify GET request for non-existent post ID returns HTTP 404."""
        logger.info("Executing test_negative_api_get_non_existent_resource_404")
        service = UserAPIService()
        response = service.get_user_by_id(post_id=99999999)
        assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"

    def test_negative_api_invalid_endpoint_404(self):
        """9. Verify GET request to invalid API endpoint returns HTTP 404."""
        logger.info("Executing test_negative_api_invalid_endpoint_404")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        response = client.get("invalid_api_v1_endpoint")
        assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"

    def test_negative_api_empty_post_payload(self):
        """10. Verify POST request with empty payload still executes safely without crashing."""
        logger.info("Executing test_negative_api_empty_post_payload")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        response = client.post("posts", data={})
        assert response.status_code in (201, 400), f"Expected 201 or 400 for empty payload, got {response.status_code}"

    def test_negative_api_put_invalid_resource_404(self):
        """11. Verify PUT update for non-existent resource ID returns 404 or 500 error."""
        logger.info("Executing test_negative_api_put_invalid_resource_404")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        response = client.put("posts/99999999", data={"title": "test", "body": "test"})
        assert response.status_code in (404, 500)


@pytest.mark.negative
@pytest.mark.database
@pytest.mark.db
class TestNegativeDatabase:
    """Negative database validation scenarios for data mismatches."""

    def test_negative_db_mismatch_assertion(self):
        """12. Verify DBUtility detects data discrepancy and fails with clear assertion details."""
        logger.info("Executing test_negative_db_mismatch_assertion")
        ui_item = {"name": "Sauce Labs Backpack", "price": "$99.99"}
        db_item = {"name": "Sauce Labs Backpack", "price": "$29.99"}

        with pytest.raises(AssertionError, match="Key 'price' Mismatch"):
            DBUtility.verify_ui_against_db(
                ui_data=ui_item,
                db_data=db_item,
                keys_to_compare=["name", "price"]
            )
        logger.info("test_negative_db_mismatch_assertion verified successfully")
