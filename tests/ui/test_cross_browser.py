"""Cross-Browser Validation Test Suite.

Validates application responsiveness, core navigation, and authentication flows
across Chrome, Firefox, and Edge browsers in headed and headless modes.
"""

from __future__ import annotations

import pytest
from src.base.base_test import BaseTest
from src.utils.logger import get_logger

logger = get_logger("TestCrossBrowser")


@pytest.mark.cross_browser
@pytest.mark.ui
@pytest.mark.regression
class TestCrossBrowser(BaseTest):
    """Test suite designated for cross-browser validation runs."""

    def test_cross_browser_login_and_catalog_render(self, driver):
        """Verify login and full catalog rendering across target browser engines."""
        logger.info("Executing test_cross_browser_login_and_catalog_render")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "Home page must load successfully"

        product_count = self.home_page.get_product_count()
        assert product_count == 6, f"Expected 6 products rendered, found: {product_count}"

        images = self.home_page.get_product_image_sources()
        assert len(images) == 6, "All 6 product images must be present"
        logger.info("test_cross_browser_login_and_catalog_render passed")

    def test_cross_browser_cart_and_checkout_flow(self, driver):
        """Verify cart addition and checkout workflow across target browser engines."""
        logger.info("Executing test_cross_browser_cart_and_checkout_flow")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()

        assert self.cart_page.is_loaded(), "Cart page must load"
        self.cart_page.checkout()

        self.checkout_page.complete_order("Cross", "Browser", "90210")
        assert self.checkout_page.verify_order(), "Order should be verified on target browser"
        logger.info("test_cross_browser_cart_and_checkout_flow passed")
