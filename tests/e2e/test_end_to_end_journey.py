"""Comprehensive End-to-End (E2E) Business Journey Test Suite.

Validates complete multi-stage user journeys across the entire application:
1. Authentication & Catalog Discovery
2. Product Detail Inspection & Cart Addition
3. Cart Subtotal Verification & Quantity Adjustments
4. Multi-Step Checkout Information & Overview Math Verification
5. Purchase Completion & Order Dispatch Confirmation
6. Post-Order Cart State Verification & Clean Logout
"""

from __future__ import annotations

import pytest
from src.base.base_test import BaseTest
from src.utils.logger import get_logger

logger = get_logger("TestE2EJourney")


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
class TestEndToEndJourney(BaseTest):
    """End-to-End business workflow test suite."""

    def test_complete_e2e_shopping_journey(self, driver):
        """Execute complete user journey from login, browsing, details, cart, checkout, to logout."""
        logger.info("Executing test_complete_e2e_shopping_journey")
        self.init_pages(driver)

        # 1. Login
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "Home page must be displayed after login"

        # 2. Browse & Sort Catalog
        self.home_page.sort_products("lohi")
        prices = self.home_page.get_product_prices()
        assert prices == sorted(prices), "Products should be sorted from lowest to highest price"

        # 3. View Product Details
        target_product = "Sauce Labs Backpack"
        self.home_page.open_product(target_product)
        assert self.product_page.get_product_name() == target_product, "Product details name mismatch"
        assert self.product_page.get_product_price() == "$29.99", "Product details price mismatch"

        # 4. Add to Cart from Details Page
        self.product_page.add_to_cart()
        assert self.product_page.get_cart_badge_count() == 1, "Cart badge should display 1 item"

        # 5. Return to Products & Add Second Item
        self.product_page.back_to_products()
        assert self.home_page.is_loaded(), "Returned to inventory page"
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        assert self.home_page.get_cart_count() == 2, "Cart badge should display 2 items"

        # 6. Open Cart & Verify Items and Subtotal Calculation
        self.home_page.go_to_cart()
        assert self.cart_page.is_loaded(), "Cart page should be loaded"
        assert self.cart_page.get_cart_item_count() == 2, "Cart must contain 2 items"
        subtotal = self.cart_page.calculate_subtotal()
        assert subtotal == round(29.99 + 9.99, 2), f"Calculated subtotal mismatch: {subtotal}"

        # 7. Proceed to Checkout Step 1
        self.cart_page.checkout()
        assert self.checkout_page.is_information_page_loaded(), "Checkout Step 1 must load"

        # 8. Enter Customer Details & Proceed to Overview Step 2
        self.checkout_page.enter_address("Enterprise", "Architect", "10001")
        self.checkout_page.continue_to_overview()
        assert self.checkout_page.is_overview_page_loaded(), "Checkout Overview Step 2 must load"

        # 9. Verify Overview Financial Breakdown
        overview_subtotal = self.checkout_page.get_subtotal_amount()
        overview_tax = self.checkout_page.get_tax_amount()
        overview_total = self.checkout_page.get_total_amount()
        assert round(overview_subtotal, 2) == round(29.99 + 9.99, 2), "Subtotal in overview mismatch"
        assert round(overview_total, 2) == round(overview_subtotal + overview_tax, 2), "Total must equal subtotal + tax"

        # 10. Finish Order & Verify Complete Confirmation
        self.checkout_page.finish_order()
        assert self.checkout_page.is_complete_page_loaded(), "Complete confirmation page must load"
        assert self.checkout_page.get_complete_message() == "Thank you for your order!"

        # 11. Return Home and Verify Empty Cart
        self.checkout_page.back_to_products_after_complete()
        assert self.home_page.is_loaded(), "Home page must load after completing order"
        assert self.home_page.get_cart_count() == 0, "Cart badge must be cleared (0 items)"

        # 12. Logout
        self.home_page.logout()
        assert self.login_page.is_loaded(), "User must be logged out on login page"
        logger.info("test_complete_e2e_shopping_journey completed successfully")

    def test_e2e_multi_item_selective_removal_checkout(self, driver):
        """Verify adding multiple items, removing one in cart, and completing checkout with remaining item."""
        logger.info("Executing test_e2e_multi_item_selective_removal_checkout")
        self.init_pages(driver)

        # Login
        self.login_page.login("standard_user", "secret_sauce")

        # Add 3 products
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        self.home_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        assert self.home_page.get_cart_count() == 3

        # Go to cart and remove Bike Light
        self.home_page.go_to_cart()
        assert self.cart_page.get_cart_item_count() == 3
        self.cart_page.remove_product("Sauce Labs Bike Light")
        assert self.cart_page.get_cart_item_count() == 2
        assert not self.cart_page.verify_product_in_cart("Sauce Labs Bike Light")

        # Complete checkout for remaining 2 items
        self.cart_page.checkout()
        self.checkout_page.complete_order("David", "Miller", "30301")
        assert self.checkout_page.verify_order(), "Order confirmation must succeed"
        logger.info("test_e2e_multi_item_selective_removal_checkout passed")
