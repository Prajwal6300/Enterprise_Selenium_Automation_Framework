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
