"""Production-ready UI Test Suite for SauceDemo Checkout Workflow.

Validates end-to-end purchasing, customer information entry, summary verification,
and order completion confirmation.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestCheckout")


@pytest.mark.checkout
@pytest.mark.smoke
@pytest.mark.ui
class TestCheckout(BaseTest):
    """Test suite covering end-to-end checkout functionality."""

    def test_complete_checkout_successfully(self, driver):
        """Verify successful order submission with valid customer details."""
        logger.info("Executing test_complete_checkout_successfully")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]
        product_data = ExcelReader(Path("testdata/Products.xlsx")).get_sheet_data("products")[0]
        customer_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("checkout_users")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        self.home_page.add_product_to_cart(product_data["name"])
        self.home_page.go_to_cart()
        self.cart_page.checkout()

        assert self.checkout_page.is_information_page_loaded(), "Checkout step 1 page must be loaded"

        self.checkout_page.complete_order(
            customer_data["first_name"],
            customer_data["last_name"],
            str(customer_data["postal_code"]),
        )

        complete_msg = self.checkout_page.get_complete_message()
        assert complete_msg == "Thank you for your order!", (
            f"Expected order confirmation header 'Thank you for your order!', got '{complete_msg}'"
        )
        logger.info("test_complete_checkout_successfully passed")

    def test_checkout_requires_first_name(self, driver):
        """Verify validation error is displayed when customer first name is omitted."""
        logger.info("Executing test_checkout_requires_first_name")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]
        product_data = ExcelReader(Path("testdata/Products.xlsx")).get_sheet_data("products")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        self.home_page.add_product_to_cart(product_data["name"])
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: First Name is required" in error_msg, (
            f"Expected validation error 'Error: First Name is required', but got '{error_msg}'"
        )
        logger.info("test_checkout_requires_first_name passed")
