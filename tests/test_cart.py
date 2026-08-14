"""Production-ready UI Test Suite for SauceDemo Shopping Cart.

Validates:
1. Adding single product to cart
2. Adding second product to cart
3. Adding multiple products (3 items)
4. Badge count updates accurately
5. Product name validation in cart
6. Product price validation in cart
7. Product quantity validation in cart
8. Removing a single item from cart
9. Removing multiple items from cart
10. Removing all items from cart (empty cart state)
11. 'Continue Shopping' navigation back to inventory
12. 'Checkout' navigation from cart
13. Cart state persistence after browser refresh
14. Dynamic subtotal calculation
15. Preservation of product order in cart
16. Add, remove, and re-add product cycle
17. Badge removal when cart reaches 0 items
18. Cart data integrity across session navigation
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
        """1. Verify adding an item updates the cart count and adds item to cart list."""
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

    def test_add_second_product_to_cart(self, driver):
        """2. Verify adding a second product increments cart count to 2 and displays both in cart."""
        logger.info("Executing test_add_second_product_to_cart")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        assert self.home_page.get_cart_count() == 1

        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        assert self.home_page.get_cart_count() == 2

        self.home_page.go_to_cart()
        items = self.cart_page.get_cart_item_names()
        assert len(items) == 2
        assert "Sauce Labs Backpack" in items and "Sauce Labs Bike Light" in items
        logger.info("test_add_second_product_to_cart passed")

    def test_add_multiple_products_to_cart(self, driver):
        """3. Verify adding multiple distinct items correctly populates cart and badge count."""
        logger.info("Executing test_add_multiple_products_to_cart")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]
        for item in products_to_add:
            self.home_page.add_product_to_cart(item)
            
        assert self.home_page.get_cart_count() == 3, "Badge count should be 3 after adding 3 items"
        
        self.home_page.go_to_cart()
        assert self.cart_page.is_loaded(), "Cart page must load"
        
        items_in_cart = self.cart_page.get_cart_item_names()
        for item in products_to_add:
            assert item in items_in_cart, f"Item '{item}' missing from cart list: {items_in_cart}"
        logger.info("test_add_multiple_products_to_cart passed")

    def test_cart_badge_count_reflects_items(self, driver):
        """4. Verify cart icon badge number matches exact count of added items."""
        logger.info("Executing test_cart_badge_count_reflects_items")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.get_cart_count() == 0

        self.home_page.add_product_to_cart("Sauce Labs Fleece Jacket")
        assert self.home_page.get_cart_count() == 1

        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        assert self.home_page.get_cart_count() == 2

        self.home_page.go_to_cart()
        assert self.cart_page.get_cart_badge_count() == 2
        logger.info("test_cart_badge_count_reflects_items passed")

    def test_cart_item_name_validation(self, driver):
        """5. Verify product name displayed inside cart matches catalog item name."""
        logger.info("Executing test_cart_item_name_validation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        target_name = "Sauce Labs Bolt T-Shirt"
        self.home_page.add_product_to_cart(target_name)
        self.home_page.go_to_cart()

        names = self.cart_page.get_cart_item_names()
        assert target_name in names, f"Expected '{target_name}' in cart, found: {names}"
        logger.info("test_cart_item_name_validation passed")

    def test_cart_item_price_validation(self, driver):
        """6. Verify product price displayed in cart matches catalog price."""
        logger.info("Executing test_cart_item_price_validation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Fleece Jacket")
        self.home_page.go_to_cart()

        prices = self.cart_page.get_cart_item_prices()
        assert 49.99 in prices, f"Expected $49.99 in cart prices: {prices}"
        logger.info("test_cart_item_price_validation passed")

    def test_cart_item_unit_prices_and_quantities(self, driver):
        """7. Verify each cart item displays accurate unit price and positive quantity."""
        logger.info("Executing test_cart_item_unit_prices_and_quantities")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack") # $29.99
        self.home_page.add_product_to_cart("Sauce Labs Bike Light") # $9.99
        self.home_page.go_to_cart()
        
        prices = self.cart_page.get_cart_item_prices()
        quantities = self.cart_page.get_cart_item_quantities()
        
        assert prices == [29.99, 9.99], f"Unexpected cart prices: {prices}"
        assert quantities == [1, 1], f"Unexpected quantities: {quantities}"
        logger.info("test_cart_item_unit_prices_and_quantities passed")

    def test_remove_product_from_cart(self, driver):
        """8. Verify removing an item removes it from the cart list."""
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

    def test_remove_multiple_products_from_cart(self, driver):
        """9. Verify removing multiple items selectively leaves remaining items in cart."""
        logger.info("Executing test_remove_multiple_products_from_cart")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        self.home_page.go_to_cart()

        assert self.cart_page.get_cart_item_count() == 3
        self.cart_page.remove_product("Sauce Labs Backpack")
        self.cart_page.remove_product("Sauce Labs Bike Light")

        remaining = self.cart_page.get_cart_item_names()
        assert remaining == ["Sauce Labs Onesie"], f"Expected only Onesie, got: {remaining}"
        assert self.cart_page.get_cart_badge_count() == 1
        logger.info("test_remove_multiple_products_from_cart passed")

    def test_remove_all_products_from_cart(self, driver):
        """10. Verify bulk removal leaves an empty shopping cart and clears the badge."""
        logger.info("Executing test_remove_all_products_from_cart")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.add_product_to_cart("Sauce Labs Onesie")
        self.home_page.go_to_cart()
        
        self.cart_page.remove_all_items()
        
        assert self.cart_page.get_cart_item_count() == 0, "Cart item count must be 0 after removing all items"
        assert self.cart_page.get_cart_badge_count() == 0, "Badge count should be 0 when cart is empty"
        logger.info("test_remove_all_products_from_cart passed")

    def test_continue_shopping_returns_to_inventory(self, driver):
        """11. Verify 'Continue Shopping' button navigates back to products catalog with active cart preserved."""
        logger.info("Executing test_continue_shopping_returns_to_inventory")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        
        self.cart_page.continue_shopping()
        
        assert self.home_page.is_loaded(), "Should return to inventory page"
        assert self.home_page.get_cart_count() == 1, "Cart badge count must remain 1 after returning to inventory"
        logger.info("test_continue_shopping_returns_to_inventory passed")

    def test_navigate_from_cart_to_checkout(self, driver):
        """12. Verify clicking 'Checkout' on cart page navigates to checkout step one."""
        logger.info("Executing test_navigate_from_cart_to_checkout")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        
        self.cart_page.checkout()
        assert self.checkout_page.is_information_page_loaded(), "Must load checkout step 1 page"
        assert "checkout-step-one.html" in driver.current_url
        logger.info("test_navigate_from_cart_to_checkout passed")

    def test_cart_persistence_after_browser_refresh(self, driver):
        """13. Verify items in cart persist when the cart page is refreshed."""
        logger.info("Executing test_cart_persistence_after_browser_refresh")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        self.home_page.go_to_cart()
        
        driver.refresh()
        
        assert self.cart_page.is_loaded(), "Cart page should reload successfully"
        assert self.cart_page.verify_product_in_cart("Sauce Labs Backpack"), (
            "Sauce Labs Backpack must still be in cart after refresh"
        )
        logger.info("test_cart_persistence_after_browser_refresh passed")

    def test_cart_subtotal_dynamic_calculation(self, driver):
        """14. Verify dynamically calculated subtotal = sum(price * qty) matches items in cart."""
        logger.info("Executing test_cart_subtotal_dynamic_calculation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Fleece Jacket") # $49.99
        self.home_page.add_product_to_cart("Sauce Labs Onesie")        # $7.99
        self.home_page.go_to_cart()
        
        calculated_subtotal = self.cart_page.calculate_subtotal()
        expected_subtotal = round(49.99 + 7.99, 2)
        
        assert calculated_subtotal == expected_subtotal, (
            f"Calculated subtotal mismatch: expected {expected_subtotal}, got {calculated_subtotal}"
        )
        logger.info("test_cart_subtotal_dynamic_calculation passed with total $%s", calculated_subtotal)

    def test_cart_item_order_preserved(self, driver):
        """15. Verify items appear in cart in the sequential order they were added."""
        logger.info("Executing test_cart_item_order_preserved")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        order_added = ["Sauce Labs Bolt T-Shirt", "Sauce Labs Bike Light", "Sauce Labs Backpack"]
        for p in order_added:
            self.home_page.add_product_to_cart(p)
            
        self.home_page.go_to_cart()
        cart_items = self.cart_page.get_cart_item_names()
        assert cart_items == order_added, f"Order mismatch: expected {order_added}, got {cart_items}"
        logger.info("test_cart_item_order_preserved passed")

    def test_add_remove_and_re_add_product_to_cart(self, driver):
        """16. Verify product can be added, removed, and added back cleanly."""
        logger.info("Executing test_add_remove_and_re_add_product_to_cart")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        target = "Sauce Labs Backpack"
        
        # 1. Add
        self.home_page.add_product_to_cart(target)
        assert self.home_page.get_cart_count() == 1
        
        # 2. Remove
        self.home_page.remove_product_from_cart(target)
        assert self.home_page.get_cart_count() == 0
        
        # 3. Re-add
        self.home_page.add_product_to_cart(target)
        assert self.home_page.get_cart_count() == 1
        
        self.home_page.go_to_cart()
        assert self.cart_page.verify_product_in_cart(target)
        logger.info("test_add_remove_and_re_add_product_to_cart passed")

    def test_cart_badge_disappears_when_cart_is_empty(self, driver):
        """17. Verify cart badge element is removed when the last cart item is deleted."""
        logger.info("Executing test_cart_badge_disappears_when_cart_is_empty")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Backpack")
        assert self.home_page.get_cart_count() == 1
        
        self.home_page.go_to_cart()
        self.cart_page.remove_product("Sauce Labs Backpack")
        
        assert self.cart_page.get_cart_badge_count() == 0, "Badge count should be 0"
        logger.info("test_cart_badge_disappears_when_cart_is_empty passed")

    def test_cart_data_integrity_across_session_navigation(self, driver):
        """18. Verify cart items persist across page navigation between home, details, and cart."""
        logger.info("Executing test_cart_data_integrity_across_session_navigation")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.add_product_to_cart("Sauce Labs Bike Light")
        
        # Navigate to product details
        self.home_page.open_product("Sauce Labs Fleece Jacket")
        assert self.product_page.get_cart_badge_count() == 1
        
        # Navigate from details directly to cart
        self.product_page.go_to_cart()
        assert self.cart_page.is_loaded()
        assert self.cart_page.verify_product_in_cart("Sauce Labs Bike Light")
        logger.info("test_cart_data_integrity_across_session_navigation passed")
