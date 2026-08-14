"""Production-ready UI Test Suite for SauceDemo Logout & Session Management.

Validates:
1. Successful logout via menu action
2. Login page loaded after logout
3. Protected inventory page redirected after session termination
4. Protected cart page redirected after session termination
5. Protected checkout page redirected after session termination
6. Browser back button behavior after logout
7. Page refresh after logout stays on login
8. Re-authenticating after logout in the same browser session
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestLogout")


@pytest.mark.regression
@pytest.mark.ui
class TestLogout(BaseTest):
    """Test suite covering logout behavior and session termination security."""

    def test_logout_returns_to_login_page(self, driver):
        """1. Verify logging out redirects user back to the login page and clears session."""
        logger.info("Executing test_logout_returns_to_login_page")
        self.init_pages(driver)
        
        login_data = ExcelReader(Path("testdata/Login.xlsx")).get_sheet_data("valid_users")[0]

        self.login_page.login(login_data["username"], login_data["password"])
        assert self.home_page.is_loaded(), "Home page should be displayed after successful login"

        self.home_page.logout()

        assert self.login_page.is_loaded(), (
            f"Expected login page to be loaded after logout, but current URL is {driver.current_url}"
        )
        logger.info("test_logout_returns_to_login_page passed")

    def test_protected_page_cannot_be_accessed_after_logout(self, driver):
        """2. Verify attempting to navigate back to /inventory.html after logout redirects to login with error."""
        logger.info("Executing test_protected_page_cannot_be_accessed_after_logout")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "Must log in first"
        
        self.home_page.logout()
        assert self.login_page.is_loaded(), "Must be on login page after logout"
        
        # Attempt direct navigation to inventory page
        base_url = self.config.get_base_url().rstrip("/")
        driver.get(f"{base_url}/inventory.html")
        
        assert self.login_page.is_loaded(), "Direct access after logout must remain on login page"
        error_msg = self.login_page.get_error_message()
        assert "You can only access '/inventory.html' when you are logged in" in error_msg, (
            f"Expected session termination message, got: {error_msg}"
        )
        logger.info("test_protected_page_cannot_be_accessed_after_logout passed")

    def test_protected_cart_page_cannot_be_accessed_after_logout(self, driver):
        """3. Verify navigating to /cart.html after logout redirects to login page with auth error."""
        logger.info("Executing test_protected_cart_page_cannot_be_accessed_after_logout")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.logout()

        base_url = self.config.get_base_url().rstrip("/")
        driver.get(f"{base_url}/cart.html")

        assert self.login_page.is_loaded(), "Direct cart access after logout must redirect to login"
        error_msg = self.login_page.get_error_message()
        assert "You can only access '/cart.html' when you are logged in" in error_msg
        logger.info("test_protected_cart_page_cannot_be_accessed_after_logout passed")

    def test_protected_checkout_page_cannot_be_accessed_after_logout(self, driver):
        """4. Verify navigating to /checkout-step-one.html after logout redirects to login with error."""
        logger.info("Executing test_protected_checkout_page_cannot_be_accessed_after_logout")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.logout()

        base_url = self.config.get_base_url().rstrip("/")
        driver.get(f"{base_url}/checkout-step-one.html")

        assert self.login_page.is_loaded(), "Direct checkout access after logout must redirect to login"
        error_msg = self.login_page.get_error_message()
        assert "You can only access '/checkout-step-one.html' when you are logged in" in error_msg
        logger.info("test_protected_checkout_page_cannot_be_accessed_after_logout passed")

    def test_browser_back_button_after_logout(self, driver):
        """5. Verify pressing browser Back after logout does not reveal authenticated user data."""
        logger.info("Executing test_browser_back_button_after_logout")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "Login must succeed"
        
        self.home_page.logout()
        assert self.login_page.is_loaded(), "Logout must succeed"
        
        driver.back()
        
        # SauceDemo shows login page with error when navigating back
        assert self.login_page.is_loaded() or not self.home_page.is_loaded(), (
            "Security vulnerability: Browser back button should not re-authenticate or display inventory without session"
        )
        logger.info("test_browser_back_button_after_logout passed")

    def test_page_refresh_after_logout_stays_on_login(self, driver):
        """6. Verify refreshing the page after logout stays safely on login page."""
        logger.info("Executing test_page_refresh_after_logout_stays_on_login")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        self.home_page.logout()
        assert self.login_page.is_loaded(), "Must be on login page"
        
        driver.refresh()
        assert self.login_page.is_loaded(), "Must still be on login page after refresh"
        logger.info("test_page_refresh_after_logout_stays_on_login passed")

    def test_login_again_after_logout_in_same_session(self, driver):
        """7. Verify user can successfully log back in immediately after logout in the same browser."""
        logger.info("Executing test_login_again_after_logout_in_same_session")
        self.init_pages(driver)

        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded()

        self.home_page.logout()
        assert self.login_page.is_loaded()

        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded()
        assert self.home_page.get_product_count() == 6
        logger.info("test_login_again_after_logout_in_same_session passed")
