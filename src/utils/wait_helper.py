"""Reusable Selenium wait helpers for stable UI synchronization."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.config_reader import ConfigReader


Locator = tuple[str, str]


class WaitHelper:
    """Central place for implicit, explicit, and fluent waits."""

    DEFAULT_POLL_FREQUENCY = 0.5
    DEFAULT_IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

    def __init__(self, driver: WebDriver, timeout: int | None = None, poll_frequency: float | None = None) -> None:
        self.driver = driver
        self.config = ConfigReader()
        self.timeout = timeout if timeout is not None else self.config.get_explicit_wait()
        self.poll_frequency = poll_frequency if poll_frequency is not None else self.DEFAULT_POLL_FREQUENCY

    def set_implicit_wait(self, timeout: int | None = None) -> None:
        wait_time = timeout if timeout is not None else self.config.get_implicit_wait()
        self.driver.implicitly_wait(wait_time)

    def explicit_wait(self, timeout: int | None = None) -> WebDriverWait:
        wait_time = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, wait_time)

    def fluent_wait(
        self,
        condition: Callable[[WebDriver], Any],
        timeout: int | None = None,
        poll_frequency: float | None = None,
        ignored_exceptions: tuple[type[Exception], ...] | None = None,
        message: str = "",
    ) -> Any:
        wait_time = timeout if timeout is not None else self.timeout
        polling = poll_frequency if poll_frequency is not None else self.poll_frequency
        exceptions = ignored_exceptions if ignored_exceptions is not None else self.DEFAULT_IGNORED_EXCEPTIONS
        return WebDriverWait(
            self.driver,
            wait_time,
            poll_frequency=polling,
            ignored_exceptions=exceptions,
        ).until(condition, message)

    def wait_until_clickable(self, locator: Locator, timeout: int | None = None) -> WebElement:
        try:
            return self.explicit_wait(timeout).until(ec.element_to_be_clickable(locator))
        except TimeoutException as error:
            raise TimeoutException(f"Element was not clickable within {timeout or self.timeout} seconds: {locator}") from error

    def wait_until_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        try:
            return self.explicit_wait(timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException as error:
            raise TimeoutException(f"Element was not visible within {timeout or self.timeout} seconds: {locator}") from error

    def wait_until_present(self, locator: Locator, timeout: int | None = None) -> WebElement:
        try:
            return self.explicit_wait(timeout).until(ec.presence_of_element_located(locator))
        except TimeoutException as error:
            raise TimeoutException(f"Element was not present within {timeout or self.timeout} seconds: {locator}") from error

    def wait_until_all_visible(self, locator: Locator, timeout: int | None = None) -> list[WebElement]:
        try:
            return self.explicit_wait(timeout).until(ec.visibility_of_all_elements_located(locator))
        except TimeoutException as error:
            raise TimeoutException(f"Elements were not visible within {timeout or self.timeout} seconds: {locator}") from error

    def wait_until_url_contains(self, fragment: str, timeout: int | None = None) -> bool:
        try:
            return self.explicit_wait(timeout).until(ec.url_contains(fragment))
        except TimeoutException as error:
            raise TimeoutException(f"URL did not contain '{fragment}' within {timeout or self.timeout} seconds") from error

    def wait_until_text_present(self, locator: Locator, text: str, timeout: int | None = None) -> bool:
        try:
            return self.explicit_wait(timeout).until(ec.text_to_be_present_in_element(locator, text))
        except TimeoutException as error:
            raise TimeoutException(
                f"Text '{text}' was not present within {timeout or self.timeout} seconds: {locator}"
            ) from error

    def clickable(self, locator: Locator) -> WebElement:
        return self.wait_until_clickable(locator)

    def visible(self, locator: Locator) -> WebElement:
        return self.wait_until_visible(locator)

    def present(self, locator: Locator) -> WebElement:
        return self.wait_until_present(locator)

    def all_visible(self, locator: Locator) -> list[WebElement]:
        return self.wait_until_all_visible(locator)

    def url_contains(self, fragment: str) -> bool:
        return self.wait_until_url_contains(fragment)

    def text_to_be(self, locator: Locator, text: str) -> bool:
        return self.wait_until_text_present(locator, text)
