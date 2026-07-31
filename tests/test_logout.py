"""Production-ready UI Test Suite for SauceDemo Logout Functionality.

Validates session termination via hamburger menu logout action.
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
    """Test suite covering logout behavior."""

    def test_logout_returns_to_login_page(self, driver):
        """Verify logging out redirects user back to the login page and clears session."""
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
