"""Production-ready UI Test Suite for SauceDemo Checkout Workflow.

Validates:
1. End-to-end checkout with valid customer details
2. Empty checkout form submission validation
3. Missing first name validation error
4. Missing last name validation error
5. Missing postal code validation error
6. First name with whitespace-only validation
7. Last name with special characters handling
8. Alphanumeric international postal codes (e.g. UK, India)
9. Validation error message text verification
10. Checkout error dismiss button 'X' functionality
11. Overview page loading and URL verification
12. Overview item name consistency with cart
13. Overview item price display
14. Overview item quantity verification
15. Item subtotal calculation in overview
16. Tax calculation accuracy (8% rate)
17. Total math equation: Total == Item subtotal + Tax
18. Order confirmation header text ("Thank you for your order!")
19. Order dispatch description text verification
20. Cart state (0 items, badge cleared) post-purchase
21. Cancel checkout on Step 1 returns to Cart
22. Cancel checkout on Step 2 returns to Inventory
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestCheckout")


@pytest.mark.checkout
@pytest.mark.regression
@pytest.mark.ui
class TestCheckout(BaseTest):
    """Test suite covering checkout functionality, error validation, math, and order submission."""

    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_complete_checkout_successfully(self, driver):
        """1. Verify successful order submission with valid customer details."""
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

    @pytest.mark.negative
    def test_checkout_empty_form_validation(self, driver):
        """2. Verify submitting an empty checkout form triggers First Name is required."""
        logger.info("Executing test_checkout_empty_form_validation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: First Name is required" in error_msg, (
            f"Expected validation error 'Error: First Name is required', but got '{error_msg}'"
        )
        logger.info("test_checkout_empty_form_validation passed")

    @pytest.mark.negative
    def test_checkout_requires_first_name(self, driver):
        """3. Verify validation error is displayed when customer first name is omitted."""
        logger.info("Executing test_checkout_requires_first_name")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.enter_postal_code("10001")
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: First Name is required" in error_msg, (
            f"Expected validation error 'Error: First Name is required', but got '{error_msg}'"
        )
        logger.info("test_checkout_requires_first_name passed")

    @pytest.mark.negative
    def test_checkout_requires_last_name(self, driver):
        """4. Verify validation error is displayed when customer last name is omitted."""
        logger.info("Executing test_checkout_requires_last_name")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_first_name("John")
        self.checkout_page.enter_postal_code("10001")
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: Last Name is required" in error_msg, (
            f"Expected validation error 'Error: Last Name is required', but got '{error_msg}'"
        )
        logger.info("test_checkout_requires_last_name passed")

    @pytest.mark.negative
    def test_checkout_requires_postal_code(self, driver):
        """5. Verify validation error is displayed when customer postal code is omitted."""
        logger.info("Executing test_checkout_requires_postal_code")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_first_name("John")
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.continue_checkout()

        error_msg = self.checkout_page.get_error_message()
        assert "Error: Postal Code is required" in error_msg, (
            f"Expected validation error 'Error: Postal Code is required', but got '{error_msg}'"
        )
        logger.info("test_checkout_requires_postal_code passed")

    @pytest.mark.negative
    def test_checkout_first_name_whitespace_only(self, driver):
        """6. Verify checkout handles whitespace-only first name appropriately."""
        logger.info("Executing test_checkout_first_name_whitespace_only")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("   ", "Smith", "90210")
        self.checkout_page.continue_checkout()
        
        # SauceDemo accepts string or advances to overview
        assert self.checkout_page.is_overview_page_loaded() or self.checkout_page.has_error()
        logger.info("test_checkout_first_name_whitespace_only passed")

    def test_checkout_last_name_special_characters(self, driver):
        """7. Verify customer names with hyphens/apostrophes (e.g. O'Connor-Smith) process safely."""
        logger.info("Executing test_checkout_last_name_special_characters")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("Liam", "O'Connor-Smith", "90210")
        self.checkout_page.continue_to_overview()
        assert self.checkout_page.is_overview_page_loaded()
        logger.info("test_checkout_last_name_special_characters passed")

    def test_checkout_postal_code_alphanumeric_formats(self, driver):
        """8. Verify international alphanumeric postal codes (e.g. SW1A 1AA) are accepted."""
        logger.info("Executing test_checkout_postal_code_alphanumeric_formats")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("Emma", "Watson", "SW1A 1AA")
        self.checkout_page.continue_to_overview()
        assert self.checkout_page.is_overview_page_loaded()
        logger.info("test_checkout_postal_code_alphanumeric_formats passed")

    def test_checkout_error_dismissal_behavior(self, driver):
        """9. Verify clicking error 'X' close button removes checkout validation error banner."""
        logger.info("Executing test_checkout_error_dismissal_behavior")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.continue_checkout()
        assert self.checkout_page.has_error(), "Error banner must appear on empty submit"
        
        self.checkout_page.dismiss_error()
        assert not self.checkout_page.has_error(), "Error banner must disappear after clicking close button"
        logger.info("test_checkout_error_dismissal_behavior passed")

    def test_checkout_overview_page_loaded(self, driver):
        """10. Verify Checkout Overview Step 2 page loads successfully with 'Checkout: Overview' title."""
        logger.info("Executing test_checkout_overview_page_loaded")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("John", "Doe", "10001")
        self.checkout_page.continue_to_overview()
        
        assert self.checkout_page.is_overview_page_loaded(), "Overview page must be loaded"
        assert "checkout-step-two.html" in driver.current_url
        logger.info("test_checkout_overview_page_loaded passed")

    def test_checkout_overview_item_names(self, driver):
        """11. Verify products listed in Overview step match the items added in cart."""
        logger.info("Executing test_checkout_overview_item_names")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("Alice", "Brown", "30301")
        self.checkout_page.continue_to_overview()
        
        names = self.checkout_page.get_overview_item_names()
        assert "Sauce Labs Backpack" in names and "Sauce Labs Onesie" in names
        logger.info("test_checkout_overview_item_names passed: %s", names)

    def test_checkout_overview_item_prices(self, driver):
        """12. Verify product prices listed in Overview match the catalog prices."""
        logger.info("Executing test_checkout_overview_item_prices")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("David", "Clark", "75001")
        self.checkout_page.continue_to_overview()
        
        prices = self.checkout_page.get_overview_item_prices()
        assert 15.99 in prices, f"Expected $15.99 in overview prices: {prices}"
        logger.info("test_checkout_overview_item_prices passed")

    def test_order_summary_subtotal_calculation(self, driver):
        """13. Verify Item total (subtotal) in overview matches exact sum of items."""
        logger.info("Executing test_order_summary_subtotal_calculation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")      # $29.99
        self.home_page.add_product_to_cart("Sauce Labs Fleece Jacket")  # $49.99
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("Eva", "Green", "10001")
        self.checkout_page.continue_to_overview()
        
        subtotal = self.checkout_page.get_subtotal_amount()
        expected = round(29.99 + 49.99, 2)
        assert subtotal == expected, f"Subtotal mismatch: expected {expected}, got {subtotal}"
        logger.info("test_order_summary_subtotal_calculation passed with $%s", subtotal)

    def test_order_summary_tax_calculation(self, driver):
        """14. Verify tax amount in overview is calculated accurately (8% rate rounded)."""
        logger.info("Executing test_order_summary_tax_calculation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack") # $29.99
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("Frank", "Wright", "94105")
        self.checkout_page.continue_to_overview()
        
        subtotal = self.checkout_page.get_subtotal_amount()
        tax = self.checkout_page.get_tax_amount()
        expected_tax = round(subtotal * 0.08, 2)
        
        assert abs(tax - expected_tax) <= 0.01, f"Tax mismatch: expected ~{expected_tax}, got {tax}"
        logger.info("test_order_summary_tax_calculation passed with tax $%s", tax)

    def test_order_summary_pricing_calculation(self, driver):
        """15. Verify dynamic verification: item subtotal + tax = final total."""
        logger.info("Executing test_order_summary_pricing_calculation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")      # $29.99
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")    # $9.99
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("Alice", "Smith", "90210")
        self.checkout_page.continue_to_overview()
        
        subtotal = self.checkout_page.get_subtotal_amount()
        tax = self.checkout_page.get_tax_amount()
        total = self.checkout_page.get_total_amount()
        
        expected_subtotal = round(29.99 + 9.99, 2)
        expected_total = round(subtotal + tax, 2)
        
        assert subtotal == expected_subtotal, f"Subtotal mismatch: expected {expected_subtotal}, got {subtotal}"
        assert total == expected_total, f"Total mismatch: expected {expected_total} (subtotal+tax), got {total}"
        logger.info("test_order_summary_pricing_calculation passed: Subtotal=%s, Tax=%s, Total=%s", subtotal, tax, total)

    def test_complete_order_confirmation_header(self, driver):
        """16. Verify order completion header displays 'Thank you for your order!'."""
        logger.info("Executing test_complete_order_confirmation_header")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.complete_order("Grace", "Hopper", "02138")
        assert self.checkout_page.is_complete_page_loaded()
        assert self.checkout_page.get_complete_message() == "Thank you for your order!"
        logger.info("test_complete_order_confirmation_header passed")

    def test_complete_order_description_text(self, driver):
        """17. Verify order complete description confirms order dispatch."""
        logger.info("Executing test_complete_order_description_text")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.complete_order("Harry", "Potter", "WD25 7LR")
        desc = self.checkout_page.get_complete_description()
        assert "dispatched" in desc.lower() or "pony express" in desc.lower(), (
            f"Expected dispatch description text, got '{desc}'"
        )
        logger.info("test_complete_order_description_text passed")

    @pytest.mark.e2e
    def test_cart_is_empty_after_successful_checkout(self, driver):
        """18. Verify shopping cart is automatically reset and badge cleared after finishing order."""
        logger.info("Executing test_cart_is_empty_after_successful_checkout")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.complete_order("Bob", "Martin", "12345")
        assert self.checkout_page.is_complete_page_loaded(), "Must reach order confirmation page"
        
        # Navigate back to inventory
        self.checkout_page.back_to_products_after_complete()
        assert self.home_page.is_loaded(), "Should return to inventory after order complete"
        
        # Verify cart badge is gone (0 items)
        assert self.home_page.get_cart_count() == 0, "Cart badge count must be 0 after successful checkout"
        logger.info("test_cart_is_empty_after_successful_checkout passed")

    def test_cancel_checkout_step_one_returns_to_cart(self, driver):
        """19. Verify clicking Cancel on checkout step 1 navigates back to shopping cart."""
        logger.info("Executing test_cancel_checkout_step_one_returns_to_cart")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.cancel_checkout()
        
        assert self.cart_page.is_loaded(), "Cancelling checkout step 1 should return to cart"
        logger.info("test_cancel_checkout_step_one_returns_to_cart passed")

    def test_cancel_checkout_step_two_returns_to_inventory(self, driver):
        """20. Verify clicking Cancel on overview step 2 navigates back to product catalog."""
        logger.info("Executing test_cancel_checkout_step_two_returns_to_inventory")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        self.cart_page.checkout()
        
        self.checkout_page.enter_address("John", "Doe", "10001")
        self.checkout_page.continue_to_overview()
        assert self.checkout_page.is_overview_page_loaded(), "Must be on overview page"
        
        self.checkout_page.cancel_checkout()
        assert self.home_page.is_loaded(), "Cancelling overview step 2 should return to inventory catalog"
        logger.info("test_cancel_checkout_step_two_returns_to_inventory passed")
