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
