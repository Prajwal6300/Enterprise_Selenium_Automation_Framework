"""Production-ready UI Test Suite for SauceDemo Login Functionality.

Validates authentication flows including successful login with standard users,
error handling for locked-out accounts, invalid credentials, and blank inputs.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from src.base.base_test import BaseTest
from src.utils.excel_reader import ExcelReader
from src.utils.logger import get_logger

logger = get_logger("TestLogin")


@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
class TestLogin(BaseTest):
    """Test suite covering authentication workflows on SauceDemo."""

    def test_valid_user_login(self, driver):
        """Verify standard user can log in successfully with valid credentials."""
        logger.info("Executing test_valid_user_login")
        self.init_pages(driver)
        
        # Load test data from Excel
        excel_path = Path("testdata/Login.xlsx")
        data = ExcelReader(excel_path).get_sheet_data("valid_users")[0]
        
        # Execute Page Object action
        self.login_page.login(data["username"], data["password"])
        
        # Assertion
        assert self.home_page.is_loaded(), (
            f"Expected Home Page to load after login, but title/url mismatch. "
            f"Current URL: {driver.current_url}"
        )
        logger.info("test_valid_user_login passed successfully")

    def test_invalid_username_shows_error(self, driver):
        """Verify proper error message is displayed when entering a non-existent username."""
        logger.info("Executing test_invalid_username_shows_error")
        self.init_pages(driver)
        
        self.login_page.login("non_existent_user_123", "secret_sauce")
        
        error_msg = self.login_page.get_error_message()
        assert "Username and password do not match" in error_msg, (
            f"Expected invalid user error message, but got: '{error_msg}'"
        )
        logger.info("test_invalid_username_shows_error passed")

    def test_invalid_password_shows_error(self, driver):
        """Verify proper error message displayed when logging in with invalid password."""
        logger.info("Executing test_invalid_password_shows_error")
        self.init_pages(driver)
        
        excel_path = Path("testdata/Login.xlsx")
        data = ExcelReader(excel_path).get_sheet_data("invalid_users")[0]
        
        self.login_page.login(data["username"], data["password"])
        
        error_msg = self.login_page.get_error_message()
        assert "Username and password do not match" in error_msg, (
            f"Expected invalid credentials error message, but got: '{error_msg}'"
        )
        logger.info("test_invalid_password_shows_error passed successfully")

    def test_empty_username_shows_error(self, driver):
        """Verify validation error when username is empty but password is provided."""
        logger.info("Executing test_empty_username_shows_error")
        self.init_pages(driver)
        
        self.login_page.login("", "secret_sauce")
        
        error_msg = self.login_page.get_error_message()
        assert "Username is required" in error_msg, (
            f"Expected 'Username is required' error, but got: '{error_msg}'"
        )
        logger.info("test_empty_username_shows_error passed")

    def test_empty_password_shows_error(self, driver):
        """Verify validation error when password is empty but username is provided."""
        logger.info("Executing test_empty_password_shows_error")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "")
        
        error_msg = self.login_page.get_error_message()
        assert "Password is required" in error_msg, (
            f"Expected 'Password is required' error, but got: '{error_msg}'"
        )
        logger.info("test_empty_password_shows_error passed")

    def test_locked_out_user_error(self, driver):
        """Verify locked-out user is blocked from logging in with specific error message."""
        logger.info("Executing test_locked_out_user_error")
        self.init_pages(driver)
        
        self.login_page.login("locked_out_user", "secret_sauce")
        
        error_msg = self.login_page.get_error_message()
        assert "Epic sadface: Sorry, this user has been locked out." in error_msg, (
            f"Expected locked out error message, but got: '{error_msg}'"
        )
        logger.info("test_locked_out_user_error passed successfully")

    def test_blank_credentials_error(self, driver):
        """Verify clicking login without entering credentials triggers validation error."""
        logger.info("Executing test_blank_credentials_error")
        self.init_pages(driver)
        
        self.login_page.login("", "")
        
        error_msg = self.login_page.get_error_message()
        assert "Epic sadface: Username is required" in error_msg, (
            f"Expected required username error, but got: '{error_msg}'"
        )
        logger.info("test_blank_credentials_error passed successfully")

    def test_password_field_is_masked(self, driver):
        """Verify that password input field has type='password' to mask sensitive text."""
        logger.info("Executing test_password_field_is_masked")
        self.init_pages(driver)
        
        assert self.login_page.is_password_masked(), (
            "Security validation failed: Password input field must have type='password'"
        )
        logger.info("test_password_field_is_masked passed")

    def test_login_button_state_and_behavior(self, driver):
        """Verify that login button is displayed, enabled, and responsive."""
        logger.info("Executing test_login_button_state_and_behavior")
        self.init_pages(driver)
        
        assert self.login_page.is_login_button_enabled(), (
            "Expected login button to be enabled and clickable on page load"
        )
        logger.info("test_login_button_state_and_behavior passed")

    def test_browser_refresh_preserves_authenticated_session(self, driver):
        """Verify refreshing the browser while logged in retains active user session."""
        logger.info("Executing test_browser_refresh_preserves_authenticated_session")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "User must be logged in before page refresh"
        
        driver.refresh()
        assert self.home_page.is_loaded(), (
            "Session validation failed: User should remain logged in after page refresh"
        )
        assert "inventory.html" in driver.current_url, (
            f"Expected inventory URL after refresh, got: {driver.current_url}"
        )
        logger.info("test_browser_refresh_preserves_authenticated_session passed")

    def test_direct_navigation_to_protected_page_without_login(self, driver):
        """Verify accessing /inventory.html without auth redirects to login with error."""
        logger.info("Executing test_direct_navigation_to_protected_page_without_login")
        self.init_pages(driver)
        
        # Navigate directly to protected inventory URL without logging in
        base_url = self.config.get_base_url().rstrip("/")
        protected_url = f"{base_url}/inventory.html"
        driver.get(protected_url)
        
        assert self.login_page.is_loaded(), (
            "Security check: Direct access to protected page must redirect to login page"
        )
        error_msg = self.login_page.get_error_message()
        assert "You can only access '/inventory.html' when you are logged in" in error_msg, (
            f"Expected protected page error, but got: '{error_msg}'"
        )
        logger.info("test_direct_navigation_to_protected_page_without_login passed")

    def test_invalid_username_and_invalid_password_shows_error(self, driver):
        """Verify proper error message displayed when entering both invalid username and password."""
        logger.info("Executing test_invalid_username_and_invalid_password_shows_error")
        self.init_pages(driver)
        
        self.login_page.login("invalid_user_999", "invalid_pass_888")
        
        error_msg = self.login_page.get_error_message()
        assert "Username and password do not match" in error_msg, (
            f"Expected invalid credentials error message, but got: '{error_msg}'"
        )
        logger.info("test_invalid_username_and_invalid_password_shows_error passed")

    def test_login_error_message_dismissable(self, driver):
        """Verify error message banner disappears when user clicks the error close 'X' button."""
        logger.info("Executing test_login_error_message_dismissable")
        self.init_pages(driver)
        
        self.login_page.login("invalid_user", "invalid_pass")
        assert self.login_page.has_error(), "Error banner must be visible after failed login"
        
        self.login_page.dismiss_error()
        assert not self.login_page.has_error(), "Error banner must be dismissed after clicking close button"
        logger.info("test_login_error_message_dismissable passed")

    def test_login_error_disappears_after_valid_login(self, driver):
        """Verify user can recover from a failed login attempt by re-entering valid credentials."""
        logger.info("Executing test_login_error_disappears_after_valid_login")
        self.init_pages(driver)
        
        # Step 1: Failed attempt
        self.login_page.login("standard_user", "wrong_password")
        assert self.login_page.has_error(), "Error banner should appear on wrong password"
        
        # Step 2: Clear and re-enter valid credentials
        self.login_page.clear_inputs()
        self.login_page.login("standard_user", "secret_sauce")
        
        assert self.home_page.is_loaded(), "User should successfully log in after correcting credentials"
        logger.info("test_login_error_disappears_after_valid_login passed")

    def test_login_multiple_user_roles_excel(self, driver):
        """Verify login functionality across multiple user accounts loaded from Excel dataset."""
        logger.info("Executing test_login_multiple_user_roles_excel")
        self.init_pages(driver)
        
        excel_path = Path("testdata/Login.xlsx")
        users = ExcelReader(excel_path).get_sheet_data("valid_users")
        
        for user in users:
            self.login_page.login(user["username"], user["password"])
            assert self.home_page.is_loaded(), f"User '{user['username']}' failed to log in"
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            self.login_page.open()
            assert self.login_page.is_loaded(), "Must return to login page after reset"
        logger.info("test_login_multiple_user_roles_excel passed for %d users", len(users))

    def test_login_after_logout_succeeds(self, driver):
        """Verify user can successfully log back in after logging out in the same browser session."""
        logger.info("Executing test_login_after_logout_succeeds")
        self.init_pages(driver)
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "First login must succeed"
        
        self.home_page.logout()
        assert self.login_page.is_loaded(), "Logout must return user to login page"
        
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded(), "Second login after logout must succeed"
        logger.info("test_login_after_logout_succeeds passed")

