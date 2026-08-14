# Development Guide

This guide explains how to extend the framework following its existing conventions: page objects, tests, utilities, test data, markers, browsers, environments, API services, and database validation.

---

## 1. Code Layout & Conventions

| Area | Location | Convention |
|------|----------|------------|
| Page Objects | `src/pages/` | One class per screen; locators private; business actions return state, not raw elements |
| Base test | `src/base/base_test.py` | UI suites inherit `BaseTest` and call `self.init_pages(driver)` |
| Utilities | `src/utils/` | Stateless helpers with explicit parameters |
| Services | `src/services/` | `APIClient` for HTTP; service classes wrap it |
| Exceptions | `src/exceptions/custom_exceptions.py` | Prefer framework exceptions over bare `Exception` |
| Test data | `testdata/` | `.xlsx`/`.json`/`.csv` only |
| Tests | `tests/` | One file per concern; class-level markers; descriptive method names |

**Golden rules:**

- **No `time.sleep()`** — always use `WaitHelper`.
- **No locators in tests** — locators live in Page Objects.
- **No secrets in code** — use `${VAR}` placeholders + env vars.
- Keep the **dependency rule**: tests → pages/services → utils → config.

---

## 2. Adding a New Page Object

1. Create `src/pages/my_page.py`:

```python
from __future__ import annotations
from src.utils.wait_helper import WaitHelper
from src.utils.logger import get_logger

logger = get_logger("MyPage")

class MyPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitHelper(driver)
        # locators as tuples: (By.XPATH, "//...")

    def is_loaded(self) -> bool:
        return self.wait.is_visible(self.PAGE_TITLE)
```

2. Register it in `BaseTest.init_pages()` (`src/base/base_test.py`) so `self.my_page` is available in tests.

3. Use only `WaitHelper` for synchronization and return extracted values/state.

---

## 3. Adding a UI Test

```python
@pytest.mark.ui
@pytest.mark.regression
class TestMyFeature(BaseTest):

    def test_my_feature_works(self, driver):
        self.init_pages(driver)
        self.login_page.login("standard_user", "secret_sauce")
        assert self.home_page.is_loaded()

        # ... act through page objects ...
        assert self.my_page.is_loaded()
```

- Name methods `test_<feature>_<behavior>`.
- Add meaningful markers (see below).
- Write one clear assertion per concern where practical.

---

## 4. Markers

Markers are declared in `pytest.ini`:

```text
markers =
    smoke
    regression
    ui
    api
    database
    db
    e2e
    negative
    cross_browser
    login
    cart
    checkout
    product
    search
    browserstack
    local
    flaky
```

Apply markers at class or method level. Run filtered: `pytest -m smoke`.

---

## 5. Adding Test Data

1. Add a file under `testdata/` (JSON/CSV/Excel).
2. Load it via `DataProvider.load_data(path, key_or_sheet)`.
3. For parameterized UI tests, mimic `tests/ui/test_data_driven.py`:

```python
DATA = DataProvider.load_data(Path("testdata/json/my_data.json"), key_or_sheet="my_cases")

@pytest.mark.parametrize("case", DATA)
def test_ddt_my_case(self, driver, case):
    ...
```

---

## 6. Adding an API Service or Test

- Reuse `APIClient` (`src/services/api_client.py`) for HTTP concerns (headers, timeout, retries).
- Wrap endpoints in a service class like `UserAPIService`.
- Validate with `APIClient.validate_status_code()` and `validate_json_key()`.
- Add `@pytest.mark.api` (and `@pytest.mark.regression` if part of regression).

```python
@pytest.mark.api
class TestMyAPI:

    @pytest.fixture(autouse=True)
    def setup_api(self):
        self.api_service = MyAPIService()
```

---

## 7. Adding a Database Test

- Use `DBUtility(db_type="sqlite", database=":memory:")` for isolated deterministic tests.
- Mark with `@pytest.mark.db` and `@pytest.mark.database`.
- Use `DBUtility.verify_ui_against_db()` for parity checks.
- To target a real DB, pass a connection string; see `DBUtility` docs.

---

## 8. Adding a Browser

1. `src/utils/browser_factory.py` — add a branch in `create()` for the new engine, with `headless` handling and options.
2. `src/config/config.ini` — add a `[<browser>]` section.
3. Register the option in `conftest.py` `pytest_addoption` if needed (values are free-form via `--browser`).
4. Update `docs/configuration.md` and `docs/test-execution.md`.

---

## 9. Adding an Environment

1. `src/config/config.ini` — add `[myenv]` with `base_url`, credentials placeholders, timeouts.
2. Select it via `ENV` env var or `[framework].environment`.
3. Document in `docs/configuration.md`.

---

## 10. Adding a Custom Exception

Extend `src/exceptions/custom_exceptions.py`:

```python
class MyFeatureError(Exception):
    """Raised when ..."""
```

Use it in page objects/services instead of bare `Exception`.

---

## 11. Reporting Hooks

If you change reporting, keep the contract:

- `conftest.py` `pytest_runtest_logreport` aggregates results and emits dashboard + JSON telemetry.
- `src/reports/enterprise_dashboard.py` renders `reports/dashboard.html`.
- `src/reports/json_exporter.py` writes normalized telemetry (with `_mask_secrets()`).
- `src/models/execution_models.py` defines the shared data shape.

---

## 12. Before Submitting Changes

```bash
# Collect cleanly
python -m pytest --collect-only -q

# Run affected tests
python -m pytest tests/your_new_test.py --browser=chrome --headless

# Quick smoke
python -m pytest -m smoke --browser=chrome --headless
```

Also run the lint/format checks your team uses (if any) before opening a PR. See [CONTRIBUTING.md](../CONTRIBUTING.md).
