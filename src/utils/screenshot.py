"""Screenshot utilities for Selenium test evidence."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from src.utils.logger import get_logger


class Screenshot:
    """Capture browser screenshots into the project screenshots folder."""

    ROOT_DIR = Path(__file__).resolve().parents[2]
    SCREENSHOT_DIR = ROOT_DIR / "screenshots"
    FAILURE_DIR = SCREENSHOT_DIR / "failures"
    FILE_EXTENSION = ".png"

    @classmethod
    def capture(cls, driver: WebDriver, test_name: str, failed: bool = True) -> str:
        logger = get_logger(cls.__name__)
        target_dir = cls.FAILURE_DIR if failed else cls.SCREENSHOT_DIR
        target_dir.mkdir(parents=True, exist_ok=True)

        safe_name = cls._sanitize_file_name(test_name)
        timestamp = cls._timestamp()
        screenshot_path = target_dir / f"{safe_name}_{timestamp}{cls.FILE_EXTENSION}"

        try:
            saved = driver.save_screenshot(str(screenshot_path))
            if not saved:
                logger.error("WebDriver returned False while saving screenshot: %s", screenshot_path)
                return ""
            logger.info("Screenshot captured: %s", screenshot_path)
            return str(screenshot_path)
        except Exception as error:
            logger.exception("Failed to capture screenshot for '%s': %s", test_name, error)
            return ""

    @staticmethod
    def _sanitize_file_name(value: str) -> str:
        sanitized = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
        return sanitized.strip("._") or "screenshot"

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
