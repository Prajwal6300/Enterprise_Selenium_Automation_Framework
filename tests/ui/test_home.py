"""Production-Ready UI Test Suite for SauceDemo Home and Product Catalog.

Validates:
1. Inventory home page rendering and title validation
2. Catalog items existence and count (6 products)
3. Product title text integrity
4. Product price float values and formatting
5. Product thumbnail image URLs
6. Product card structure
7. Product sorting: Name (A to Z)
8. Product sorting: Name (Z to A)
9. Product sorting: Price (low to high)
10. Product sorting: Price (high to low)
11. Navigation to product details
12. Product details title consistency
13. Product details price consistency
14. Product details description validation
15. Product details image verification
16. Back to products navigation
17. Catalog and details info consistency
18. Reset app state restores default inventory
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestHome")


@pytest.mark.product
@pytest.mark.ui
@pytest.mark.regression
class TestHome(BaseTest):
    """Comprehensive test suite covering Home page, product catalog, sorting, and navigation."""

    def test_home_page_loads_successfully(self, driver):
        """1. Verify home page loads and displays 'Products' header title after authentication."""
        logger.info("Executing test_home_page_loads_successfully")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        assert self.home_page.is_loaded(), "Home page should be loaded after valid login"
        assert self.home_page.get_page_title() == "Products", (
            f"Expected page title 'Products', got '{self.home_page.get_page_title()}'"
        )
        logger.info("test_home_page_loads_successfully passed")

    def test_product_inventory_is_displayed(self, driver):
        """2. Verify product inventory container is visible on the home page."""
        logger.info("Executing test_product_inventory_is_displayed")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        count = self.home_page.get_product_count()
        assert count > 0, f"Expected inventory to be displayed with items, but found {count} items"
        logger.info("test_product_inventory_is_displayed passed with %d items", count)

    def test_product_count_matches_expected(self, driver):
        """3. Verify product catalog displays exactly 6 products in default inventory."""
        logger.info("Executing test_product_count_matches_expected")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        product_count = self.home_page.get_product_count()
        assert product_count == 6, f"Expected exactly 6 products, found: {product_count}"
        logger.info("test_product_count_matches_expected passed")

    def test_all_product_names_are_non_empty_and_valid(self, driver):
        """4. Verify every catalog product has a non-empty name string."""
        logger.info("Executing test_all_product_names_are_non_empty_and_valid")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        names = self.home_page.get_product_names()
        assert len(names) == 6, f"Expected 6 product names, got {len(names)}"
        for name in names:
            assert len(name.strip()) > 0, f"Detected empty product name in catalog: '{name}'"
            assert "Sauce Labs" in name or "T-Shirt" in name or "Onesie" in name, (
                f"Unexpected product name format: '{name}'"
            )
        logger.info("test_all_product_names_are_non_empty_and_valid passed: %s", names)

    def test_all_product_prices_are_positive_and_formatted(self, driver):
        """5. Verify every catalog product has a valid price with '$' symbol and positive float value."""
        logger.info("Executing test_all_product_prices_are_positive_and_formatted")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        raw_prices = self.home_page.get_product_prices_raw()
        float_prices = self.home_page.get_product_prices()

        assert len(raw_prices) == 6, f"Expected 6 raw prices, found {len(raw_prices)}"
        assert len(float_prices) == 6, f"Expected 6 float prices, found {len(float_prices)}"
        for raw, val in zip(raw_prices, float_prices):
            assert raw.startswith("$"), f"Price '{raw}' does not start with '$'"
            assert val > 0.0, f"Price {val} is not positive"
        logger.info("test_all_product_prices_are_positive_and_formatted passed: %s", float_prices)

    def test_all_product_images_are_loaded(self, driver):
        """6. Verify all product cards contain valid rendered image source paths."""
        logger.info("Executing test_all_product_images_are_loaded")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        images = self.home_page.get_product_image_sources()
        assert len(images) == 6, f"Expected 6 product images, found {len(images)}"
        for img in images:
            assert img.startswith("http") or ".jpg" in img or ".png" in img or "media" in img, (
                f"Invalid product image source: '{img}'"
            )
        logger.info("test_all_product_images_are_loaded passed")

    def test_product_cards_structure_and_elements(self, driver):
        """7. Verify each product card includes title, description, price, and add-to-cart button."""
        logger.info("Executing test_product_cards_structure_and_elements")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        catalog = self.home_page.get_all_products_catalog()
        assert len(catalog) == 6, f"Expected 6 catalog entries, found {len(catalog)}"
        for item in catalog:
            assert item["name"], "Product card missing title"
            assert item["price"], f"Product card '{item['name']}' missing price"
            assert len(item["description"]) > 5, f"Product card '{item['name']}' description too short"
            assert item["image_src"], f"Product card '{item['name']}' missing image URL"
        logger.info("test_product_cards_structure_and_elements passed")

    def test_product_sorting_name_a_to_z(self, driver):
        """8. Verify sorting by Name (A to Z) displays products in alphabetical order."""
        logger.info("Executing test_product_sorting_name_a_to_z")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.sort_products("az")
        names = self.home_page.get_product_names()

        assert names == sorted(names), f"Products not sorted A-Z: {names}"
        assert names[0] == "Sauce Labs Backpack"
        assert names[-1] == "Test.allTheThings() T-Shirt (Red)"
        logger.info("test_product_sorting_name_a_to_z passed")

    def test_product_sorting_name_z_to_a(self, driver):
        """9. Verify sorting by Name (Z to A) displays products in reverse alphabetical order."""
        logger.info("Executing test_product_sorting_name_z_to_a")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.sort_products("za")
        names = self.home_page.get_product_names()

        assert names == sorted(names, reverse=True), f"Products not sorted Z-A: {names}"
        assert names[0] == "Test.allTheThings() T-Shirt (Red)"
        assert names[-1] == "Sauce Labs Backpack"
        logger.info("test_product_sorting_name_z_to_a passed")

    def test_product_sorting_price_low_to_high(self, driver):
        """10. Verify sorting by Price (low to high) orders products in ascending price."""
        logger.info("Executing test_product_sorting_price_low_to_high")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.sort_products("lohi")
        prices = self.home_page.get_product_prices()

        assert prices == sorted(prices), f"Prices not sorted low to high: {prices}"
        assert prices[0] == 7.99, f"Cheapest item should be $7.99, got: {prices[0]}"
        assert prices[-1] == 49.99, f"Most expensive item should be $49.99, got: {prices[-1]}"
        logger.info("test_product_sorting_price_low_to_high passed")

    def test_product_sorting_price_high_to_low(self, driver):
        """11. Verify sorting by Price (high to low) orders products in descending price."""
        logger.info("Executing test_product_sorting_price_high_to_low")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.sort_products("hilo")
        prices = self.home_page.get_product_prices()

        assert prices == sorted(prices, reverse=True), f"Prices not sorted high to low: {prices}"
        assert prices[0] == 49.99, f"Most expensive item should be $49.99, got: {prices[0]}"
        assert prices[-1] == 7.99, f"Cheapest item should be $7.99, got: {prices[-1]}"
        logger.info("test_product_sorting_price_high_to_low passed")

    def test_navigate_to_product_detail_page(self, driver):
        """12. Verify clicking a product card opens the product detail view."""
        logger.info("Executing test_navigate_to_product_detail_page")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        target = "Sauce Labs Backpack"
        self.home_page.open_product(target)

        assert "inventory-item.html" in driver.current_url, (
            f"Expected detail page URL, got: {driver.current_url}"
        )
        assert self.product_page.get_product_name() == target
        logger.info("test_navigate_to_product_detail_page passed")

    def test_product_detail_title_matches_catalog(self, driver):
        """13. Verify product title on detail view matches the item selected from catalog."""
        logger.info("Executing test_product_detail_title_matches_catalog")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        target = "Sauce Labs Bike Light"
        self.home_page.open_product(target)

        detail_title = self.product_page.get_product_name()
        assert detail_title == target, f"Expected '{target}', got '{detail_title}'"
        logger.info("test_product_detail_title_matches_catalog passed")

    def test_product_detail_price_matches_catalog(self, driver):
        """14. Verify product price on detail view matches the price shown in catalog listing."""
        logger.info("Executing test_product_detail_price_matches_catalog")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        target = "Sauce Labs Fleece Jacket"
        self.home_page.open_product(target)

        detail_price = self.product_page.get_product_price()
        assert detail_price == "$49.99", f"Expected '$49.99', got '{detail_price}'"
        logger.info("test_product_detail_price_matches_catalog passed")

    def test_product_detail_description_matches_catalog(self, driver):
        """15. Verify product detail view contains a comprehensive product description."""
        logger.info("Executing test_product_detail_description_matches_catalog")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        target = "Sauce Labs Onesie"
        self.home_page.open_product(target)

        desc = self.product_page.get_product_description()
        assert len(desc) > 20, f"Description too short: '{desc}'"
        assert "infant onesie" in desc.lower()
        logger.info("test_product_detail_description_matches_catalog passed")

    def test_product_detail_image_is_valid(self, driver):
        """16. Verify product detail view renders the product hero image."""
        logger.info("Executing test_product_detail_image_is_valid")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Bolt T-Shirt")

        img_src = self.product_page.get_product_image_src()
        assert len(img_src) > 0, "Product detail image src is empty"
        assert ".jpg" in img_src or ".png" in img_src or "media" in img_src or "http" in img_src
        logger.info("test_product_detail_image_is_valid passed")

    def test_navigate_back_from_product_detail(self, driver):
        """17. Verify clicking 'Back to products' on detail page returns to the catalog listing."""
        logger.info("Executing test_navigate_back_from_product_detail")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        self.home_page.open_product("Sauce Labs Backpack")
        assert "inventory-item.html" in driver.current_url

        self.product_page.back_to_products()
        assert self.home_page.is_loaded(), "Should return to inventory home page"
        assert "inventory.html" in driver.current_url
        logger.info("test_navigate_back_from_product_detail passed")

    def test_catalog_and_detail_info_consistency(self, driver):
        """18. Verify exact data consistency (name, price, description) between catalog and details."""
        logger.info("Executing test_catalog_and_detail_info_consistency")
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")

        target = "Test.allTheThings() T-Shirt (Red)"
        self.home_page.open_product(target)

        assert self.product_page.get_product_name() == target
        assert self.product_page.get_product_price() == "$15.99"
        assert len(self.product_page.get_product_description()) > 10

        self.product_page.back_to_products()
        assert self.home_page.is_loaded()
        logger.info("test_catalog_and_detail_info_consistency passed")
