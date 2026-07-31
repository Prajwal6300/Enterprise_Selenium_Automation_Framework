"""Global pytest configuration, WebDriver lifecycle hooks, and Enterprise Reporting integrations."""

from __future__ import annotations

import datetime
import os
from pathlib import Path
import time
from typing import Any, Generator, List, Dict

import pytest

from src.reports.enterprise_dashboard import EnterpriseDashboardBuilder
from src.reports.report_manager import ReportManager
from src.utils.browser_factory import BrowserFactory
from src.utils.config_reader import ConfigReader
from src.utils.logger import get_logger
from src.utils.screenshot import Screenshot

ROOT_DIR = Path(__file__).resolve().parent
SESSION_START_TIME = time.time()
SESSION_TEST_RESULTS: List[Dict[str, Any]] = []


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register command-line options used by local and CI executions."""
    parser.addoption("--browser", action="store", default=None, help="chrome, firefox, edge, or browserstack")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--env", action="store", default="qa", help="Environment section from config.ini")


@pytest.fixture(scope="session")
def config(request: pytest.FixtureRequest) -> ConfigReader:
    """Return a config reader for the selected environment."""
    return ConfigReader(env=request.config.getoption("--env"))


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest, config: ConfigReader) -> Generator:
    """Create and tear down a WebDriver instance for every test."""
    logger = get_logger(request.node.name)
    browser = request.config.getoption("--browser") or config.get("browser")
    headless = request.config.getoption("--headless") or config.get_bool("headless")

    factory = BrowserFactory(config=config, logger=logger)
    web_driver = factory.create_driver(browser=browser, headless=headless)
    web_driver.maximize_window()
    web_driver.get(config.get("base_url"))

    request.node.driver = web_driver
    logger.info("Started test '%s' on browser '%s'", request.node.name, browser)
    yield web_driver

    logger.info("Closing browser for test '%s'", request.node.name)
    web_driver.quit()


def pytest_html_report_title(report: Any) -> None:
    """Customize pytest-html report title header."""
    report.title = "Enterprise Test Automation Execution Dashboard"


def pytest_configure(config: pytest.Config) -> None:
    """Populate pytest metadata dictionary for report headers."""
    if hasattr(config, "_metadata"):
        env_arg = config.getoption("--env") if hasattr(config, "getoption") else "qa"
        browser_arg = config.getoption("--browser") if hasattr(config, "getoption") else "chrome"
        sys_meta = ReportManager.get_system_metadata(env=env_arg or "qa", browser=browser_arg or "chrome")
        config._metadata.update(sys_meta)


def pytest_html_results_summary(prefix: list, summary: Any, postfix: list) -> None:
    """Inject custom KPI summary cards and metadata table into HTML report header."""
    css_content = ReportManager.generate_dashboard_css()
    script_content = ReportManager.generate_modal_script()

    env_name = "QA"
    meta = ReportManager.get_system_metadata(env=env_name, browser="Chrome")

    kpi_html = f"""
    {css_content}
    {script_content}
    <div class="dashboard-header">
        <div class="dashboard-title">
            <h1>🚀 Enterprise Test Automation Dashboard</h1>
            <span style="color: #94a3b8; font-weight: 600;">Execution Date: {meta['Execution Date']}</span>
        </div>
        
        <div class="kpi-cards-grid">
            <div class="kpi-card kpi-total">
                <div class="kpi-label">Project</div>
                <div style="font-size: 16px; font-weight: 700; color: #f8fafc; margin-top: 6px;">SauceDemo E-Commerce</div>
            </div>
            <div class="kpi-card kpi-passed">
                <div class="kpi-label">Environment</div>
                <div style="font-size: 18px; font-weight: 700; color: #10b981; margin-top: 6px;">{meta['Environment']}</div>
            </div>
            <div class="kpi-card kpi-rate">
                <div class="kpi-label">Target Browser</div>
                <div style="font-size: 18px; font-weight: 700; color: #34d399; margin-top: 6px;">{meta['Target Browser']}</div>
            </div>
            <div class="kpi-card kpi-skipped">
                <div class="kpi-label">Python Version</div>
                <div style="font-size: 18px; font-weight: 700; color: #f59e0b; margin-top: 6px;">{meta['Python Version']}</div>
            </div>
            <div class="kpi-card kpi-failed">
                <div class="kpi-label">Framework</div>
                <div style="font-size: 16px; font-weight: 700; color: #f43f5e; margin-top: 6px;">{meta['Framework Version']}</div>
            </div>
        </div>

        <div class="meta-table-container">
            <table class="meta-table">
                <thead><tr><th colspan="2">💻 Environment & System Metadata</th></tr></thead>
                <tbody>
                    <tr><td><b>Host Machine</b></td><td>{meta['Host Machine']}</td></tr>
                    <tr><td><b>Operating System</b></td><td>{meta['Operating System']}</td></tr>
                    <tr><td><b>Execution User</b></td><td>{meta['Execution User']}</td></tr>
                    <tr><td><b>Selenium Version</b></td><td>{meta['Selenium Version']}</td></tr>
                </tbody>
            </table>
            <table class="meta-table">
                <thead><tr><th colspan="2">📦 Version Control & CI/CD Info</th></tr></thead>
                <tbody>
                    <tr><td><b>Git Branch</b></td><td>{meta['Git Branch']}</td></tr>
                    <tr><td><b>Git Commit</b></td><td>{meta['Git Commit Hash']}</td></tr>
                    <tr><td><b>CI System</b></td><td>{meta.get('CI System', 'Local Run')}</td></tr>
                    <tr><td><b>Cloud Grid</b></td><td>{meta.get('Cloud Grid', 'Local WebDrivers')}</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    """
    prefix.append(kpi_html)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Attach failure screenshot, URL, browser logs, and record results for Enterprise Dashboard."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call":
        return

    driver_obj = getattr(item, "driver", None)
    screenshot_uri = ""

    if report.failed and driver_obj is not None:
        screenshot_path = Screenshot.capture(driver_obj, item.name)
        if screenshot_path:
            screenshot_uri = ReportManager.get_base64_image(screenshot_path)
            extra = getattr(report, "extras", [])
            try:
                from pytest_html import extras
                extra.append(extras.html(f'<div><b>Failure Screenshot:</b><br/><img src="{screenshot_uri}" style="max-width:350px; border-radius:8px; border:2px solid #ef4444;" /></div>'))
                report.extras = extra
            except Exception:
                pass

            try:
                import allure
                allure.attach.file(screenshot_path, name=item.name, attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass

    # Extract categories from pytest markers
    categories = [mark.name for mark in item.iter_markers()]
    if not categories:
        categories = ["ui"]

    file_path = str(item.fspath)
    try:
        file_path = os.path.relpath(file_path, str(ROOT_DIR))
    except Exception:
        pass

    # Collect result data for Enterprise Dashboard Builder
    result_entry = {
        "name": item.name,
        "file": file_path,
        "status": report.outcome,
        "duration": report.duration,
        "categories": categories,
        "screenshot_uri": screenshot_uri,
        "error_message": str(report.longrepr) if report.failed else "",
    }
    SESSION_TEST_RESULTS.append(result_entry)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Generate standalone Grafana/Datadog-style Enterprise Analytics Dashboard HTML report."""
    session_duration = time.time() - SESSION_START_TIME
    builder = EnterpriseDashboardBuilder(output_path="reports/dashboard.html")
    builder.build_dashboard(
        test_results=SESSION_TEST_RESULTS,
        session_duration=session_duration,
        env="QA",
        browser="Chrome"
    )
