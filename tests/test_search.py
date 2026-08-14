"""Production-ready UI Test Suite for SauceDemo Search and Inventory Discovery.

Validates catalog listing, sorting options, and opening product detail pages.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestSearch")


@pytest.mark.product
@pytest.mark.search
@pytest.mark.regression
@pytest.mark.ui
class TestSearch(BaseTest):
    """Test suite covering inventory catalog search, discovery, and detailed view."""

    def test_product_is_listed_and_searchable_by_name(self, driver):
        """Verify that expected products appear in the inventory listing."""
        logger.info("Executing test_product_is_listed_and_searchable_by_name")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]
        product_data = ExcelReader(Path("testdata/Products.xlsx")).get_sheet_data("products")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        assert self.home_page.is_loaded(), "Home page must be loaded after login"

        product_names = self.home_page.get_product_names()
        assert product_data["name"] in product_names, (
            f"Expected product '{product_data['name']}' to be present in inventory: {product_names}"
        )
        logger.info("test_product_is_listed_and_searchable_by_name passed")

    def test_search_partial_product_name(self, driver):
        """Verify discovering products using partial search string."""
        logger.info("Executing test_search_partial_product_name")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "Home page must load"

        matches = self.home_page.search_product("Light")
        assert len(matches) >= 1, "Expected at least 1 match for partial query 'Light'"
        assert any("Bike Light" in m for m in matches), f"Expected Bike Light in matches: {matches}"
        logger.info("test_search_partial_product_name passed")

    def test_search_case_insensitive_matching(self, driver):
        """Verify search filtering matches regardless of uppercase or lowercase characters."""
        logger.info("Executing test_search_case_insensitive_matching")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        upper_matches = self.home_page.search_product("BACKPACK")
        lower_matches = self.home_page.search_product("backpack")
        mixed_matches = self.home_page.search_product("BackPack")

        assert upper_matches == lower_matches == mixed_matches, (
            f"Case insensitivity check failed: upper={upper_matches}, lower={lower_matches}, mixed={mixed_matches}"
        )
        assert len(upper_matches) == 1, "Expected exactly 1 backpack match"
        logger.info("test_search_case_insensitive_matching passed")

    def test_search_non_existent_product_returns_empty(self, driver):
        """Verify search query for non-existent item returns an empty match list."""
        logger.info("Executing test_search_non_existent_product_returns_empty")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        matches = self.home_page.search_product("UNOBTAINABLE_GADGET_999")
        assert len(matches) == 0, f"Expected 0 matches for non-existent query, got: {matches}"
        logger.info("test_search_non_existent_product_returns_empty passed")

    def test_search_special_characters_returns_no_matches(self, driver):
        """Verify search query containing special characters returns empty without crashing."""
        logger.info("Executing test_search_special_characters_returns_no_matches")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        matches = self.home_page.search_product("@#$%^&*")
        assert len(matches) == 0, f"Expected 0 matches for special characters, got: {matches}"
        logger.info("test_search_special_characters_returns_no_matches passed")

    def test_search_empty_input_returns_all_products(self, driver):
        """Verify searching with empty string returns full product catalog."""
        logger.info("Executing test_search_empty_input_returns_all_products")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        matches = self.home_page.search_product("")
        assert len(matches) == 6, f"Expected 6 products for empty search, got: {len(matches)}"
        logger.info("test_search_empty_input_returns_all_products passed")

    def test_search_numeric_input_handling(self, driver):
        """Verify searching with numeric string handles safely and returns no matches if non-existent."""
        logger.info("Executing test_search_numeric_input_handling")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        matches = self.home_page.search_product("987654321")
        assert len(matches) == 0, f"Expected 0 matches for numeric query, got: {len(matches)}"
        logger.info("test_search_numeric_input_handling passed")

    def test_catalog_displays_all_product_cards(self, driver):
        """Verify catalog renders 6 product cards with non-empty titles and prices."""
        logger.info("Executing test_catalog_displays_all_product_cards")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        count = self.home_page.get_product_count()
        assert count == 6, f"Expected 6 products in default inventory, found: {count}"
        
        prices = self.home_page.get_product_prices()
        assert len(prices) == 6, "Every product must have a readable price"
        assert all(p > 0 for p in prices), "All product prices must be greater than zero"
        logger.info("test_catalog_displays_all_product_cards passed")

    def test_catalog_images_are_loaded_and_valid(self, driver):
        """Verify all inventory product cards contain valid rendered images."""
        logger.info("Executing test_catalog_images_are_loaded_and_valid")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        images = self.home_page.get_product_image_sources()
        assert len(images) == 6, f"Expected 6 product images, found: {len(images)}"
        assert all(img.startswith("http") or "media" in img or ".jpg" in img or ".png" in img for img in images), (
            f"Invalid image src paths detected: {images}"
        )
        logger.info("test_catalog_images_are_loaded_and_valid passed")

    def test_product_sorting_name_az(self, driver):
        """Verify sorting products by Name (A to Z) arranges names in alphabetical order."""
        logger.info("Executing test_product_sorting_name_az")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.sort_products("az")
        
        names = self.home_page.get_product_names()
        assert names == sorted(names), f"Products are not sorted alphabetically A-Z: {names}"
        logger.info("test_product_sorting_name_az passed")

    def test_product_sorting_name_za(self, driver):
        """Verify sorting products by Name (Z to A) arranges names in reverse alphabetical order."""
        logger.info("Executing test_product_sorting_name_za")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.sort_products("za")
        
        names = self.home_page.get_product_names()
        assert names == sorted(names, reverse=True), f"Products are not sorted reverse alphabetically Z-A: {names}"
        logger.info("test_product_sorting_name_za passed")

    def test_product_sorting_price_low_to_high(self, driver):
        """Verify sorting products by Price (low to high) arranges items in ascending price order."""
        logger.info("Executing test_product_sorting_price_low_to_high")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.sort_products("lohi")
        
        prices = self.home_page.get_product_prices()
        assert prices == sorted(prices), f"Prices are not sorted low-to-high: {prices}"
        assert prices[0] == 7.99, f"Expected cheapest item to be $7.99, got: {prices[0]}"
        assert prices[-1] == 49.99, f"Expected most expensive item to be $49.99, got: {prices[-1]}"
        logger.info("test_product_sorting_price_low_to_high passed")

    def test_product_sorting_price_high_to_low(self, driver):
        """Verify sorting products by Price (high to low) arranges items in descending price order."""
        logger.info("Executing test_product_sorting_price_high_to_low")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.sort_products("hilo")
        
        prices = self.home_page.get_product_prices()
        assert prices == sorted(prices, reverse=True), f"Prices are not sorted high-to-low: {prices}"
        assert prices[0] == 49.99, f"Expected most expensive item first ($49.99), got: {prices[0]}"
        assert prices[-1] == 7.99, f"Expected cheapest item last ($7.99), got: {prices[-1]}"
        logger.info("test_product_sorting_price_high_to_low passed")

    def test_open_product_details(self, driver):
        """Verify clicking a product navigates to the detailed view with matching price & description."""
        logger.info("Executing test_open_product_details")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]
        product_data = ExcelReader(Path("testdata/Products.xlsx")).get_sheet_data("products")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        self.home_page.open_product(product_data["name"])

        actual_name = self.product_page.get_product_name()
        actual_price = self.product_page.get_product_price()

        assert actual_name == product_data["name"], (
            f"Product title mismatch. Expected: {product_data['name']}, Got: {actual_name}"
        )
        assert actual_price == product_data["price"], (
            f"Product price mismatch. Expected: {product_data['price']}, Got: {actual_price}"
        )
        logger.info("test_open_product_details passed")

    def test_product_price_and_desc_consistency_between_home_and_details(self, driver):
        """Verify product details page maintains exact name, price, and description from home page."""
        logger.info("Executing test_product_price_and_desc_consistency_between_home_and_details")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        target_product = "Sauce Labs Fleece Jacket"
        
        self.home_page.open_product(target_product)
        
        detail_name = self.product_page.get_product_name()
        detail_price = self.product_page.get_product_price()
        detail_desc = self.product_page.get_product_description()
        
        assert detail_name == target_product, f"Expected detail name {target_product}, got {detail_name}"
        assert detail_price == "$49.99", f"Expected price $49.99, got {detail_price}"
        assert len(detail_desc) > 10, f"Expected valid product description, got: {detail_desc}"
        
        # Navigate back to products list
        self.product_page.back_to_products()
        assert self.home_page.is_loaded(), "Back to products button should return to inventory"
        logger.info("test_product_price_and_desc_consistency_between_home_and_details passed")

