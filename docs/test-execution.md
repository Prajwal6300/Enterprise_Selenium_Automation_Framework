# Test Execution

This guide explains every supported way to execute the test suite, the markers you can filter on, and how parallelism, retries, and timeouts behave.

---

## 1. Test Inventory

The suite contains **181 collected test cases** (171 test functions; 5 data-driven functions are parameterized and expand to 15 instances).

```bash
# List everything without running
pytest --collect-only -q
```

---

## 2. Running the Full Suite

```bash
pytest
```

This runs all 181 tests with the defaults from `src/config/config.ini` (browser `chrome`, headless off) unless overridden.

Automatic reporting via `pytest.ini` `addopts`:

```text
--html=reports/html/report.html --self-contained-html
--alluredir=reports/allure-results
--junitxml=reports/junit/results.xml
```

---

## 3. Browser Selection

```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
pytest --browser=browserstack   # requires BrowserStack credentials
```

You can also set the `BROWSER` environment variable or the `[framework].default_browser` key in `config.ini`.

---

## 4. Headless Execution

```bash
pytest --browser=chrome --headless
```

Omit `--headless` for a visible browser window. `HEADLESS=true` or `[framework].default_headless=true` also enable headless mode.

---

## 5. Parallel Execution (pytest-xdist)

```bash
# Auto-detect cores
pytest -n auto --browser=chrome --headless

# Fixed worker count
pytest -n 2 --browser=chrome --headless
```

`conftest.py` includes a `pytest_runtest_logreport` hook that aggregates worker results so the dashboard and JSON telemetry stay accurate in parallel runs.

---

## 6. Retry Execution (pytest-rerunfailures)

```bash
pytest --reruns 1 --browser=chrome --headless
pytest --reruns 2 --reruns-delay 5 --browser=chrome --headless
```

Reruns are useful for flaky-network scenarios. Tests are not retried by default.

---

## 7. Markers

Markers are registered in `pytest.ini`. Filter with `-m`.

### 7.1 Summary of counts (verified via `--collect-only -m`)

| Marker | Count | Scope |
|--------|-------|-------|
| `smoke` | 21 | Critical login/cart/checkout/E2E paths |
| `regression` | 144 | Full regression (UI + API + DB + E2E) |
| `ui` | 135 | All Selenium UI tests |
| `api` | 32 | All API tests (workflow + validation + negative) |
| `db` / `database` | 14 | All database tests |
| `e2e` | 6 | End-to-end journeys |
| `negative` | 25 | Negative scenarios (UI + API + DB) |
| `login` | 16 | Login suite |
| `cart` | 18 | Cart suite |
| `checkout` | 20 | Checkout suite |
| `search` | 15 | Search/catalog suite |
| `product` | 43 | Product + search + catalog coverage |
| `cross_browser` | 2 | Cross-browser sanity |
| `browserstack` | — | Reserved for cloud-only tests |

### 7.2 Usage examples

```bash
pytest -m smoke --browser=chrome --headless
pytest -m "api or db"                       # combined
pytest -m "not ui"                          # everything non-UI
pytest -m smoke -n auto --headless          # parallel smoke
```

---

## 8. Running Suites by Path

```bash
# UI suites
pytest tests/test_login.py tests/test_cart.py tests/test_checkout.py --browser=chrome --headless
pytest tests/ui/ --browser=chrome --headless

# API (no browser needed)
pytest tests/api/

# Database (no browser needed)
pytest tests/database/

# E2E & regression
pytest tests/e2e/ --browser=chrome --headless
pytest tests/regression/ --browser=chrome --headless

# Single test
pytest tests/test_login.py::TestLogin::test_valid_user_login --browser=chrome --headless

# Data-driven subset by parameter ID
pytest "tests/ui/test_data_driven.py::TestDataDrivenUI::test_ddt_valid_login_json[user_data0]" --browser=chrome
```

---

## 9. Timeout Control

- **pytest-timeout** is installed; add `--timeout=60` to fail tests that exceed 60 seconds.
- Framework-level waits come from `[timeouts]` in `config.ini`: `implicit_wait=10`, `explicit_wait=15`, `page_load_wait=30`.
- API tests use `api_timeout`; DB tests use `db_timeout`.

```bash
pytest --timeout=60 --browser=chrome --headless
```

---

## 10. Exit Codes

`pytest` returns:

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | At least one test failed |
| 2 | Interrupted by the user |
| 3 | Internal error during collection/execution |
| 4 | Usage error (bad CLI options) |
| 5 | No tests collected |

---

## 11. Typical Commands

| Scenario | Command |
|----------|---------|
| Full suite, default browser | `pytest` |
| Chrome headless | `pytest --browser=chrome --headless` |
| Firefox headless | `pytest --browser=firefox --headless` |
| Edge headless | `pytest --browser=edge --headless` |
| Smoke, parallel | `pytest -m smoke -n auto --headless` |
| Regression | `pytest -m regression --headless` |
| API only | `pytest -m api` |
| DB only | `pytest -m db` |
| Rerun failures | `pytest --reruns 1 --headless` |
| Timeout 60s | `pytest --timeout=60 --headless` |
| Allure serve | `allure serve reports/allure-results` |

---

## 12. Execution Modes Summary

| Mode | Mechanism | Requires |
|------|-----------|----------|
| Local headed | `--browser=chrome` (no headless) | Browser installed |
| Local headless | `--browser=chrome --headless` | Browser installed |
| Parallel | `-n auto` / `-n N` | pytest-xdist |
| Cloud | `--browser=browserstack` | BrowserStack creds |
| Container | Docker / docker-compose | Docker |
| CI | GitHub Actions / Jenkins | CI config files |
