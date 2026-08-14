# Architecture

This document describes the internal architecture of the Enterprise Selenium Python Automation Framework. It maps each concept in the design to the concrete modules that implement it.

---

## 1. Architectural Overview

The framework follows a **layered architecture**:

```text
┌─────────────────────────────────────────────────────────────────┐
│                         TEST LAYER                              │
│  tests/*.py  tests/api/*  tests/database/*  tests/e2e/*         │
│  tests/regression/*  tests/ui/*                                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
┌───────────────────────────────▼─────────────────────────────────┐
│                   ORCHESTRATION LAYER                           │
│  conftest.py (fixtures, hooks)                                  │
│  src/base/base_test.py (BaseTest)                               │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
┌───────────────────────────────▼─────────────────────────────────┐
│                APPLICATION SERVICE LAYER                        │
│  src/pages/*          → Page Objects (UI)                       │
│  src/services/api_client.py / user_api.py → REST API            │
│  src/utils/db_utility.py          → Database                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
┌───────────────────────────────▼─────────────────────────────────┐
│                      UTILITY LAYER                              │
│  src/utils/ (waits, logging, screenshots, data, soft assert)    │
│  src/config/config_reader.py (ConfigReader)                     │
│  src/exceptions/custom_exceptions.py                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
┌───────────────────────────────▼─────────────────────────────────┐
│                   REPORTING LAYER                               │
│  src/reports/ (dashboard, report manager, JSON exporter)        │
│  src/models/execution_models.py (typed data models)             │
└─────────────────────────────────────────────────────────────────┘
```

**Dependency rule:** each layer may only depend on layers below it. Tests never talk to Selenium directly; they interact with page objects and services.

---

## 2. Directory-to-Layer Mapping

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| Test | `tests/` | Executable test cases grouped by concern |
| Orchestration | `conftest.py`, `src/base/` | Pytest fixtures, browser lifecycle, hooks |
| Application service | `src/pages/`, `src/services/` | Page Objects, API client, DB service |
| Utility | `src/utils/`, `src/config/`, `src/exceptions/` | Reusable helpers and cross-cutting concerns |
| Reporting | `src/reports/`, `src/models/` | Dashboard, HTML/JUnit/Allure, JSON telemetry |

---

## 3. Test Layer (`tests/`)

Tests are grouped into suites, each with its own markers (registered in `pytest.ini`):

| Directory / File | Suite | Count |
|------------------|-------|-------|
| `tests/test_login.py` | Login | 16 |
| `tests/test_logout.py` | Logout | 7 |
| `tests/test_cart.py` | Cart | 18 |
| `tests/test_checkout.py` | Checkout | 20 |
| `tests/test_search.py` | Search | 15 |
| `tests/test_negative_scenarios.py` | Negative | 12 |
| `tests/api/test_api_workflow.py` | API workflow | 11 |
| `tests/api/test_api_validation.py` | API validation | 8 |
| `tests/api/test_api_negative.py` | API negative | 8 |
| `tests/database/test_db_validation.py` | DB validation | 6 |
| `tests/database/test_data_integrity.py` | DB integrity | 6 |
| `tests/e2e/test_end_to_end_journey.py` | E2E | 2 |
| `tests/e2e/test_purchase_workflow.py` | E2E purchase | 2 |
| `tests/regression/test_regression_suite.py` | Regression | 5 |
| `tests/ui/test_home.py` | Home UI | 18 |
| `tests/ui/test_product.py` | Product UI | 10 |
| `tests/ui/test_data_driven.py` | Data-driven | 15 |
| `tests/ui/test_cross_browser.py` | Cross-browser | 2 |

> Totals: **171 test functions** → **181 collected test cases** (5 data-driven functions are parameterized and expand to 15 instances).

Tests obtain a browser via the `driver` fixture and page objects via `BaseTest`. They also consume external data through `DataProvider.load_data()`.

---

## 4. Orchestration Layer

### 4.1 `conftest.py`

Root-level conftest provides the shared pytest infrastructure:

- **`driver` fixture** — the Selenium WebDriver. It resolves the browser from `--browser` CLI / `BROWSER` env / `config.ini`, creates the driver via `BrowserFactory`, yields it to the test, and always quits on teardown. A browser *session* scope variant is provided for E2E/regression suites.
- **`driverless` fixture** — used by API and database tests that do not need a browser.
- **Hooks**:
  - `pytest_addoption` — registers `--browser`, `--headless` command-line options.
  - `pytest_runtest_makereport` — captures the failure screenshot into the pytest-html report.
  - `pytest_runtest_logreport` — aggregates xdist worker results and triggers dashboard / JSON telemetry generation at session end.
