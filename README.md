# Enterprise Selenium Python Automation Framework

<<<<<<< HEAD
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/selenium-v4.28.1-green.svg)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-v9.1.1-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20%7C%20Jenkins-orange.svg)](.github/workflows/regression.yml)
[![Cloud Grid](https://img.shields.io/badge/Cloud%20Grid-BrowserStack-informational.svg)](browserstack.yml)   

An **enterprise-grade, scalable, and modular test automation framework** built using **Python**, **Selenium WebDriver**, **pytest**, and the **Page Object Model (POM)** pattern.

This framework is designed for production Web UI testing, REST API automation, database data-integrity validation, cross-browser cloud execution (BrowserStack), Docker containerization, and continuous integration (Jenkins & GitHub Actions). 
=======
A production-grade **web UI, REST API, and database** test automation framework built on **Selenium WebDriver** and **pytest**, covering the **SauceDemo** e-commerce demo application across Chrome, Firefox, Edge, and BrowserStack.

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green.svg)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-9.x-yellow.svg)](https://docs.pytest.org/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20%7C%20Jenkins-orange.svg)](.github/workflows/regression.yml)
[![Cloud Grid](https://img.shields.io/badge/Cloud%20Grid-BrowserStack-informational.svg)](browserstack.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
>>>>>>> 8be0472 (Finalize enterprise Selenium automation framework)

---

## Table of Contents

1. [Project Overview](#-project-overview)
2. [Why This Framework Exists](#-why-this-framework-exists)
3. [Key Features](#-key-features)
4. [Architecture Overview](#-architecture-overview)
5. [Technology Stack](#-technology-stack)
6. [Project Structure](#-project-structure)
7. [Test Modules](#-test-modules)
8. [Number of Implemented Tests](#-number-of-implemented-tests)
9. [Test-Case Summary](#-test-case-summary)
10. [Installation](#-installation)
11. [Virtual Environment Setup](#-virtual-environment-setup)
12. [Configuration](#-configuration)
13. [Test Data](#-test-data)
14. [Running Tests](#-running-tests)
15. [Browser Selection](#-browser-selection)
16. [Headless Execution](#-headless-execution)
17. [Parallel Execution](#-parallel-execution)
18. [Retry Execution](#-retry-execution)
19. [Smoke Tests](#-smoke-tests)
20. [Regression Tests](#-regression-tests)
21. [API Tests](#-api-tests)
22. [Database Tests](#-database-tests)
23. [HTML Reports](#-html-reports)
24. [Enterprise Dashboard](#-enterprise-dashboard)
25. [Allure](#-allure)
26. [Screenshots](#-screenshots)
27. [Logging](#-logging)
28. [BrowserStack](#-browserstack)
29. [Docker](#-docker)
30. [Jenkins](#-jenkins)
31. [GitHub Actions](#-github-actions)
32. [Troubleshooting](#-troubleshooting)
33. [Security](#-security)
34. [Development](#-development)
35. [Contribution](#-contribution)
36. [License](#-license)

---

## 1. Project Overview

This project is an **enterprise-style test automation framework** that automates the **SauceDemo** web application and validates supporting REST APIs and database records.

It is designed for:

<<<<<<< HEAD
    subgraph "Page Object Model (POM)"
        J[LoginPage]
        K[HomePage]
        L[ProductPage]
        M[CartPage]
        N[CheckoutPage]
    end   
=======
- **QA / SDET engineers** who need a reusable, well-structured Selenium + pytest framework.
- **Teams** that must verify web UI behavior, REST API contracts, and database integrity in a single pipeline.
- **Developers and hiring managers** evaluating a production-shaped Python automation codebase.
>>>>>>> 8be0472 (Finalize enterprise Selenium automation framework)

It solves the common problem of ad-hoc, throwaway test scripts by providing:

- A **Page Object Model (POM)** with all locators encapsulated in dedicated page classes.
- **Deterministic synchronization** with explicit waits (zero hardcoded `time.sleep()`).
- **Multi-format test data** (Excel, JSON, CSV) with a unified `DataProvider`.
- **REST API** and **database** validation layers alongside Selenium UI tests.
- **Enterprise reporting**: HTML, JUnit XML, Allure, a standalone analytics dashboard, and normalized JSON telemetry.
- **CI/CD integration** for GitHub Actions, Jenkins, Docker, and BrowserStack.

The framework targets **SauceDemo only**. It is not a generic cross-site automation tool — see the [Configuration Guide](docs/configuration.md) for the documented limitation around changing the target URL.

---

## 2. Why This Framework Exists

- Most Selenium projects hardcode sleeps, locators inside tests, and credentials in source files. This framework centralizes waits, locators, and secrets.
- Teams need one place to run UI, API, and database checks with consistent, machine-readable results.
- Test results must be understandable by engineers **and** managers — hence the standalone dashboard, JUnit XML for CI, and JSON telemetry for analytics.

---

## 3. Key Features

- **181 automated tests** across UI, API, database, E2E, data-driven, negative, cross-browser, and regression suites.
- **Page Object Model**: locators and actions encapsulated in `src/pages/`.
- **Explicit-wait synchronization** via `WaitHelper` (no `time.sleep()` anywhere in the codebase).
- **Multi-browser support**: Chrome, Firefox, Edge — local headless and headed modes.
- **BrowserStack** cloud execution through `--browser=browserstack` and `browserstack.yml`.
- **REST API testing** against the public JSONPlaceholder API (`https://jsonplaceholder.typicode.com`) with status-code, schema, header, and SLA assertions.
- **Database validation** using SQLAlchemy against an in-memory SQLite catalog (MySQL/PostgreSQL dialects supported by `DBUtility`).
- **Data-driven testing** from Excel (`.xlsx`), JSON, and CSV via `DataProvider` + `ExcelReader`.
- **Reports** generated automatically on every run:
  - Standalone analytics dashboard (`reports/dashboard.html`)
  - Self-contained pytest-html report (`reports/html/report.html`)
  - JUnit XML (`reports/junit/results.xml`)
  - Allure telemetry (`reports/allure-results/`)
  - Normalized JSON execution telemetry (`reports/executions/EXEC-*.json`)
- **Automatic failure screenshots** embedded into the HTML report and saved to `screenshots/failures/`.
- **Centralized logging** to `logs/framework.log` and console.
- **CI/CD**: GitHub Actions workflow, Jenkins declarative pipeline, Docker image, and docker-compose.

---

## 4. Architecture Overview

The framework follows a layered architecture. Tests depend only on page objects and services; page objects depend on utilities; utilities depend on configuration.

```text
Test Runner (pytest)
        │
        ▼
Pytest Fixtures & Hooks (conftest.py, BaseTest)
        │
        ▼
Browser Factory (BrowserFactory) ──► Selenium WebDriver
        │                                  │
        ▼                                  ▼
Page Objects (src/pages) ─────────────────► SauceDemo UI
        │
        ├── WaitHelper ──── explicit / fluent waits
        ├── Logger ──────── console + file logging
        ├── Screenshot ──── failure evidence
        │
        ├── APIClient / UserAPIService ──── REST API layer
        ├── DBUtility ───────────────────── Database layer
        ├── ExcelReader / DataProvider ──── Test data layer
        │
        ▼
Reporting (pytest-html, JUnit XML, Allure, EnterpriseDashboardBuilder, JSONExporter)
```

See [docs/architecture.md](docs/architecture.md) for the full layer-by-layer explanation, including a Mermaid diagram.

---

## 5. Technology Stack

| Area | Technology |
|------|-----------|
| Language | Python 3.10+ (tested on 3.13.1) |
| Test runner | pytest 9.x (installed 9.1.1) |
| Browser automation | Selenium WebDriver 4.x (installed 4.46.0) |
| Driver management | webdriver-manager 4.x + Selenium Manager fallback |
| Parallel execution | pytest-xdist (3.8.0) |
| Retry engine | pytest-rerunfailures (16.4) |
| Timeout control | pytest-timeout (2.4.0) |
| HTML reporting | pytest-html (4.2.0) |
| Allure reporting | allure-pytest (2.16.0) |
| Test data | openpyxl (3.1.5), pandas (3.0.5), PyYAML (6.0.3) |
| API testing | requests (2.34.2) |
| Database | SQLAlchemy (2.0.51), PyMySQL (1.2.0), SQLite (built-in) |
| Environment | python-dotenv (1.2.2) |
| Cloud grid | BrowserStack (`browserstack-local` 1.2.15) |

> Versions shown are those verified during development. `requirements.txt` declares minimum versions (`>=`), so newer compatible versions install cleanly.

---

## 6. Project Structure

```text
Enterprise_Selenium_Python_Automation_Framework/
├── .github/
│   └── workflows/
│       └── regression.yml        # GitHub Actions CI pipeline
├── browserstack.yml              # BrowserStack cloud configuration
├── ci/                           # CI helper folders (placeholder)
├── conftest.py                   # Pytest fixtures, hooks, reporting triggers
├── docker-compose.yml            # Compose orchestration for the test container
├── Dockerfile                    # Selenium test container definition
├── docs/                         # Architecture, execution & integration guides
├── drivers/                      # Local WebDriver cache (gitignored)
├── Jenkinsfile                   # Jenkins declarative pipeline
├── logs/                         # Runtime framework logs (gitignored)
├── pytest.ini                    # Pytest configuration & markers
├── README.md                     # This file
├── reports/                      # All generated reports (gitignored)
├── requirements.txt              # Python dependencies
├── screenshots/                  # Failure screenshots (gitignored)
├── scripts/
│   └── sync_results.py           # Seed/ingest execution telemetry utility
├── src/
<<<<<<< HEAD
│   ├── base/
│   │   └── base_test.py            # Base test initialization fixture class
│   ├── config/
│   │   ├── config.ini              # Multi-environment config (QA/UAT/PROD)
│   │   └── config_reader.py        # Configuration parser
│   ├── pages/                      # Page Object Model (POM) classes
│   │   ├── login_page.py           # SauceDemo Login POM
│   │   ├── home_page.py            # SauceDemo Products Inventory POM
│   │   ├── product_page.py         # Product Detail POM
│   │   ├── cart_page.py            # Cart POM
│   │   └── checkout_page.py        # Checkout POM
│   ├── reports/
│   │   ├── enterprise_dashboard.py # Standalone Light HTML Dashboard Builder
│   │   └── report_manager.py       # Metadata & Pytest-HTML injection manager
│   ├── services/                   # REST API Automation Layer
│   │   ├── api_client.py           # HTTP Client (GET/POST/PUT/DELETE)
│   │   └── user_api.py             # User API Service Object
│   └── utils/                      # Core Utility Helpers
│       ├── browser_factory.py      # Cross-browser & BrowserStack factory
│       ├── data_provider.py        # Multi-format data parser
│       ├── db_utility.py           # MySQL/PostgreSQL/SQLite DB connector & verification
│       ├── email_reporter.py       # Automated SMTP HTML report dispatcher
│       ├── excel_reader.py         # OpenPyXL Excel data reader
│       ├── logger.py               # Enterprise rotating logger
│       ├── screenshot.py           # Failure screenshot utility
│       ├── soft_assert.py          # Non-blocking multi-step soft assertions
│       ├── test_data_generator.py  # Synthetic test data generator
│       └── wait_helper.py          # Explicit wait synchronization wrappers
├── testdata/
│   ├── Login.xlsx                  # User authentication Excel dataset
│   └── Products.xlsx               # Inventory product Excel dataset
├── tests/ 
│   ├── api/
│   │   └── test_api_workflow.py   # REST API automation tests
│   ├── database/
│   │   └── test_db_validation.py  # UI vs Database integrity tests
│   ├── test_cart.py                # Shopping cart UI tests
│   ├── test_checkout.py            # E2E checkout workflow UI tests
│   ├── test_login.py               # Authentication UI tests
│   ├── test_logout.py              # User session logout UI tests
│   └── test_search.py              # Catalog discovery & detail UI tests
├── browserstack.yml                # BrowserStack cloud execution configuration
├── CHANGELOG.md                    # Release history and version updates
├── conftest.py                     # Global pytest fixtures, CLI options, & hooks
├── CONTRIBUTING.md                 # Open-source contributor guidelines
├── docker-compose.yml              # Multi-container orchestration definition
├── Dockerfile                      # Container image definition
├── Jenkinsfile                     # Declarative Jenkins CI/CD pipeline
├── LICENSE                         # MIT License
├── pytest.ini                      # Pytest execution settings, markers, & reports
└── requirements.txt                # Python dependencies
=======
│   ├── base/                     # BaseTest (browser lifecycle + page init)
│   ├── config/                   # config.ini + ConfigReader
│   ├── exceptions/               # Custom exception types
│   ├── models/                   # Typed execution data models
│   ├── pages/                    # Page Object Model classes
│   ├── reports/                  # Dashboard builder, report manager, JSON exporter
│   ├── services/                 # API client + user API service
│   └── utils/                    # Waits, logging, screenshots, data, DB helpers
├── testdata/                     # External test data (Excel, JSON, CSV)
└── tests/                        # Executable test suites
>>>>>>> 8be0472 (Finalize enterprise Selenium automation framework)
```

### Key directories

| Path | Purpose |
|------|---------|
| `src/pages/` | Page Object Model classes (`LoginPage`, `HomePage`, `ProductPage`, `CartPage`, `CheckoutPage`). Each encapsulates locators and business actions for a page. |
| `src/utils/` | Reusable framework utilities: `WaitHelper`, `Logger`, `Screenshot`, `ExcelReader`, `DataProvider`, `DBUtility`, `SoftAssert`, `TestDataGenerator`, `EmailReporter`. |
| `src/config/` | `config.ini` (multi-environment settings) and `ConfigReader` (parses config + resolves environment variables). |
| `src/services/` | `APIClient` (Requests wrapper with retries and validation helpers) and `UserAPIService` (service-object pattern for JSONPlaceholder). |
| `src/reports/` | `EnterpriseDashboardBuilder` (standalone HTML dashboard), `ReportManager` (metadata + CSS/JS), `JSONExporter` (normalized telemetry). |
| `src/models/` | Typed dataclasses for test results, failures, execution summaries, and metrics. |
| `tests/` | Executable test suites (see [Test Modules](#-test-modules)). |
| `testdata/` | External datasets: `Login.xlsx`, `Products.xlsx`, `csv/`, `json/`. |

---

<<<<<<< HEAD
## ⚡ Quick Start & Installation & run
=======
## 7. Test Modules
>>>>>>> 8be0472 (Finalize enterprise Selenium automation framework)

| Module | Location | Tests | Coverage |
|--------|----------|-------|----------|
| Login | `tests/test_login.py` | 16 | Valid/invalid auth, locked user, blank fields, masked password, session refresh, protected-page redirects, error dismissal |
| Logout | `tests/test_logout.py` | 7 | Logout flow, protected-page access after logout, back-button and refresh behavior |
| Cart | `tests/test_cart.py` | 18 | Add/remove/update items, badge counts, subtotal math, order preservation, refresh persistence |
| Checkout | `tests/test_checkout.py` | 20 | Successful checkout, field validation, overview math, tax, completion confirmation, cancel flows |
| Search / Catalog | `tests/test_search.py` | 15 | Product discovery, partial/case-insensitive matching, sorting, detail navigation |
| Home (UI) | `tests/ui/test_home.py` | 18 | Catalog rendering, product cards, sorting, detail-page parity |
| Product (UI) | `tests/ui/test_product.py` | 10 | Detail view validation, add/remove from details, badge state |
| API | `tests/api/` | 27 | CRUD workflows, schema/header/SLA validation, negative API cases |
| Database | `tests/database/` | 12 | Connection health, SKU lookup, constraints, UI-vs-DB parity, integrity |
| E2E | `tests/e2e/` | 4 | Complete shopping journeys |
| Regression | `tests/regression/` | 5 | Cross-subsystem sanity checks |
| Negative scenarios | `tests/test_negative_scenarios.py` | 12 | Locked user, invalid credentials, checkout validation, unauthorized access, API/DB negatives |
| Cross-browser | `tests/ui/test_cross_browser.py` | 2 | Login/catalog and cart/checkout across browser engines |
| Data-driven | `tests/ui/test_data_driven.py` | 15 | JSON/CSV parameterized UI tests |

---

## 8. Number of Implemented Tests

Verified with `pytest --collect-only -q`:

```text
181 tests collected in 2.46s
```

- **171 test functions** defined in the codebase.
- **181 collected test cases** because 5 data-driven functions are parameterized and expand to 15 instances (10 additional instances).
- This count is **derived from the actual source** and is not an estimate.

---

## 9. Test-Case Summary

| Suite | Count |
|-------|-------|
| Login | 16 |
| Logout | 7 |
| Cart | 18 |
| Checkout | 20 |
| Search / Catalog | 15 |
| Home UI | 18 |
| Product UI | 10 |
| API (workflow + validation + negative) | 27 |
| Database (validation + integrity) | 12 |
| E2E | 4 |
| Regression | 5 |
| Negative scenarios | 12 |
| Cross-browser | 2 |
| Data-driven (JSON/CSV) | 15 |
| **Total** | **181** |

See [docs/test-cases.md](docs/test-cases.md) for the complete, source-derived test-case matrix.

---

## 10. Installation

### Prerequisites

- **Python 3.10+** (verified on 3.13.1)
- **Google Chrome**, **Mozilla Firefox**, or **Microsoft Edge** installed for local UI runs
- (Optional) **Docker** for containerized execution
- (Optional) **Allure CLI** for Allure HTML reports (the Python package alone does not provide the CLI)
- (Optional) **BrowserStack** account for cloud execution

### Clone the repository

```bash
git clone <repository-url>
cd Enterprise_Selenium_Python_Automation_Framework
<<<<<<< HEAD

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt


---

# ▶️ Running the Framework

After installing the dependencies, you can execute the framework using the following commands.

## Verify Installation

Check Python version:

```bash
python --version
```

Check pytest installation:

```bash
pytest --version
```

List all installed packages:

```bash
pip list
```

---

## Run Complete Test Suite

Execute all UI, API, and Database tests.

```bash
pytest
```

---

## Run Tests with Chrome

```bash
pytest --browser=chrome
```

---

## Run Chrome in Headless Mode

```bash
pytest --browser=chrome --headless
```

---

## Run Firefox

```bash
pytest --browser=firefox
```

---

## Run Microsoft Edge

```bash
pytest --browser=edge
```

---

## Run BrowserStack Tests

Set BrowserStack credentials.

### Windows PowerShell

```powershell
$env:BROWSERSTACK_USERNAME="YOUR_USERNAME"
$env:BROWSERSTACK_ACCESS_KEY="YOUR_ACCESS_KEY"
```

### Linux/macOS

```bash
export BROWSERSTACK_USERNAME="YOUR_USERNAME"
export BROWSERSTACK_ACCESS_KEY="YOUR_ACCESS_KEY"
```

Execute:

```bash
pytest --browser=browserstack
```

---

## Run Smoke Tests

```bash
pytest -m smoke
```

---

## Run Regression Suite

```bash
pytest -m regression
```

---

## Run API Tests

```bash
pytest tests/api/
```

or

```bash
pytest -m api
```

---

## Run Database Tests

```bash
pytest tests/database/
```

or

```bash
pytest -m db
```

---

## Run Specific Test File

Example:

```bash
pytest tests/test_login.py
```

Run Checkout Tests

```bash
pytest tests/test_checkout.py
```

Run Search Tests

```bash
pytest tests/test_search.py
```

---

## Run Specific Test Method

```bash
pytest tests/test_login.py::TestLogin::test_valid_user_login
```

---

## Parallel Execution

Automatically use all CPU cores.

```bash
pytest -n auto
```

Use four parallel workers.

```bash
pytest -n 4
```

Retry failed tests once.

```bash
pytest -n auto --reruns 1
```

---

## Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

Generated report:

```
reports/report.html
```

---

## Generate Allure Report

Generate Allure results.

```bash
pytest --alluredir=reports/allure-results
```

Generate HTML report.

```bash
allure serve reports/allure-results
```

---

## Generate JUnit XML Report

```bash
pytest --junitxml=reports/results.xml
```

---

## Docker Execution

Build Docker image.

```bash
docker build -t enterprise-selenium-framework .
```

Run framework inside Docker.

```bash
docker run --rm enterprise-selenium-framework
```

---

## Docker Compose

```bash
docker-compose up --build
```

---

## Jenkins

The framework includes a production-ready Jenkins pipeline.

Simply create a Pipeline Job and point Jenkins to the repository.

Jenkins automatically performs:

- Checkout Source Code
- Install Dependencies
- Execute Tests
- Generate HTML Report
- Generate Allure Report
- Archive Reports
- Publish Build Artifacts

---

## GitHub Actions

Push the repository to GitHub.

Every push or pull request automatically:

- Installs Python
- Installs dependencies
- Executes Selenium tests
- Generates reports
- Uploads execution artifacts

Workflow file:

```
.github/workflows/regression.yml
```

---

## Generated Reports

After every successful execution, the framework automatically generates:

```
reports/
│
├── dashboard.html
├── report.html
├── results.xml
├── allure-results/
└── allure-report/
```

---

## Screenshots

Whenever a UI test fails, screenshots are automatically captured.

```
screenshots/
└── failures/
```

---

## Logs

Execution logs are automatically generated.

```
logs/
└── automation.log
```

---

## Expected Output

Example:

```
====================================================
Platform : Windows 11
Python   : 3.13
Browser  : Chrome
Environment : QA

Collected Tests : 18

18 Passed
0 Failed
0 Skipped

Execution Time : 01:08

HTML Report Generated

Enterprise Dashboard Generated

Allure Results Generated

====================================================
```
=======
>>>>>>> 8be0472 (Finalize enterprise Selenium automation framework)
```

---

## 11. Virtual Environment Setup

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux / macOS (Bash)

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify the install:

```bash
python -m pytest --version
python -c "import selenium; print(selenium.__version__)"
```

---

## 12. Configuration

All runtime configuration lives in **`src/config/config.ini`** (not the repository root).

Key sections:

| Section | Purpose |
|---------|---------|
| `[framework]` | Active environment, default browser, headless default |
| `[qa]` / `[staging]` / `[production]` | Base URL, credentials placeholders, timeouts |
| `[chrome]` / `[firefox]` / `[edge]` | Per-browser headless defaults and window size |
| `[browserstack]` | BrowserStack capabilities and credentials placeholders |
| `[timeouts]` | Implicit (10s), explicit (15s), page-load (30s) waits |

Credentials are read from environment variables using `${VAR}` placeholders. Copy `.env.example` to `.env` (or set environment variables) before running:

```bash
# Required for UI tests that read credentials from config
APP_USERNAME=standard_user
APP_PASSWORD=secret_sauce
BASE_URL=https://www.saucedemo.com
BROWSER=chrome
HEADLESS=false
ENV=qa
```

> **Important limitation:** Changing `base_url` alone does **not** make the Page Objects work against another website. The locators in `src/pages/` are specific to SauceDemo's DOM. Automating another site requires writing new page objects. See [docs/configuration.md](docs/configuration.md).

---

## 13. Test Data

Test data is stored under `testdata/`:

| File | Purpose |
|------|---------|
| `testdata/Login.xlsx` | Sheets: `valid_users`, `invalid_users`, `checkout_users` |
| `testdata/Products.xlsx` | Sheet: `products` (name, price, etc.) |
| `testdata/json/login_data.json` | Valid/invalid/locked/empty login cases |
| `testdata/json/checkout_data.json` | Valid customers and negative checkout cases |
| `testdata/json/search_data.json` | Search scenarios with expected match counts |
| `testdata/json/products_data.json` | Product catalog data |
| `testdata/csv/users.csv` | Username/password/role/expected_result rows |
| `testdata/csv/products.csv` | Product rows |
| `testdata/csv/checkout.csv` | Checkout rows |

Data is loaded with `DataProvider.load_data(path, key_or_sheet)` which dispatches on file extension, or `ExcelReader(path).get_sheet_data(sheet)` for workbooks. See [docs/test-data.md](docs/test-data.md).

---

## 14. Running Tests

```bash
# Run the full suite (default browser from config)
pytest

# Full suite, explicit Chrome, headless
pytest --browser=chrome --headless

# A single test module
pytest tests/test_login.py --browser=chrome --headless

# A single test function
pytest tests/test_login.py::TestLogin::test_valid_user_login --browser=chrome

# List all tests without running them
pytest --collect-only -q
```

The following addopts are applied automatically via `pytest.ini`:
`--html=reports/html/report.html --self-contained-html --alluredir=reports/allure-results --junitxml=reports/junit/results.xml`

---

## 15. Browser Selection

```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
pytest --browser=browserstack   # requires BrowserStack credentials
```

The browser can also be set via the `BROWSER` environment variable or the `browser` key in `config.ini`.

---

## 16. Headless Execution

```bash
pytest --browser=chrome --headless
pytest --browser=firefox --headless
pytest --browser=edge --headless
```

Omit `--headless` to run with a visible browser window. `HEADLESS=true` in the environment (or the `headless` config key) also enables headless mode.

---

## 17. Parallel Execution

```bash
# Auto-detect CPU core count
pytest -n auto --browser=chrome --headless

# Fixed worker count
pytest -n 2 --browser=chrome --headless
```

> Note: `conftest.py` includes a `pytest_runtest_logreport` hook that aggregates xdist worker results so the dashboard and JSON telemetry remain correct under parallel execution.

---

## 18. Retry Execution

```bash
# Retry each failed test once
pytest --reruns 1 --browser=chrome --headless

# Retry with a delay
pytest --reruns 2 --reruns-delay 5 --browser=chrome
```

---

## 19. Smoke Tests

```bash
pytest -m smoke --browser=chrome --headless
```

The `smoke` marker tags the most critical flows (21 tests). See [docs/test-execution.md](docs/test-execution.md) for the tagged test list.

---

## 20. Regression Tests

```bash
pytest -m regression --browser=chrome --headless
```

The `regression` marker (144 tests) covers UI, API, database, and E2E suites.

---

## 21. API Tests

```bash
pytest -m api
```

The API suite (32 tests) targets the public **JSONPlaceholder** API (`https://jsonplaceholder.typicode.com`). It does **not** require a browser.

---

## 22. Database Tests

```bash
pytest -m db
```

The database suite (14 tests) uses an **in-memory SQLite** catalog for deterministic validation. `DBUtility` also supports MySQL and PostgreSQL dialects for real databases.

---

## 23. HTML Reports

Generated automatically on every run:

- **pytest-html report**: `reports/html/report.html` (self-contained, includes metadata and failure screenshots)
- **JUnit XML**: `reports/junit/results.xml` (for CI parsing)

Open with a browser or view the generated `file:///` path printed at the end of the run.

---

## 24. Enterprise Dashboard

A standalone executive analytics dashboard is generated at **`reports/dashboard.html`** after every session:

- KPI cards: total tests, passed, failed, skipped, execution time, success rate
- 6 Chart.js visualizations (pass/fail doughnut, timeline, module distribution, duration, browser distribution, success gauge)
- Searchable, sortable, paginated results table with status/module filters
- Screenshot viewer modal, log code viewer, and PDF/Excel/CSV export buttons
- Environment & execution metadata panel

See [docs/reporting.md](docs/reporting.md).

---

## 25. Allure

```bash
# Generate Allure telemetry (already enabled by pytest.ini)
pytest --alluredir=reports/allure-results --browser=chrome --headless

# Serve the interactive report (requires Allure CLI installed separately)
allure serve reports/allure-results
```

Allure failures automatically attach the captured screenshot. The **Allure CLI is a separate installation** — the `allure-pytest` Python package only writes telemetry files.

---

## 26. Screenshots

- On **failure**, `Screenshot.capture()` saves a PNG to `screenshots/failures/<test_name>_<timestamp>.png`.
- The screenshot is embedded as a base64 preview inside `reports/html/report.html`.
- It is also attached to Allure results and linked in the enterprise dashboard.

---

## 27. Logging

- Console output is always active.
- A rotating file log is written to **`logs/framework.log`** with timestamps, level, logger name, file, and line.
- Password/token values are masked in telemetry via `JSONExporter._mask_secrets()`.

---

## 28. BrowserStack

```bash
$env:BROWSERSTACK_USERNAME="your_username"     # PowerShell
$env:BROWSERSTACK_ACCESS_KEY="your_access_key"
pytest --browser=browserstack -m smoke
```

Capabilities are defined in `browserstack.yml` and read at runtime from `[browserstack]` in `config.ini` (credentials via environment variables). See [docs/browserstack.md](docs/browserstack.md).

---

## 29. Docker

```bash
# Build the image
docker build -t enterprise-selenium-framework .

# Run the full suite headlessly in a container
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -v ${PWD}/screenshots:/app/screenshots \
  -v ${PWD}/logs:/app/logs \
  enterprise-selenium-framework

# Or use docker-compose (Chrome headless, 2 workers, reruns)
docker compose up --build
```

See [docs/docker.md](docs/docker.md).

---

## 30. Jenkins

The repository includes a declarative `Jenkinsfile` with `Checkout → Setup → Test` stages and a `post` block that publishes the dashboard, archives artifacts (screenshots, logs, reports), and records JUnit results. It supports `BROWSER` and `HEADLESS` build parameters. See [docs/jenkins.md](docs/jenkins.md).

---

## 31. GitHub Actions

`.github/workflows/regression.yml` triggers on push/PR to `main`/`master`/`develop`, on a daily schedule, and manually via `workflow_dispatch`. It provisions Python 3.12, installs browsers, runs the suite, and uploads the dashboard, HTML report, JUnit XML, Allure results, JSON telemetry, and failure screenshots as artifacts. See [docs/github-actions.md](docs/github-actions.md).

---

## 32. Troubleshooting

Common issues (pytest not recognized, driver errors, missing Excel files, report generation, BrowserStack credentials, etc.) are documented in [docs/troubleshooting.md](docs/troubleshooting.md).

---

## 33. Security

**Never commit secrets to the repository.** This includes:

- Passwords
- API keys / access tokens
- BrowserStack credentials
- Database credentials
- SMTP passwords
- Private keys
- `.env` files

The framework reads all credentials from environment variables or `${VAR}` placeholders resolved by `ConfigReader`. A safe template is provided at `.env.example`; the actual `.env` is excluded by `.gitignore`.

---

## 34. Development

See [docs/development-guide.md](docs/development-guide.md) for how to add page objects, tests, utilities, test data, markers, browsers, environments, API services, and database validations following the framework's conventions.

---

## 35. Contribution

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, branch workflow, and PR guidelines.

---

## 36. License

This project is licensed under the [MIT License](LICENSE).

---

## Quick Reference

```text
SETUP
  python -m venv venv
  .\venv\Scripts\Activate.ps1          # Windows
  pip install -r requirements.txt

RUN
  pytest

CHROME
  pytest --browser=chrome --headless

FIREFOX
  pytest --browser=firefox --headless

EDGE
  pytest --browser=edge --headless

PARALLEL
  pytest -n auto --headless

SMOKE
  pytest -m smoke --headless

REGRESSION
  pytest -m regression --headless

API
  pytest -m api

DATABASE
  pytest -m db

ALLURE
  pytest --alluredir=reports/allure-results
```
