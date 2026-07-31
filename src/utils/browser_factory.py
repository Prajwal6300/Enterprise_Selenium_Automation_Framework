"""Create Selenium WebDriver instances for local and BrowserStack runs."""

from __future__ import annotations

from typing import Literal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from src.utils.config_reader import ConfigReader


SupportedBrowser = Literal["chrome", "firefox", "edge", "browserstack"]


class BrowserFactory:
    """Factory responsible for creating configured Selenium drivers."""

    def __init__(self, config: ConfigReader, logger) -> None:
        self.config = config
        self.logger = logger
        self.driver_cache = DriverCacheManager(root_dir="drivers")

    def create_driver(self, browser: str | None = None, headless: bool | None = None) -> WebDriver:
        browser_name = self._resolve_browser(browser)
        run_headless = self.config.is_headless() if headless is None else headless
        self.logger.info("Creating WebDriver for browser '%s'", browser_name)

        if browser_name == "chrome":
            driver = self._create_chrome(run_headless)
        elif browser_name == "firefox":
            driver = self._create_firefox(run_headless)
        elif browser_name == "edge":
            driver = self._create_edge(run_headless)
        elif browser_name == "browserstack":
            driver = self._create_browserstack()
        else:
            raise ValueError(f"Unsupported browser '{browser_name}'. Use chrome, firefox, edge, or browserstack.")

        self._configure_driver(driver, browser_name, run_headless)
        return driver

    def _resolve_browser(self, browser: str | None) -> SupportedBrowser:
        browser_name = (browser or self.config.get_browser()).lower().strip()
        if browser_name not in {"chrome", "firefox", "edge", "browserstack"}:
            raise ValueError(f"Unsupported browser '{browser_name}'. Use chrome, firefox, edge, or browserstack.")
        return browser_name  # type: ignore[return-value]

    def _create_chrome(self, headless: bool) -> WebDriver:
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless=new")
        try:
            service = ChromeService(ChromeDriverManager(cache_manager=self.driver_cache).install())
            return webdriver.Chrome(service=service, options=options)
        except Exception as error:
            self.logger.warning("WebDriverManager failed to install Chrome driver (%s). Falling back to Selenium Manager.", error)
            return webdriver.Chrome(options=options)

    def _create_firefox(self, headless: bool) -> WebDriver:
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if headless:
            options.add_argument("--headless")
        try:
            service = FirefoxService(GeckoDriverManager(cache_manager=self.driver_cache).install())
            return webdriver.Firefox(service=service, options=options)
        except Exception as error:
            self.logger.warning("WebDriverManager failed to install Gecko driver (%s). Falling back to Selenium Manager.", error)
            return webdriver.Firefox(options=options)

    def _create_edge(self, headless: bool) -> WebDriver:
        options = EdgeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless=new")
        try:
            service = EdgeService(EdgeChromiumDriverManager(cache_manager=self.driver_cache).install())
            return webdriver.Edge(service=service, options=options)
        except Exception as error:
            self.logger.warning("WebDriverManager failed to install Edge driver (%s). Falling back to Selenium Manager.", error)
            return webdriver.Edge(options=options)

    def _create_browserstack(self) -> WebDriver:
        capabilities = self.config.get_browserstack_capabilities()
        bstack_options = capabilities["bstack:options"]
        if not isinstance(bstack_options, dict):
            raise TypeError("BrowserStack options must be a dictionary.")

        username = str(bstack_options.get("userName", ""))
        access_key = str(bstack_options.get("accessKey", ""))
        if not username or not access_key:
            raise ValueError("BrowserStack credentials must be set in BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY.")

        options = ChromeOptions()
        for capability_name, capability_value in capabilities.items():
            options.set_capability(capability_name, capability_value)

        remote_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
        return webdriver.Remote(command_executor=remote_url, options=options)

    def _configure_driver(self, driver: WebDriver, browser_name: SupportedBrowser, headless: bool) -> None:
        implicit_wait = self.config.get_implicit_wait()
        page_load_timeout = self.config.get_page_load_timeout()
        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)

        if browser_name != "browserstack" and not headless:
            driver.maximize_window()

        self.logger.info(
            "WebDriver ready: browser=%s, headless=%s, implicit_wait=%s, page_load_timeout=%s",
            browser_name,
            headless,
            implicit_wait,
            page_load_timeout,
        )