- Helper fixtures that wrap page objects for commonly used flows (login, add-to-cart, etc.).

### 4.2 `src/base/base_test.py` — `BaseTest`

`BaseTest` is the base class for all UI test classes. It:

- Declares `driver = None` and lazily initializes it using the same browser resolution logic.
- Provides `self.login`, `self.home`, `self.product`, `self.cart`, `self.checkout` page-object instances.
- Offers helper methods such as `open_and_verify()` (navigate + wait for home) and standard setup/teardown hooks that are overridable by subclasses.

---

## 5. Application Service Layer

### 5.1 Page Objects (`src/pages/`)

Every SauceDemo screen has one page class that encapsulates its locators and business actions:

| Class | File | Responsibilities |
|-------|------|------------------|
| `LoginPage` | `src/pages/login_page.py` | Username/password entry, login submission, error message handling, locked-out error, field clearing, credential field masking (entering char-by-char). |
| `HomePage` | `src/pages/home_page.py` | Catalog rendering, product card access, sorting dropdown, add/remove to cart, cart badge count, navigation to cart. |
| `ProductPage` | `src/pages/product_page.py` | Product detail title/description/price extraction, add-to-cart from detail view, back navigation. |
| `CartPage` | `src/pages/cart_page.py` | Cart item listing, quantity updates, item removal, subtotal math, checkout initiation. |
| `CheckoutPage` | `src/pages/checkout_page.py` | Information step, form validation errors, overview totals/tax computation, finish confirmation, cancel flows. |

All page objects use `WaitHelper` for synchronization — **no `time.sleep()` calls exist anywhere in the framework**.

### 5.2 API Layer (`src/services/`)

| Class | File | Purpose |
|-------|------|---------|
| `APIClient` | `src/services/api_client.py` | Thin Requests wrapper: base URL, headers, timeout, retry-with-backoff, and shared assertion helpers (status code, content-type, required keys, SLA timing). |
| `UserAPIService` | `src/services/user_api.py` | Service-object pattern over `APIClient` for the JSONPlaceholder API (`https://jsonplaceholder.typicode.com`): `get_users`, `get_user(id)`, `create_user`, `update_user`, `delete_user`, `get_posts`, etc. |

The API tests in `tests/api/` exercise workflows, validation, and negative cases against this public demo API — no browser is required.

### 5.3 Database Layer (`src/utils/db_utility.py` — `DBUtility`)

`DBUtility` is a SQLAlchemy-based database helper:

- Connects to a **default in-memory SQLite** catalog so database tests are deterministic and require no external server.
- Supports **MySQL** and **PostgreSQL** dialects when a connection string is provided.
- Provides `health_check()`, `fetch_all()`, `fetch_one()`, schema inspection, and sample-data seeding for the `products` catalog used by the integrity suite.

Database tests in `tests/database/` verify connection health, SKU lookup, unique constraints, UI-to-database parity, and data integrity.

---

## 6. Utility Layer (`src/utils/`)

| Utility | Purpose |
|---------|---------|
| `WaitHelper` | Explicit waits (`wait_for_element`, `wait_for_visible`, `wait_for_clickable`, `wait_for_text`, `wait_until`), fluent wait with retry, and page-load readiness. |
| `Logger` | Console + rotating file logger writing to `logs/framework.log` with timestamps, level, file, and line. |
| `Screenshot` | Captures PNG evidence to `screenshots/failures/`, returns a base64 preview for HTML/Allure embedding. |
| `ExcelReader` | Reads `.xlsx` sheets into `list[dict]` via openpyxl; used for `Login.xlsx` and `Products.xlsx`. |
| `DataProvider` | Unified `load_data(path, key)` dispatcher over JSON / CSV / Excel. |
| `DBUtility` | SQLAlchemy-backed database helper (see above). |
| `SoftAssert` | Collects multiple assertion failures and reports them together at the end of a test. |
| `TestDataGenerator` | Deterministic test-data generators (prices, usernames, checkout metadata). |
| `EmailReporter` | Optional SMTP email report notifier (configurable, not run by default). |

---

## 7. Configuration Layer (`src/config/`)

