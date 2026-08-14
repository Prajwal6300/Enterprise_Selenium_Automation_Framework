"""Page Object Model class for the SauceDemo cart page."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.logger import get_logger
from src.utils.wait_helper import Locator, WaitHelper


class CartPage:
    """Encapsulate cart page locators, actions, and verifications."""

    PAGE_TITLE: Locator = (By.CLASS_NAME, "title")
    CART_ITEMS: Locator = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES: Locator = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_PRICES: Locator = (By.CLASS_NAME, "inventory_item_price")
    CART_QUANTITIES: Locator = (By.CLASS_NAME, "cart_quantity")
    CART_BADGE: Locator = (By.CLASS_NAME, "shopping_cart_badge")
    CHECKOUT_BUTTON: Locator = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON: Locator = (By.ID, "continue-shopping")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_loaded(self) -> bool:
        try:
            return self.get_page_title() == "Your Cart"
        except TimeoutException:
            self.logger.warning("Cart page was not loaded within the configured timeout.")
            return False

    def get_page_title(self) -> str:
        return self._find_visible(self.PAGE_TITLE).text.strip()

    def get_cart_item_names(self) -> list[str]:
        try:
            return [item.text.strip() for item in self.wait.wait_until_all_visible(self.CART_ITEM_NAMES)]
        except TimeoutException:
            return []

    def get_cart_item_prices_raw(self) -> list[str]:
        """Return raw string prices of items in cart."""
        try:
            return [elem.text.strip() for elem in self.wait.wait_until_all_visible(self.CART_ITEM_PRICES)]
        except TimeoutException:
            return []

    def get_cart_item_prices(self) -> list[float]:
        """Return parsed float prices of items in cart."""
        raw_prices = self.get_cart_item_prices_raw()
        return [float(p.replace("$", "").strip()) for p in raw_prices]

    def get_cart_item_quantities(self) -> list[int]:
        """Return integer quantities of all cart items."""
        try:
            return [int(elem.text.strip()) for elem in self.wait.wait_until_all_visible(self.CART_QUANTITIES)]
        except TimeoutException:
            return []

    def calculate_subtotal(self) -> float:
        """Calculate dynamic subtotal = sum(unit_price * quantity) for all cart items."""
        prices = self.get_cart_item_prices()
        quantities = self.get_cart_item_quantities()
        if not prices:
            return 0.0
        total = 0.0
        for i in range(len(prices)):
            qty = quantities[i] if i < len(quantities) else 1
            total += prices[i] * qty
        return round(total, 2)

    def get_all_cart_items_data(self) -> list[dict[str, Any]]:
        """Return structured cart items data."""
        names = self.get_cart_item_names()
        prices = self.get_cart_item_prices_raw()
        quantities = self.get_cart_item_quantities()
        items = []
        for i in range(len(names)):
            items.append({
                "name": names[i],
                "price": prices[i] if i < len(prices) else "",
                "quantity": quantities[i] if i < len(quantities) else 1,
            })
        return items

    def verify_product_in_cart(self, product_name: str) -> bool:
        return product_name.strip() in self.get_cart_item_names()

    def verify_product_removed(self, product_name: str) -> bool:
        return product_name.strip() not in self.get_cart_item_names()

    def remove_product(self, product_name: str) -> None:
        self._click(self._remove_button_locator(product_name), f"remove button for {product_name}")

    def remove_item(self, product_name: str) -> None:
        self.remove_product(product_name)

    def remove_all_items(self) -> None:
        """Remove all products currently displayed in the cart."""
        while True:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".cart_item button")
            if not buttons:
                break
            try:
                buttons[0].click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", buttons[0])
        self.logger.info("Removed all items from cart.")


    def get_cart_badge_count(self) -> int:
        """Return current badge count on shopping cart icon."""
        try:
            return int(self._find_visible(self.CART_BADGE).text.strip())
        except TimeoutException:
            return 0

    def checkout(self) -> None:
        self._click(self.CHECKOUT_BUTTON, "checkout button")
        self.wait.wait_until_url_contains("checkout-step-one.html")

    def continue_shopping(self) -> None:
        self._click(self.CONTINUE_SHOPPING_BUTTON, "continue shopping button")
        self.wait.wait_until_url_contains("inventory.html")

    def get_cart_item_count(self) -> int:
        try:
            return len(self.wait.wait_until_all_visible(self.CART_ITEMS))
        except TimeoutException:
            return 0


    def _find_visible(self, locator: Locator) -> WebElement:
        return self.wait.wait_until_visible(locator)

    def _find_clickable(self, locator: Locator) -> WebElement:
        return self.wait.wait_until_clickable(locator)

    def _click(self, locator: Locator, element_name: str) -> None:
        try:
            element = self._find_clickable(locator)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.debug("Clicked %s.", element_name)
        except Exception:
            try:
                elem = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", elem)
                self.logger.debug("Clicked %s via fallback.", element_name)
            except Exception as error:
                self.logger.exception("Unable to click %s.", element_name)
                raise RuntimeError(f"Unable to click {element_name}.") from error

    @staticmethod
    def _remove_button_locator(product_name: str) -> Locator:
        normalized_name = product_name.lower().replace(" ", "-").replace(".", "")
        return By.ID, f"remove-{normalized_name}"
