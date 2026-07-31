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

    def verify_product_in_cart(self, product_name: str) -> bool:
        return product_name.strip() in self.get_cart_item_names()

    def verify_product_removed(self, product_name: str) -> bool:
        return product_name.strip() not in self.get_cart_item_names()

    def remove_product(self, product_name: str) -> None:
        self._click(self._remove_button_locator(product_name), f"remove button for {product_name}")

    def remove_item(self, product_name: str) -> None:
        self.remove_product(product_name)

    def checkout(self) -> None:
        self._click(self.CHECKOUT_BUTTON, "checkout button")

    def continue_shopping(self) -> None:
        self._click(self.CONTINUE_SHOPPING_BUTTON, "continue shopping button")

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
            self._find_clickable(locator).click()
            self.logger.debug("Clicked %s.", element_name)
        except WebDriverException as error:
            self.logger.exception("Unable to click %s.", element_name)
            raise RuntimeError(f"Unable to click {element_name}.") from error

    @staticmethod
    def _remove_button_locator(product_name: str) -> Locator:
        normalized_name = product_name.lower().replace(" ", "-").replace(".", "")
        return By.ID, f"remove-{normalized_name}"
