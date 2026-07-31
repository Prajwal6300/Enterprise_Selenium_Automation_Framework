"""Page Object Model for the SauceDemo checkout workflow."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.logger import get_logger
from src.utils.wait_helper import Locator, WaitHelper


class CheckoutPage:
    """Encapsulate checkout information, overview, and confirmation pages."""

    TITLE: Locator = (By.CLASS_NAME, "title")
    FIRST_NAME_INPUT: Locator = (By.ID, "first-name")
    LAST_NAME_INPUT: Locator = (By.ID, "last-name")
    POSTAL_CODE_INPUT: Locator = (By.ID, "postal-code")
    CONTINUE_BUTTON: Locator = (By.ID, "continue")
    FINISH_BUTTON: Locator = (By.ID, "finish")
    COMPLETE_HEADER: Locator = (By.CLASS_NAME, "complete-header")
    ERROR_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-test='error']")
    SUMMARY_TOTAL: Locator = (By.CLASS_NAME, "summary_total_label")

    INFORMATION_TITLE = "Checkout: Your Information"
    OVERVIEW_TITLE = "Checkout: Overview"
    COMPLETION_MESSAGE = "Thank you for your order!"

    def __init__(self, driver: WebDriver) -> None:
        """Store the browser and create the shared synchronization utilities."""
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_information_page_loaded(self) -> bool:
        """Return whether the checkout address form is currently displayed."""
        return self._verify_title(self.INFORMATION_TITLE)

    def is_overview_page_loaded(self) -> bool:
        """Return whether the order overview page is currently displayed."""
        return self._verify_title(self.OVERVIEW_TITLE)

    def enter_first_name(self, first_name: str) -> None:
        """Enter the customer's first name in the checkout address form."""
        self._replace_text(self.FIRST_NAME_INPUT, first_name, "first name")

    def enter_last_name(self, last_name: str) -> None:
        """Enter the customer's last name in the checkout address form."""
        self._replace_text(self.LAST_NAME_INPUT, last_name, "last name")

    def enter_postal_code(self, postal_code: str) -> None:
        """Enter the customer's postal code in the checkout address form."""
        self._replace_text(self.POSTAL_CODE_INPUT, postal_code, "postal code")

    def enter_address(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill all required checkout address fields."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def enter_customer_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Backward-compatible alias for :meth:`enter_address`."""
        self.enter_address(first_name, last_name, postal_code)

    def continue_checkout(self) -> None:
        """Submit the address form and move to the order overview."""
        btn = self._find_clickable(self.CONTINUE_BUTTON)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
        if "checkout-step-one" in self.driver.current_url:
            self.driver.execute_script("arguments[0].click();", btn)
        self.logger.debug("Clicked Continue button.")

    def continue_to_overview(self) -> None:
        """Continue to the overview and verify that navigation succeeded."""
        self.continue_checkout()
        self._wait_for_title(self.OVERVIEW_TITLE)

    def finish_order(self) -> None:
        """Submit the order from the overview page."""
        try:
            btn = self._find_clickable(self.FINISH_BUTTON)
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
            if "checkout-step-two" in self.driver.current_url:
                self.driver.execute_script("arguments[0].click();", btn)
            self.logger.info("Finished checkout order.")
        except WebDriverException as error:
            self.logger.exception("Unable to finish checkout order.")
            raise RuntimeError("Unable to finish checkout order.") from error

    def finish_checkout(self) -> None:
        """Backward-compatible alias for :meth:`finish_order`."""
        self.finish_order()

    def complete_order(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill the address, continue to the overview, and finish the order."""
        self.enter_address(first_name, last_name, postal_code)
        self.continue_to_overview()
        self.finish_order()

    def verify_order(self, expected_message: str = COMPLETION_MESSAGE) -> bool:
        """Return whether the confirmation page contains the expected order message."""
        try:
            actual_message = self.wait.wait_until_visible(self.COMPLETE_HEADER).text.strip()
            is_verified = actual_message == expected_message
            if not is_verified:
                self.logger.error(
                    "Order verification failed. Expected '%s', received '%s'.",
                    expected_message,
                    actual_message,
                )
            return is_verified
        except TimeoutException:
            self.logger.warning("Order confirmation message was not displayed.")
            return False

    def get_complete_message(self) -> str:
        """Return the visible order confirmation message."""
        return self._find_visible(self.COMPLETE_HEADER).text.strip()

    def get_error_message(self) -> str:
        """Return checkout validation error text."""
        return self._find_visible(self.ERROR_MESSAGE).text.strip()

    def get_summary_total(self) -> str:
        """Return the order total shown on the overview page."""
        return self._find_visible(self.SUMMARY_TOTAL).text.strip()

    def _verify_title(self, expected_title: str) -> bool:
        """Compare the page title after waiting for it to become visible."""
        try:
            return self._find_visible(self.TITLE).text.strip() == expected_title
        except TimeoutException:
            self.logger.warning("Expected checkout page '%s' was not loaded.", expected_title)
            return False

    def _wait_for_title(self, expected_title: str) -> None:
        """Wait until the checkout title contains the expected page state."""
        self.wait.wait_until_visible(self.TITLE)
        self.wait.wait_until_text_present(self.TITLE, expected_title)

    def _find_visible(self, locator: Locator) -> WebElement:
        """Return a visible element using the framework's explicit wait."""
        return self.wait.wait_until_visible(locator)

    def _find_clickable(self, locator: Locator) -> WebElement:
        """Return an interactable element using the framework's explicit wait."""
        return self.wait.wait_until_clickable(locator)

    def _replace_text(self, locator: Locator, value: str, field_name: str) -> None:
        """Clear a field and enter validated text, wrapping WebDriver failures."""
        if value is None or not str(value).strip():
            raise ValueError(f"{field_name.capitalize()} must not be empty.")

        try:
            field = self._find_visible(locator)
            field.clear()
            field.send_keys(str(value).strip())
            self.logger.debug("Entered checkout %s.", field_name)
        except WebDriverException as error:
            self.logger.exception("Unable to enter checkout %s.", field_name)
            raise RuntimeError(f"Unable to enter checkout {field_name}.") from error

    def _click(self, locator: Locator, element_name: str) -> None:
        """Click a control after waiting for it to become interactable."""
        try:
            self._find_clickable(locator).click()
            self.logger.debug("Clicked %s.", element_name)
        except WebDriverException as error:
            self.logger.exception("Unable to click %s.", element_name)
            raise RuntimeError(f"Unable to click {element_name}.") from error
