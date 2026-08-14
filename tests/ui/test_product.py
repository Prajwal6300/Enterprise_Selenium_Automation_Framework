"""Production-Ready UI Test Suite for SauceDemo Product Details Functionality.

Validates:
1. Opening product detail view from catalog listing
2. Product title verification on details view
3. Product price verification on details view
4. Product description validation on details view
5. Product hero image verification on details view
6. Adding item to cart from details page
7. Cart badge count update on details page
8. Removing item from cart on details page
9. Navigation back to catalog via 'Back to products' button
10. State consistency and preservation across navigation
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.logger import get_logger

logger = get_logger("TestProduct")


@pytest.mark.product
@pytest.mark.ui
@pytest.mark.regression
class TestProduct(BaseTest):
    """Test suite covering Product Details view and actions."""

    def test_open_product_detail_view(self, driver):
        """1. Verify clicking a product card navigates to the detailed view URL."""
        logger.info("Executing test_open_product_detail_view")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Backpack")
        assert "inventory-item.html" in driver.current_url, (
            f"Expected item detail URL, got: {driver.current_url}"
        )
        assert self.product_page.get_product_name() == "Sauce Labs Backpack"
        logger.info("test_open_product_detail_view passed")

    def test_product_detail_title_validation(self, driver):
        """2. Verify product title displayed on detail page matches selected product."""
        logger.info("Executing test_product_detail_title_validation")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        expected_name = "Sauce Labs Bike Light"
        self.home_page.open_product(expected_name)

        actual_name = self.product_page.get_product_name()
        assert actual_name == expected_name, f"Expected '{expected_name}', got '{actual_name}'"
        logger.info("test_product_detail_title_validation passed")

    def test_product_detail_price_validation(self, driver):
        """3. Verify product price string and parsed float value on detail view."""
        logger.info("Executing test_product_detail_price_validation")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Bolt T-Shirt")

        price_str = self.product_page.get_product_price()
        price_float = self.product_page.get_product_price_float()

        assert price_str == "$15.99", f"Expected '$15.99', got '{price_str}'"
        assert price_float == 15.99, f"Expected 15.99, got {price_float}"
        logger.info("test_product_detail_price_validation passed")

    def test_product_detail_description_validation(self, driver):
        """4. Verify product description text on detail view is non-empty and accurate."""
        logger.info("Executing test_product_detail_description_validation")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Fleece Jacket")

        desc = self.product_page.get_product_description()
        assert len(desc) > 30, f"Description is unexpectedly short: '{desc}'"
        assert "fleece jacket" in desc.lower()
        logger.info("test_product_detail_description_validation passed")

    def test_product_detail_image_src_validation(self, driver):
        """5. Verify product image element has a valid image source URL."""
        logger.info("Executing test_product_detail_image_src_validation")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Onesie")

        img_src = self.product_page.get_product_image_src()
        assert len(img_src) > 0, "Product detail image source is empty"
        assert ".jpg" in img_src or ".png" in img_src or "media" in img_src or "http" in img_src
        logger.info("test_product_detail_image_src_validation passed")

    def test_add_product_to_cart_from_detail_page(self, driver):
        """6. Verify clicking 'Add to cart' on detail page transitions button to 'Remove'."""
        logger.info("Executing test_add_product_to_cart_from_detail_page")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Backpack")
        self.product_page.add_to_cart()

        assert self.product_page.is_product_added_to_cart(), (
            "Expected 'Remove' button to be displayed after adding item from detail page"
        )
        logger.info("test_add_product_to_cart_from_detail_page passed")

    def test_cart_badge_increments_from_detail_page(self, driver):
        """7. Verify cart badge counter displays 1 after adding item from product details."""
        logger.info("Executing test_cart_badge_increments_from_detail_page")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Bike Light")
        self.product_page.add_to_cart()

        badge_count = self.product_page.get_cart_badge_count()
        assert badge_count == 1, f"Expected cart badge count 1, got {badge_count}"
        logger.info("test_cart_badge_increments_from_detail_page passed")

    def test_remove_product_from_cart_on_detail_page(self, driver):
        """8. Verify clicking 'Remove' on detail page removes item and clears badge."""
        logger.info("Executing test_remove_product_from_cart_on_detail_page")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Bolt T-Shirt")
        self.product_page.add_to_cart()
        assert self.product_page.get_cart_badge_count() == 1

        self.product_page.remove_from_cart()
        assert self.product_page.is_product_removed_from_cart(), (
            "Expected 'Add to cart' button to reappear after removing item"
        )
        assert self.product_page.get_cart_badge_count() == 0, "Badge count should reset to 0"
        logger.info("test_remove_product_from_cart_on_detail_page passed")

    def test_navigate_back_to_catalog_from_detail(self, driver):
        """9. Verify 'Back to products' button returns user to catalog listing."""
        logger.info("Executing test_navigate_back_to_catalog_from_detail")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Fleece Jacket")
        assert self.product_page.is_back_to_products_visible()

        self.product_page.back_to_products()
        assert self.home_page.is_loaded(), "Must return to home catalog page"
        assert self.home_page.get_product_count() == 6
        logger.info("test_navigate_back_to_catalog_from_detail passed")

    def test_product_detail_state_persistence_on_return(self, driver):
        """10. Verify item added on detail view continues to show 'Remove' button on catalog listing."""
        logger.info("Executing test_product_detail_state_persistence_on_return")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        target = "Sauce Labs Onesie"
        self.home_page.open_product(target)
        self.product_page.add_to_cart()

        self.product_page.back_to_products()
        assert self.home_page.is_loaded()
        assert self.home_page.is_product_in_cart_state(target), (
            f"Expected product '{target}' to show 'Remove' button in catalog listing"
        )
        assert self.home_page.get_cart_count() == 1
        logger.info("test_product_detail_state_persistence_on_return passed")
