"""Central configuration reader for the Selenium automation framework."""

from __future__ import annotations

import configparser
import os
from pathlib import Path


class ConfigReader:
    """Read framework settings from config.ini using Python ConfigParser."""

    DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.ini"

    def __init__(self, environment: str | None = None, config_path: str | Path | None = None, env: str | None = None) -> None:
        self.config_path = Path(config_path).resolve() if config_path else self.DEFAULT_CONFIG_PATH
        self.parser = configparser.ConfigParser(interpolation=None)
        self._load_config()
        self.environment = environment or env or self.get("active_environment", section="framework")
        self._validate_section(self.environment)

    def _load_config(self) -> None:
        read_files = self.parser.read(self.config_path)
        if not read_files:
            raise FileNotFoundError(f"Configuration file was not found: {self.config_path}")

    def _validate_section(self, section: str) -> None:
        if not self.parser.has_section(section):
            raise KeyError(f"Configuration section '{section}' was not found in {self.config_path}")

    def _resolve_env_variable(self, value: str) -> str:
        if value.startswith("${") and value.endswith("}"):
            variable_name = value[2:-1]
            return os.getenv(variable_name, "")
        return value

    def get(self, key: str, default: str | None = None, section: str | None = None) -> str:
        active_section = section or self.environment
        self._validate_section(active_section)
        value = self.parser.get(active_section, key, fallback=default)
        if value is None:
            raise KeyError(f"Configuration key '{key}' was not found in section '{active_section}'")
        return self._resolve_env_variable(value.strip())

    def get_int(self, key: str, default: int | None = None, section: str | None = None) -> int:
        value = self.get(key, None if default is None else str(default), section)
        return int(value)

    def get_bool(self, key: str, default: bool | None = None, section: str | None = None) -> bool:
        value = self.get(key, None if default is None else str(default), section).lower()
        if value not in {"true", "false", "1", "0", "yes", "no", "on", "off"}:
            raise ValueError(f"Configuration key '{key}' must be a boolean value, got '{value}'")
        return value in {"true", "1", "yes", "on"}

    def get_browser(self) -> str:
        return self.get("browser", section="framework").lower()

    def get_base_url(self) -> str:
        return self.get("base_url")

    def get_username(self) -> str:
        return self.get("username")

    def get_password(self) -> str:
        return self.get("password")

    def is_headless(self) -> bool:
        browser = self.get_browser()
        browser_headless = self.get_bool("headless", section=browser) if self.parser.has_section(browser) else False
        return self.get_bool("headless", default=browser_headless, section="framework")

    def get_timeout(self) -> int:
        return self.get_int("timeout")

    def get_implicit_wait(self) -> int:
        return self.get_int("implicit_wait", section="timeouts")

    def get_explicit_wait(self) -> int:
        return self.get_int("explicit_wait", section="timeouts")

    def get_page_load_timeout(self) -> int:
        return self.get_int("page_load_timeout", section="timeouts")

    def is_browserstack_enabled(self) -> bool:
        return self.get_browser() == "browserstack" or self.get_bool("enabled", section="browserstack")

    def get_browserstack_capabilities(self) -> dict[str, object]:
        return {
            "browserName": self.get("browser_name", section="browserstack"),
            "browserVersion": self.get("browser_version", section="browserstack"),
            "bstack:options": {
                "userName": self.get("username", section="browserstack"),
                "accessKey": self.get("access_key", section="browserstack"),
                "projectName": self.get("project_name", section="browserstack"),
                "buildName": self.get("build_name", section="browserstack"),
                "sessionName": self.get("session_name", section="browserstack"),
                "os": self.get("os", section="browserstack"),
                "osVersion": self.get("os_version", section="browserstack"),
                "local": self.get_bool("local", section="browserstack"),
                "seleniumVersion": self.get("selenium_version", section="browserstack"),
            },
        }
