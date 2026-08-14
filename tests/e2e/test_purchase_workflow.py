"""End-to-End Purchase Workflow and Business Journey Test Suite.

Validates multi-step enterprise user journeys:
1. Complete Browse -> Detail -> Add -> Continue Shopping -> Second Add -> Checkout -> Logout workflow
2. Price sorting -> High & Low Bundle Purchase -> Multi-item Overview Validation -> Purchase Completion
3. Reset App State workflow -> Clean slate verification
"""

from __future__ import annotations

import pytest

from src.base.base_test import BaseTest
from src.utils.logger import get_logger

logger = get_logger("TestPurchaseWorkflow")


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
class TestPurchaseWorkflow(BaseTest):
    """Business workflow test suite covering complex e-commerce purchase scenarios."""

    def test_e2e_browse_detail_continue_shopping_workflow(self, driver):
        """Scenario 3: Login -> Browse -> Detail 1 -> Add -> Continue shopping -> Add item 2 -> Cart -> Checkout -> Finish -> Logout."""
        logger.info("Executing test_e2e_browse_detail_continue_shopping_workflow")
        self.init_pages(driver)

        # 1. Login
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded()

        # 2. Open Product 1 Details & Add
        self.home_page.open_product("Sauce Labs Fleece Jacket")
        assert self.product_page.get_product_price() == "$49.99"
        self.product_page.add_to_cart()
        assert self.product_page.get_cart_badge_count() == 1

        # 3. Back to Products & Add Product 2 directly
        self.product_page.back_to_products()
        assert self.home_page.is_loaded()
        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        assert self.home_page.get_cart_count() == 2

        # 4. Open Cart & Verify Contents
        self.home_page.go_to_cart()
        assert self.cart_page.is_loaded()
        assert self.cart_page.get_cart_item_count() == 2
        subtotal = self.cart_page.calculate_subtotal()
        assert subtotal == round(49.99 + 7.99, 2)

        # 5. Checkout
        self.cart_page.checkout()
        self.checkout_page.enter_address("Samantha", "Reed", "90210")
        self.checkout_page.continue_to_overview()

        # 6. Verify Overview Financials
        overview_subtotal = self.checkout_page.get_subtotal_amount()
        expected_subtotal = round(49.99 + 7.99, 2)
        assert round(overview_subtotal, 2) == expected_subtotal
        assert round(self.checkout_page.get_total_amount(), 2) == round(overview_subtotal + self.checkout_page.get_tax_amount(), 2)

        # 7. Complete Purchase
        self.checkout_page.finish_order()
        assert self.checkout_page.is_complete_page_loaded()
        assert self.checkout_page.get_complete_message() == "Thank you for your order!"

        # 8. Return Home & Logout
        self.checkout_page.back_to_products_after_complete()
        assert self.home_page.is_loaded()
        assert self.home_page.get_cart_count() == 0

        self.home_page.logout()
        assert self.login_page.is_loaded()
        logger.info("test_e2e_browse_detail_continue_shopping_workflow passed")

    def test_e2e_sorted_catalog_bundle_purchase(self, driver):
        """Scenario: Sort catalog High-to-Low -> Purchase most expensive ($49.99) and cheapest ($7.99) -> Verify checkout totals."""
        logger.info("Executing test_e2e_sorted_catalog_bundle_purchase")
        self.init_pages(driver)

        # Login
        self.login_page.login("standard_user", "secret_sauce")

        # Sort High to Low
        self.home_page.sort_products("hilo")
        prices = self.home_page.get_product_prices()
        assert prices[0] == 49.99 and prices[-1] == 7.99

        # Add highest and lowest priced items
        self.home_page.add_product_to_cart("Sauce Labs Fleece Jacket")
        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        assert self.home_page.get_cart_count() == 2

        # Proceed to checkout
        self.home_page.go_to_cart()
        assert self.cart_page.is_loaded()
        self.cart_page.checkout()
        assert self.checkout_page.is_information_page_loaded()
        self.checkout_page.complete_order("Oliver", "Queen", "98001")

        assert self.checkout_page.verify_order()
        logger.info("test_e2e_sorted_catalog_bundle_purchase passed")
