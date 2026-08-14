"""Page Object Model class for SauceDemo product interactions."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.logger import get_logger
from src.utils.wait_helper import Locator, WaitHelper


class ProductPage:
    """Encapsulate product list and product details page behavior."""

    INVENTORY_PRODUCT_NAMES: Locator = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_NAME: Locator = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESCRIPTION: Locator = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE: Locator = (By.CLASS_NAME, "inventory_details_price")
    PRODUCT_IMAGE: Locator = (By.CSS_SELECTOR, ".inventory_details_img")
    ADD_TO_CART_BUTTON: Locator = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON: Locator = (By.CSS_SELECTOR, "button[id^='remove']")
    BACK_TO_PRODUCTS_BUTTON: Locator = (By.ID, "back-to-products")
    CART_LINK: Locator = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE: Locator = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.logger = get_logger(self.__class__.__name__)


    def select_product(self, product_name: str) -> None:
        try:
            self._get_product_from_list(product_name).click()
            self.logger.info("Selected product '%s'.", product_name)
        except WebDriverException as error:
            self.logger.exception("Unable to select product '%s'.", product_name)
            raise RuntimeError(f"Unable to select product '{product_name}'.") from error

    def get_product_name(self) -> str:
        return self._find_visible(self.PRODUCT_NAME).text.strip()

    def get_product_description(self) -> str:
        return self._find_visible(self.PRODUCT_DESCRIPTION).text.strip()

    def get_product_price(self) -> str:
        return self._find_visible(self.PRODUCT_PRICE).text.strip()

    def get_product_price_float(self) -> float:
        """Return product price parsed as a float."""
        return float(self.get_product_price().replace("$", "").strip())

    def get_product_image_src(self) -> str:
        """Return product detail image src URL."""
        try:
            return self._find_visible(self.PRODUCT_IMAGE).get_attribute("src") or ""
        except Exception:
            return ""

    def get_cart_badge_count(self) -> int:
        """Return current shopping cart badge count from product details view."""
        try:
            return int(self._find_visible(self.CART_BADGE).text.strip())
        except TimeoutException:
            return 0

    def is_back_to_products_visible(self) -> bool:
        """Check if back to products button is visible."""
        try:
            return self._find_visible(self.BACK_TO_PRODUCTS_BUTTON).is_displayed()
        except TimeoutException:
            return False

    def verify_product_price(self, expected_price: str) -> bool:
        return self.get_product_price() == expected_price.strip()


    def add_to_cart(self) -> None:
        self._click(self.ADD_TO_CART_BUTTON, "add to cart button")
        self.logger.debug("Added product to cart from details page.")

    def remove_from_cart(self) -> None:
        self._click(self.REMOVE_BUTTON, "remove button")
        self.logger.debug("Removed product from cart on details page.")

    def is_product_added_to_cart(self) -> bool:
        try:
            return self._find_visible(self.REMOVE_BUTTON).is_displayed()
        except TimeoutException:
            return False

    def is_product_removed_from_cart(self) -> bool:
        try:
            return self._find_visible(self.ADD_TO_CART_BUTTON).is_displayed()
        except TimeoutException:
            return False

    def back_to_products(self) -> None:
        self._click(self.BACK_TO_PRODUCTS_BUTTON, "back to products button")
        self.wait.wait_until_url_contains("inventory.html")

    def go_to_cart(self) -> None:
        self._click(self.CART_LINK, "cart link")
        self.wait.wait_until_url_contains("cart.html")

    def _get_product_from_list(self, product_name: str) -> WebElement:
        expected_name = product_name.strip()
        for product in self.wait.wait_until_all_visible(self.INVENTORY_PRODUCT_NAMES):
            if product.text.strip() == expected_name:
                return product
        raise ValueError(f"Product was not found: {product_name}")

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
