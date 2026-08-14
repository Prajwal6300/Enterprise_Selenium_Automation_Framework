# Changelog

All notable changes to the **Enterprise Selenium Python Automation Framework** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Complete documentation set** under `docs/`:
  - `architecture.md` — layered architecture, directory-to-layer mapping, runtime flow.
  - `installation.md` — prerequisites, venv setup, dependency installation, optional Allure/Docker/BrowserStack setup.
  - `configuration.md` — `src/config/config.ini` sections, environment variables, precedence, environment switching.
  - `test-execution.md` — every execution mode, marker reference, parallel/retry/timeout options.
  - `test-cases.md` — full source-derived test-case matrix (181 tests).
  - `test-data.md` — Excel/JSON/CSV datasets and loading API.
  - `reporting.md` — dashboard, HTML, JUnit, Allure, JSON telemetry.
  - `browserstack.md`, `docker.md`, `jenkins.md`, `github-actions.md` — integration guides.
  - `troubleshooting.md`, `development-guide.md`, `faq.md` — support and contribution guides.
- **README rewrite**: accurate test count (181), correct config path (`src/config/config.ini`), corrected structure (no `src/pages/base_page.py`), security section, and quick-reference commands.
- **CHANGELOG / CONTRIBUTING refresh** matching the actual implementation and repository state.

### Changed
- Consolidated `docs/` into a single clean, non-duplicating documentation structure (removed the older `test_execution.md`, `browserstack_guide.md`, `ci_cd.md`, and `docker_guide.md` placeholders).
- Corrected documentation claims that did not match the source code (e.g., hardcoded Selenium version badge, nonexistent `config/config.ini`, nonexistent `src/pages/base_page.py`).

---

## [2.5.0-Enterprise] - 2026-07-31

### Added
- **Premium Light Analytics Dashboard**:
  - Redesigned reporting engine generating standalone `reports/dashboard.html`.
  - Inspired by Microsoft Fluent UI, Stripe, Google Material Design 3, GitHub Light, and Notion.
  - Features 6 interactive Chart.js visualizations (Pass vs Fail Doughnut, Execution Timeline Line Chart, Module Distribution Bar Chart, Test Duration Breakdown, Browser Breakdown, and Success Rate Gauge).
  - Searchable, sortable, and paginated test execution table with custom status badges (`Passed`, `Failed`, `Skipped`, `Running`).
  - Interactive Screenshot Viewer Modal and Log Code Viewer Modal with Copy and Download capability.
  - Executive performance panel and 15-item Environment & Metadata panel.
  - Multi-format Export options: PDF, Excel, and CSV table generation.
- **Selenium 4 Fallback Engine**:
  - Enhanced `BrowserFactory` with automatic fallback to native `SeleniumManager` when `WebDriverManager` API encounters network rate limits or memory constraints.
- **Enhanced Test Synchronization**:
  - Added hybrid native/JS click fallbacks in `CheckoutPage` and `HomePage` to eliminate browser execution race conditions.

### Changed
- Refactored `pytest_sessionfinish` hook in `conftest.py` to automatically populate test metadata and render the new light enterprise dashboard.
- Updated `Jenkinsfile` HTML publisher configuration to target `reports/dashboard.html`.
- Updated `report_manager.py` with custom CSS tokens for light theme consistency.

---

## [2.0.0] - 2026-03-15

### Added
- Multi-browser cross-platform support (Chrome, Firefox, Edge, Headless).
- BrowserStack integration via `browserstack.yml` configuration.
- REST API Automation suite using `requests` with status code and schema validation helpers (`APIClient`, `UserAPIService`).
- Database validation layer using SQLAlchemy (`DBUtility`) for UI vs DB record assertions.
- Excel Data-Driven testing integration using OpenPyXL (`ExcelReader`).

---

## [1.0.0] - 2026-01-10

### Added
- Initial framework architecture implementing Page Object Model (POM) for SauceDemo E-Commerce platform.
- Explicit wait synchronization utility (`WaitHelper`).
- Logging infrastructure (`Logger`) and automated failure screenshot utility (`Screenshot`).
- Pytest configuration (`pytest.ini` & `conftest.py`).
- Docker containerization (`Dockerfile` & `docker-compose.yml`).
- CI/CD workflow pipelines for GitHub Actions and Jenkins.
