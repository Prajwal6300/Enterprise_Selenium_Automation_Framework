# FAQ

Frequently asked questions about the Enterprise Selenium Python Automation Framework.

---

## 1. General

### What application does this framework automate?

**SauceDemo** (`https://www.saucedemo.com`), the public e-commerce demo site. UI tests use SauceDemo's pages; API tests use the public **JSONPlaceholder** API; database tests use an in-memory SQLite catalog.

### How many tests are there?

**181 collected test cases** (171 test functions; 5 data-driven functions are parameterized and expand to 15 instances). Verified with `pytest --collect-only -q`.

### Which browsers are supported?

Chrome, Firefox, and Edge locally (headed or headless), plus **BrowserStack** cloud via `--browser=browserstack`.

### Does it need a browser for every test?

No. UI tests need a browser. **API tests** (`-m api`) and **database tests** (`-m db`) run headless/without a browser.

---

## 2. Configuration

### Where is the config file?

`src/config/config.ini` — not the repository root. It is read by `ConfigReader`.

### How do I change the target environment?

Set `ENV` (or `[framework].environment`) to `qa`, `staging`, or `production`. Each section defines its own `base_url`, credentials, and timeouts.

### Can I point it at my own website?

**Not by config alone.** The Page Objects contain SauceDemo-specific locators. You must write new Page Objects for a different site (see [development-guide.md](development-guide.md)).

### Where do credentials come from?

Environment variables or `.env` via `${VAR}` placeholders — never from source files. Copy `.env.example` to `.env`.

---

## 3. Execution

### What command runs everything?

`pytest` (uses config defaults: Chrome, headed). Add `--headless` for CI-friendly runs.

### How do I run headless?

`pytest --browser=chrome --headless` (or set `HEADLESS=true`).

### How do I run in parallel?

`pytest -n auto` or `pytest -n 2`.

### How do I retry failures?

`pytest --reruns 1` (or `--reruns N --reruns-delay S`).

### How do I run just the smoke tests?

`pytest -m smoke`.

### How do I run only API or DB tests?

`pytest -m api` and `pytest -m db`.

---

## 4. Reporting

### Where are reports?

Under `reports/`:

- `reports/dashboard.html` — executive dashboard
- `reports/html/report.html` — pytest-html
- `reports/junit/results.xml` — JUnit XML
- `reports/allure-results/` — Allure telemetry
- `reports/executions/EXEC-*.json` — JSON telemetry

### Why is the dashboard missing/outdated?

The dashboard is generated at session end by a conftest hook. Run a normal `pytest` session; it is produced automatically.

### How do I view Allure results?

`allure serve reports/allure-results` (requires the **Allure CLI**, installed separately — the Python package only writes telemetry).

### Do reports contain secrets?

No. `JSONExporter._mask_secrets()` replaces passwords/tokens with `***REDACTED***`.

---

## 5. Test Data

### What test data is included?

`testdata/Login.xlsx`, `Products.xlsx`, `csv/` (users, products, checkout), and `json/` (login, checkout, search, products). See [test-data.md](test-data.md).

### Why does the login test need `testdata/Login.xlsx`?

The Excel sheet `valid_users` provides the credentials used by several login/cart/checkout tests; the file is committed to the repo (demo credentials only).

---

## 6. Architecture

### Why Page Objects?

They centralize locators and business actions, keeping tests clean and resilient to DOM changes. See [architecture.md](architecture.md).

### Are there any `time.sleep()` calls?

**No.** All synchronization uses `WaitHelper` explicit/fluent waits.

### How are failures captured?

`Screenshot.capture()` saves a PNG to `screenshots/failures/` and embeds it in the HTML report.

---

## 7. CI/CD

### What CI is supported?

GitHub Actions (`.github/workflows/regression.yml`), Jenkins (`Jenkinsfile`), Docker (`Dockerfile` + `docker-compose.yml`), and BrowserStack (`browserstack.yml`).

### Does GitHub Actions run BrowserStack?

No. The workflow runs local browsers (Chrome/Firefox/Edge). Use BrowserStack directly or via Jenkins/self-hosted runners for cloud execution.

### Why did my CI job pass but no dashboard was uploaded?

Artifacts upload with `if: always()`. If `reports/dashboard.html` is missing, the archive is empty — check the dashboard step ran to completion.

---

## 8. Contribution

### How do I add a test?

Follow [development-guide.md](development-guide.md), then open a PR per [CONTRIBUTING.md](../CONTRIBUTING.md).

### Are credentials safe to commit?

**No.** Never commit real passwords, tokens, or BrowserStack keys. Use `${VAR}` placeholders and `.env`.

---

## 9. Versioning

### What is the framework version?

`2.5.0-Enterprise` (reported by `ReportManager` and in `package.json`). See [CHANGELOG.md](../CHANGELOG.md) for history.

### What Python/pytest versions are supported?

Python 3.10+; pytest 9.x (verified 9.1.1). Requirements use `>=` minimums, so newer compatible versions install.