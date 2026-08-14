"""Page Object Model class for the SauceDemo login page."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.logger import get_logger
from src.utils.wait_helper import Locator, WaitHelper


class LoginPage:
    """Encapsulate login page locators, waits, and user actions."""

    USERNAME_INPUT: Locator = (By.ID, "user-name")
    PASSWORD_INPUT: Locator = (By.ID, "password")
    LOGIN_BUTTON: Locator = (By.ID, "login-button")
    ERROR_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON: Locator = (By.CLASS_NAME, "error-button")
    LOGIN_LOGO: Locator = (By.CLASS_NAME, "login_logo")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url: str = "https://www.saucedemo.com/") -> None:
        self.driver.get(url)
        self.wait.wait_until_visible(self.LOGIN_LOGO)
        self.logger.info("Navigated to login page: %s", url)

    def is_loaded(self) -> bool:
        try:
            return self._find_visible(self.LOGIN_LOGO).is_displayed()
        except TimeoutException:
            self.logger.warning("Login page did not load within the configured timeout.")
            return False

    def enter_username(self, username: str) -> None:
        self._type(self.USERNAME_INPUT, username, "username")

    def enter_password(self, password: str) -> None:
        self._type(self.PASSWORD_INPUT, password, "password")

    def click_login(self) -> None:
        try:
            btn = self._find_clickable(self.LOGIN_BUTTON)
            btn.click()
            # If still on login page and not errored, ensure form is submitted
            if "inventory.html" not in self.driver.current_url and not self.has_error():
                self.driver.execute_script(
                    """
                    let form = document.querySelector('form');
                    if (form && form.requestSubmit) {
                        form.requestSubmit();
                    }
                    """
                )
            self.logger.debug("Clicked login button.")
        except WebDriverException as error:
            self.logger.exception("Unable to click login button.")
            raise RuntimeError("Unable to click login button.") from error

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        try:
            return self._find_visible(self.ERROR_MESSAGE).text.strip()
        except TimeoutException as error:
            self.logger.exception("Login error message was not visible.")
            raise AssertionError("Expected login error message was not visible.") from error

    def is_password_masked(self) -> bool:
        """Verify whether password input field masks entered text (type='password')."""
        try:
            input_type = self._find_visible(self.PASSWORD_INPUT).get_attribute("type")
            return input_type == "password"
        except Exception as error:
            self.logger.warning("Could not determine password input masking type: %s", error)
            return False

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled and interactable."""
        try:
            return self._find_visible(self.LOGIN_BUTTON).is_enabled()
        except Exception:
            return False

    def clear_inputs(self) -> None:
        """Clear username and password input fields."""
        try:
            self._find_visible(self.USERNAME_INPUT).clear()
            self._find_visible(self.PASSWORD_INPUT).clear()
        except Exception as error:
            self.logger.warning("Failed to clear login fields: %s", error)

    def has_error(self) -> bool:
        """Check if an error alert is currently displayed on login page."""
        try:
            return self._find_visible(self.ERROR_MESSAGE).is_displayed()
        except TimeoutException:
            return False

    def dismiss_error(self) -> None:
        """Dismiss the login error banner by clicking the error close button."""
        try:
            self._click(self.ERROR_BUTTON, "error dismiss button")
        except Exception as error:
            self.logger.warning("Failed to click error dismiss button: %s", error)

    def _find_visible(self, locator: Locator) -> WebElement:
        return self.wait.wait_until_visible(locator)

    def _find_clickable(self, locator: Locator) -> WebElement:
        return self.wait.wait_until_clickable(locator)

    def _type(self, locator: Locator, value: str, field_name: str) -> None:
        try:
            element = self._find_clickable(locator)
            element.click()
            element.clear()
            if value is not None and str(value) != "":
                element.send_keys(str(value))
                if element.get_attribute("value") != str(value):
                    self.driver.execute_script(
                        """
                        let elem = arguments[0];
                        let proto = Object.getPrototypeOf(elem);
                        let desc = Object.getOwnPropertyDescriptor(proto, 'value');
                        if (desc && desc.set) {
                            desc.set.call(elem, arguments[1]);
                        } else {
                            elem.value = arguments[1];
                        }
                        elem.dispatchEvent(new Event('input', { bubbles: true }));
                        elem.dispatchEvent(new Event('change', { bubbles: true }));
                        """,
                        element,
                        str(value),
                    )
            self.logger.debug("Entered value into %s field.", field_name)
        except WebDriverException as error:
            self.logger.exception("Unable to enter value into %s field.", field_name)
            raise RuntimeError(f"Unable to enter value into {field_name} field.") from error

    def _click(self, locator: Locator, element_name: str) -> None:
        try:
            self._find_clickable(locator).click()
            self.logger.debug("Clicked %s.", element_name)
        except WebDriverException as error:
            self.logger.exception("Unable to click %s.", element_name)
            raise RuntimeError(f"Unable to click {element_name}.") from error