- **`config.ini`** — the single source of runtime configuration. Sections: `[framework]`, `[qa]`, `[staging]`, `[production]`, `[chrome]`, `[firefox]`, `[edge]`, `[browserstack]`, `[timeouts]`.
- **`ConfigReader`** — singleton `ConfigReader` that:
  - Parses `config.ini` with interpolation.
  - Resolves `${VAR}` placeholders (e.g., `${BASE_URL}`) against **environment variables** and the local `.env` file (via python-dotenv), so **no secrets live in source files**.
  - Exposes typed getters: `get_framework()`, `get_environment()`, `get_browser_config()`, `get_browserstack_capabilities()`, `get_timeouts()`, and a general `get(section, key)`.

See [configuration.md](configuration.md) for the full key reference.

---

## 8. Exception Layer (`src/exceptions/custom_exceptions.py`)

Custom exceptions provide precise failure semantics:

- `BrowserInitializationError` — browser creation failed.
- `PageLoadTimeoutError` — page did not reach readiness within timeout.
- `LocatorNotFoundError` — element/locator not found.
- `ElementNotClickableError` — clickable-expected element could not be clicked.
- `DataNotAvailableError` — test data missing/unreadable.
- `DatabaseConnectionError` — database connection failed.
- `ConfigurationError` — invalid/missing configuration.
- `EmailSendError` — email notification failed.

Tests can catch these to distinguish environmental failures from functional failures.

---

## 9. Reporting Layer (`src/reports/`)

| Module | Purpose |
|--------|---------|
| `report_manager.py` | `ReportManager` — builds the execution summary, produces `reports/dashboard.html` metadata, attaches CSS/JS resources, and coordinates report emission. Exposes the framework version (`2.5.0-Enterprise`) and environment metadata used across reports. |
| `enterprise_dashboard.py` | `EnterpriseDashboardBuilder` — renders the standalone analytics dashboard with KPI cards, Chart.js visualizations, a searchable/paginated results table, screenshot viewer, and PDF/Excel/CSV export. |
| `json_exporter.py` | `JSONExporter` — writes normalized execution telemetry to `reports/executions/EXEC-*.json`, `reports/latest_execution.json`, and `reports/history_index.json`. Secrets are masked via `_mask_secrets()`. |

The three reporting outputs are generated automatically at the end of every session:

- `reports/dashboard.html` (standalone dashboard)
- `reports/html/report.html` + `reports/junit/results.xml` (pytest-html / JUnit — via pytest addopts)
- `reports/allure-results/` (Allure telemetry — via pytest addopts)
- `reports/executions/EXEC-*.json` (JSON telemetry)

See [reporting.md](reporting.md).

---

## 10. Data Models (`src/models/execution_models.py`)

Typed dataclasses keep report data consistent and serializable:

- `TestResult`, `Failure`, `ExecutionSummary`, `ExecutionMetrics`, `BrowserInfo`, `ExecutionMetadata`, `EnvironmentInfo`, `DashboardData`.

`JSONExporter` and `EnterpriseDashboardBuilder` both consume these models, guaranteeing that telemetry and the dashboard never drift out of sync.

---

## 11. Runtime Flow

A typical UI test run:

1. `conftest.py` fixture `driver` asks `BrowserFactory.create()` for a WebDriver.
2. `BrowserFactory` reads the browser name (CLI `--browser` → env `BROWSER` → `config.ini`), applies `--headless` override, and instantiates Chrome / Firefox / Edge / BrowserStack (via `webdriver-manager`, with Selenium Manager fallback).
3. The test (a subclass of `BaseTest`) initializes page objects bound to that driver.
4. Page objects use `WaitHelper` to synchronize with the application; assertions run against extracted state.
5. On failure, `Screenshot.capture()` saves evidence and embeds it in the HTML report.
6. At session end, hooks aggregate results and emit dashboard + JSON telemetry.
7. Reports are written under `reports/`.

API tests skip step 1–4 (they use `driverless`) and call `UserAPIService` directly. Database tests use `DBUtility` directly.

---

## 12. Concurrency & CI

- **Parallelism:** `pytest -n auto` / `-n N` via pytest-xdist; the `pytest_runtest_logreport` hook merges worker results for correct reporting.
- **CI:** GitHub Actions (`regression.yml`), Jenkins (`Jenkinsfile`), Docker (`Dockerfile` + `docker-compose.yml`), BrowserStack (`browserstack.yml`).
- **Scheduling:** regression workflow triggers on push/PR/schedule/manual dispatch.

See the integration docs: [github-actions.md](github-actions.md), [jenkins.md](jenkins.md), [docker.md](docker.md), [browserstack.md](browserstack.md).
