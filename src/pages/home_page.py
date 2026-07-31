"""Page Object Model class for the SauceDemo inventory home page."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from src.utils.logger import get_logger
from src.utils.wait_helper import Locator, WaitHelper


class HomePage:
    """Encapsulate inventory page locators, menu actions, product search, and verifications."""

    PAGE_TITLE: Locator = (By.CLASS_NAME, "title")
    CART_LINK: Locator = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE: Locator = (By.CLASS_NAME, "shopping_cart_badge")
    MENU_BUTTON: Locator = (By.ID, "react-burger-menu-btn")
    MENU_CONTAINER: Locator = (By.CLASS_NAME, "bm-menu-wrap")
    MENU_CLOSE_BUTTON: Locator = (By.ID, "react-burger-cross-btn")
    ALL_ITEMS_LINK: Locator = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK: Locator = (By.ID, "about_sidebar_link")
    LOGOUT_LINK: Locator = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK: Locator = (By.ID, "reset_sidebar_link")
    LOGIN_BUTTON: Locator = (By.ID, "login-button")
    SORT_DROPDOWN: Locator = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_CARDS: Locator = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME_LINKS: Locator = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_loaded(self) -> bool:
        try:
            return self.get_page_title() == "Products" and len(self.get_product_names()) > 0
        except TimeoutException:
            self.logger.warning("Home page was not loaded within the configured timeout.")
            return False

    def get_page_title(self) -> str:
        return self._find_visible(self.PAGE_TITLE).text.strip()

    def get_product_names(self) -> list[str]:
        return [element.text.strip() for element in self.wait.wait_until_all_visible(self.PRODUCT_NAME_LINKS)]

    def search_product(self, search_text: str) -> list[str]:
        normalized_search_text = search_text.strip().lower()
        if not normalized_search_text:
            raise ValueError("Search text cannot be empty.")
        return [name for name in self.get_product_names() if normalized_search_text in name.lower()]

    def is_product_displayed(self, product_name: str) -> bool:
        return product_name.strip() in self.get_product_names()

    def open_product(self, product_name: str) -> None:
        try:
            self._get_product_element(product_name).click()
            self.logger.info("Opened product details page for '%s'.", product_name)
        except WebDriverException as error:
            self.logger.exception("Unable to open product '%s'.", product_name)
            raise RuntimeError(f"Unable to open product '{product_name}'.") from error

    def add_product_to_cart(self, product_name: str) -> None:
        button_locator = self._add_to_cart_button_locator(product_name)
        self._click(button_locator, f"add to cart button for {product_name}")

    def sort_products(self, sort_value: str) -> None:
        try:
            Select(self._find_visible(self.SORT_DROPDOWN)).select_by_value(sort_value)
            self.logger.info("Sorted products using value '%s'.", sort_value)
        except WebDriverException as error:
            self.logger.exception("Unable to sort products using value '%s'.", sort_value)
            raise RuntimeError(f"Unable to sort products using value '{sort_value}'.") from error

    def go_to_cart(self) -> None:
        self._click(self.CART_LINK, "cart link")

    def get_cart_count(self) -> int:
        try:
            return int(self._find_visible(self.CART_BADGE).text.strip())
        except TimeoutException:
            return 0

    def open_menu(self) -> None:
        self._click(self.MENU_BUTTON, "menu button")
        self.wait.wait_until_visible(self.LOGOUT_LINK)

    def close_menu(self) -> None:
        self._click(self.MENU_CLOSE_BUTTON, "menu close button")

    def is_menu_open(self) -> bool:
        try:
            return self._find_visible(self.MENU_CONTAINER).is_displayed()
        except TimeoutException:
            return False

    def logout(self) -> None:
        self.open_menu()
        logout_elem = self.wait.wait_until_visible(self.LOGOUT_LINK)
        self.driver.execute_script("arguments[0].click();", logout_elem)
        self.logger.info("Logged out successfully via JS click.")

    def reset_app_state(self) -> None:
        self.open_menu()
        self._click(self.RESET_APP_STATE_LINK, "reset app state link")

    def verify_product_count(self, expected_count: int) -> bool:
        return len(self.get_product_names()) == expected_count

    def verify_cart_count(self, expected_count: int) -> bool:
        return self.get_cart_count() == expected_count

    def _get_product_element(self, product_name: str) -> WebElement:
        expected_name = product_name.strip()
        for element in self.wait.wait_until_all_visible(self.PRODUCT_NAME_LINKS):
            if element.text.strip() == expected_name:
                return element
        raise ValueError(f"Product was not found on home page: {product_name}")

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
    def _add_to_cart_button_locator(product_name: str) -> Locator:
        normalized_name = product_name.lower().replace(" ", "-").replace(".", "")
        return By.ID, f"add-to-cart-{normalized_name}"
