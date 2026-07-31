"""Base pytest class that owns browser setup and teardown for UI tests."""

from __future__ import annotations

from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.product_page import ProductPage
from src.utils.browser_factory import BrowserFactory
from src.utils.config_reader import ConfigReader
from src.utils.logger import get_logger
from src.utils.screenshot import Screenshot


class BaseTest:
    """Base class for Selenium tests that need a configured browser."""

    driver: WebDriver
    config: ConfigReader

    @pytest.fixture(scope="function")
    def driver(self, request: pytest.FixtureRequest, config: ConfigReader) -> Generator[WebDriver, None, None]:
        self.config = config
        self.logger = get_logger(request.node.name)
        browser = request.config.getoption("--browser") or self.config.get_browser()
        headless = request.config.getoption("--headless") or self.config.is_headless()

        self.logger.info("Starting setup for test '%s'", request.node.name)
        factory = BrowserFactory(config=self.config, logger=self.logger)
        self.driver = factory.create_driver(browser=browser, headless=headless)
        request.node.driver = self.driver

        base_url = self.config.get_base_url()
        self.logger.info("Opening application URL: %s", base_url)
        self.driver.get(base_url)

        self.init_pages(self.driver)
        yield self.driver

        self.logger.info("Starting teardown for test '%s'", request.node.name)
        self.driver.quit()
        self.logger.info("Browser closed for test '%s'", request.node.name)

    def init_pages(self, driver: WebDriver) -> None:
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)

    def capture_screenshot(self, name: str) -> str:
        if not hasattr(self, "driver"):
            raise RuntimeError("Cannot capture screenshot because WebDriver is not initialized.")
        return Screenshot.capture(self.driver, name)
