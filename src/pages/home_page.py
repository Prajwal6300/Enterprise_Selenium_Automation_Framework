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
    PRODUCT_PRICES: Locator = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_DESCRIPTIONS: Locator = (By.CLASS_NAME, "inventory_item_desc")
    PRODUCT_IMAGES: Locator = (By.CSS_SELECTOR, ".inventory_item_img img")

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

    def get_product_count(self) -> int:
        """Return total number of visible product cards in catalog."""
        try:
            return len(self.wait.wait_until_all_visible(self.PRODUCT_CARDS))
        except TimeoutException:
            return 0

    def get_product_prices_raw(self) -> list[str]:
        """Return list of formatted price strings e.g. ['$29.99', '$9.99']."""
        return [element.text.strip() for element in self.wait.wait_until_all_visible(self.PRODUCT_PRICES)]

    def get_product_prices(self) -> list[float]:
        """Return list of float prices parsed from catalog."""
        raw_prices = self.get_product_prices_raw()
        return [float(p.replace("$", "").strip()) for p in raw_prices]

    def get_product_descriptions(self) -> list[str]:
        """Return list of product description strings."""
        return [element.text.strip() for element in self.wait.wait_until_all_visible(self.PRODUCT_DESCRIPTIONS)]

    def get_product_image_sources(self) -> list[str]:
        """Return list of image source URLs for all inventory cards."""
        return [elem.get_attribute("src") or "" for elem in self.wait.wait_until_all_visible(self.PRODUCT_IMAGES)]

    def get_all_products_catalog(self) -> list[dict[str, Any]]:
        """Return complete catalog data as list of dictionaries."""
        names = self.get_product_names()
        prices = self.get_product_prices_raw()
        descriptions = self.get_product_descriptions()
        images = self.get_product_image_sources()
        catalog = []
        for i in range(len(names)):
            catalog.append({
                "name": names[i],
                "price": prices[i] if i < len(prices) else "",
                "description": descriptions[i] if i < len(descriptions) else "",
                "image_src": images[i] if i < len(images) else "",
            })
        return catalog

    def search_product(self, search_text: str) -> list[str]:
        """Discover and filter products by name or partial text."""
        normalized_search_text = search_text.strip().lower()
        if not normalized_search_text:
            return self.get_product_names()
        return [name for name in self.get_product_names() if normalized_search_text in name.lower()]

    def is_product_displayed(self, product_name: str) -> bool:
        return product_name.strip() in self.get_product_names()

    def open_product(self, product_name: str) -> None:
        try:
            element = self._get_product_element(product_name)
            try:
                parent_a = element.find_element(By.XPATH, "./ancestor::a[1]")
                parent_a.click()
            except Exception:
                element.click()
            self.wait.wait_until_url_contains("inventory-item.html")
            self.logger.info("Opened product details page for '%s'.", product_name)
        except Exception:
            try:
                element = self._get_product_element(product_name)
                self.driver.execute_script("let a = arguments[0].closest('a'); if(a) { a.click(); } else { arguments[0].click(); }", element)
                self.wait.wait_until_url_contains("inventory-item.html")
                self.logger.info("Opened product details page for '%s' via JS click.", product_name)
            except Exception as error:
                self.logger.exception("Unable to open product '%s'.", product_name)
                raise RuntimeError(f"Unable to open product '{product_name}'.") from error

    def add_product_to_cart(self, product_name: str) -> None:
        button_locator = self._add_to_cart_button_locator(product_name)
        self._click(button_locator, f"add to cart button for {product_name}")

    def remove_product_from_cart(self, product_name: str) -> None:
        button_locator = self._remove_button_locator(product_name)
        self._click(button_locator, f"remove from cart button for {product_name}")

    def is_product_in_cart_state(self, product_name: str) -> bool:
        """Check if product card currently shows the 'Remove' button."""
        button_locator = self._remove_button_locator(product_name)
        try:
            return self._find_visible(button_locator).is_displayed()
        except TimeoutException:
            return False

    def sort_products(self, sort_value: str) -> None:
        try:
            Select(self._find_visible(self.SORT_DROPDOWN)).select_by_value(sort_value)
            self.logger.info("Sorted products using value '%s'.", sort_value)
        except WebDriverException as error:
            self.logger.exception("Unable to sort products using value '%s'.", sort_value)
            raise RuntimeError(f"Unable to sort products using value '{sort_value}'.") from error

    def get_active_sort_option(self) -> str:
        """Return value of the currently selected sort option."""
        try:
            return Select(self._find_visible(self.SORT_DROPDOWN)).first_selected_option.get_attribute("value") or ""
        except Exception:
            return ""

    def go_to_cart(self) -> None:
        self._click(self.CART_LINK, "cart link")
        self.wait.wait_until_url_contains("cart.html")

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
        self.wait.wait_until_visible((By.ID, "login-button"))
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
    def _add_to_cart_button_locator(product_name: str) -> Locator:
        normalized_name = product_name.lower().replace(" ", "-").replace(".", "")
        return By.ID, f"add-to-cart-{normalized_name}"

    @staticmethod
    def _remove_button_locator(product_name: str) -> Locator:
        normalized_name = product_name.lower().replace(" ", "-").replace(".", "")
        return By.ID, f"remove-{normalized_name}"

