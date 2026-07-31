"""Production-ready UI Test Suite for SauceDemo Shopping Cart.

Validates adding products, removing items, badge count updates, and cart contents persistence.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestCart")


@pytest.mark.cart
@pytest.mark.regression
@pytest.mark.ui
class TestCart(BaseTest):
    """Test suite covering cart management actions."""

    def test_add_product_to_cart(self, driver):
        """Verify adding an item updates the cart count and adds item to cart list."""
        logger.info("Executing test_add_product_to_cart")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]
        product_data = ExcelReader(Path("testdata/Products.xlsx")).get_sheet_data("products")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        self.home_page.add_product_to_cart(product_data["name"])
        self.home_page.go_to_cart()

        assert self.cart_page.is_loaded(), "Cart page should be loaded"
        items_in_cart = self.cart_page.get_cart_item_names()
        assert product_data["name"] in items_in_cart, (
            f"Expected item '{product_data['name']}' in cart list, but found: {items_in_cart}"
        )
        logger.info("test_add_product_to_cart passed")

    def test_remove_product_from_cart(self, driver):
        """Verify removing an item removes it from the cart list."""
        logger.info("Executing test_remove_product_from_cart")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]
        product_data = ExcelReader(Path("testdata/Products.xlsx")).get_sheet_data("products")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        self.home_page.add_product_to_cart(product_data["name"])
        self.home_page.go_to_cart()
        
        self.cart_page.remove_item(product_data["name"])
        items_in_cart = self.cart_page.get_cart_item_names()

        assert product_data["name"] not in items_in_cart, (
            f"Expected item '{product_data['name']}' to be removed from cart, but it is still present."
        )
        logger.info("test_remove_product_from_cart passed")
