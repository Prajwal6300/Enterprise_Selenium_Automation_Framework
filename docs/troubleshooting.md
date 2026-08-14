# Troubleshooting

Common issues and their fixes, grouped by area.

---

## 1. Installation & Environment

| Symptom | Cause | Fix |
|---------|-------|-----|
| `pytest: command not found` | venv not activated | Activate venv or use `python -m pytest` |
| `ModuleNotFoundError: No module named 'selenium'` | deps not installed in active venv | `pip install -r requirements.txt` |
| `ImportError` on framework modules | running from wrong directory | Run pytest from the repository root so `src/` and `conftest.py` resolve |
| PowerShell blocks `.venv\Scripts\Activate.ps1` | execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then re-activate |

---

## 2. Browser / Driver Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `SessionNotCreatedException: This version of ChromeDriver only supports Chrome version X` | driver/browser mismatch | Update the browser; `webdriver-manager` + Selenium Manager resolve matching drivers automatically |
| `WebDriverException: unknown error: cannot find Chrome binary` | Chrome not installed / not on PATH | Install Chrome (or Firefox/Edge) and ensure the executable is discoverable |
| `BrowserInitializationError` | browser creation failed | Confirm the browser is installed and the `--browser` value is one of `chrome`, `firefox`, `edge`, `browserstack` |
| Edge tests fail | Edge not installed | Install Microsoft Edge, or use Chrome/Firefox |
| Slow driver startup | first-run driver download | Let webdriver-manager download once; subsequent runs reuse the cache |

---

## 3. Test Failures That Look Like Flakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Intermittent `TimeoutException` | element not visible within `explicit_wait` | Increase `[timeouts].explicit_wait` in `src/config/config.ini` |
| Flaky failures under load | network/slow page | Use `--reruns 1`; the Docker/CI defaults already do |
| Element intercepted / not clickable | page animating | `WaitHelper` retries clicks; ensure no ad overlays |

---

## 4. Data & Test Data

| Symptom | Cause | Fix |
|---------|-------|-----|
| `DataNotAvailableError` | test data file missing | Confirm `testdata/Login.xlsx`, `testdata/Products.xlsx`, `csv/`, `json/` exist |
| KeyError for a data column | dataset schema changed | Match column names used by the test (see [test-data.md](test-data.md)) |
| Excel read fails | openpyxl missing / file locked | `pip install openpyxl`; close the workbook in Excel |

---

## 5. Reporting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `reports/html/report.html` missing | pytest-html plugin not installed | `pip install pytest-html` |
| `allure serve` fails: command not found | Allure CLI not installed | Install Allure CLI (see [installation.md](installation.md)) |
| `reports/dashboard.html` not updated | reporting hook didn't fire | Run a normal `pytest` session; check `conftest.py` `pytest_runtest_logreport` |
| JUnit XML empty | `--junitxml` output dir missing | Create `reports/junit/` or rely on `addopts` which writes it |

---

## 6. API / Database

| Symptom | Cause | Fix |
|---------|-------|-----|
| API tests fail with connection errors | no internet or JSONPlaceholder down | Check network; the API tests target `https://jsonplaceholder.typicode.com` |
| `DatabaseConnectionError` | DB engine unavailable | DB tests use in-memory SQLite by default; only a custom `DBUtility` connection string needs an external server |
| Slow API SLA test failures | latency | Increase tolerance or the `api_timeout` setting |

---

## 7. BrowserStack

| Symptom | Cause | Fix |
|---------|-------|-----|
| Auth failure on `--browser=browserstack` | credentials not set | Set `BROWSERSTACK_USERNAME` / `BROWSERSTACK_ACCESS_KEY` env vars or `.env` |
| Timeout on Safari | provisioning latency | Increase `explicit_wait`; verify capability in `browserstack.yml` |

---

## 8. CI/CD

| Symptom | Cause | Fix |
|---------|-------|-----|
| GitHub Actions: Chrome not found | `chrome` browser but Chrome install step skipped | The workflow installs Chrome unconditionally; check the step logs |
| GitHub Actions: Edge not found | browser `edge` on Ubuntu | Edge is installed only when `inputs.browser == 'edge'` |
| Jenkins: `python: command not found` | agent lacks Python | Install Python and add to `PATH` on the agent |
| Jenkins: dashboard not published | `publishHTML` needs HTML Publisher plugin | Install the **HTML Publisher** plugin in Jenkins |
| Docker: browser missing | image only has Chromium + Firefox | Use Chrome/Firefox in Docker; Edge is not installed in the image |

---

## 9. Fastest Diagnostic Commands

```bash
# Does the suite collect cleanly?
python -m pytest --collect-only -q

# Run one login test verbosely
python -m pytest tests/test_login.py::TestLogin::test_valid_user_login -v

# Confirm browser works
python -m pytest -m smoke --browser=chrome --headless

# See installed versions
python -m pip list | findstr /i "pytest selenium openpyxl"
```

---

## 10. If Nothing Else Helps

1. Run a single failing test with `-v -s` and read `logs/framework.log`.
2. Check the failure screenshot under `screenshots/failures/`.
3. Confirm your environment matches [installation.md](installation.md) versions.
4. Open the HTML report for the full failure trace and screenshot.
