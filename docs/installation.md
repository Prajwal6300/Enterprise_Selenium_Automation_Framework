# Installation

This guide walks through installing the framework on Windows, Linux, and macOS, plus optional infrastructure (Docker, Allure, BrowserStack).

---

## 1. Prerequisites

| Requirement | Version / Notes |
|-------------|-----------------|
| Python | 3.10+ (developed and verified on **3.13.1**) |
| pip | Latest (upgrade after creating the venv) |
| Google Chrome | Required for `--browser=chrome` local runs |
| Mozilla Firefox | Required for `--browser=firefox` local runs |
| Microsoft Edge | Required for `--browser=edge` local runs |
| Git | To clone the repository |
| (Optional) Docker | For containerized execution |
| (Optional) Allure CLI | For Allure interactive HTML reports |
| (Optional) BrowserStack account | For cloud grid execution |

**Driver management:** Browser binaries are located automatically. The framework uses **`webdriver-manager`** to download matching drivers, with **Selenium Manager** as an automatic fallback — no manual driver installation is needed.

---

## 2. Clone the Repository

```bash
git clone <repository-url>
cd Enterprise_Selenium_Python_Automation_Framework
```

---

## 3. Create a Virtual Environment

Isolating dependencies is strongly recommended.

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If execution policy blocks activation, run PowerShell as Administrator once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` declares minimum versions (`>=`), so compatible newer releases are allowed.

Key packages (verified versions):

| Package | Verified |
|---------|----------|
| pytest | 9.1.1 |
| selenium | 4.46.0 |
| webdriver-manager | 4.1.2 |
| pytest-xdist | 3.8.0 |
| pytest-rerunfailures | 16.4 |
| pytest-timeout | 2.4.0 |
| pytest-html | 4.2.0 |
| allure-pytest | 2.16.0 |
| openpyxl | 3.1.5 |
| pandas | 3.0.5 |
| PyYAML | 6.0.3 |
| SQLAlchemy | 2.0.51 |
| PyMySQL | 1.2.0 |
| python-dotenv | 1.2.2 |
| requests | 2.34.2 |
| browserstack-local | 1.2.15 |

---

## 6. Verify the Installation

```bash
python -m pytest --version
python -c "import selenium; print(selenium.__version__)"
python -m pytest --collect-only -q
```

The last command should report `181 tests collected`.

---

## 7. First Run

```bash
pytest --browser=chrome --headless
```

Results land under `reports/`:

- `reports/dashboard.html` — enterprise analytics dashboard
- `reports/html/report.html` — self-contained pytest-html report
- `reports/junit/results.xml` — JUnit XML for CI
- `reports/allure-results/` — Allure telemetry
- `reports/executions/EXEC-*.json` — JSON telemetry

---

## 8. Optional: Allure CLI

The Python package `allure-pytest` only **writes telemetry files**. To view the interactive Allure report, install the Allure command-line tool separately.

- **macOS:** `brew install allure`
- **Windows (Scoop):** `scoop install allure`
- **Windows (Chocolatey):** `choco install allure`
- **Manual:** download from the [Allure releases page](https://github.com/allure-framework/allure-core/releases) and add `allure/bin` to `PATH`.

Verify: `allure --version`

Generate and view:

```bash
pytest --alluredir=reports/allure-results --browser=chrome --headless
allure serve reports/allure-results
```

---

## 9. Optional: Docker

```bash
docker build -t enterprise-selenium-framework .
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -v ${PWD}/screenshots:/app/screenshots \
  -v ${PWD}/logs:/app/logs \
  enterprise-selenium-framework
```

Or orchestrated:

```bash
docker compose up --build
```

The container defaults to **Chrome headless, `-n auto` workers, and 1 rerun**. See [docker.md](docker.md).

---

## 10. Optional: BrowserStack

```bash
$env:BROWSERSTACK_USERNAME="your_username"   # PowerShell
$env:BROWSERSTACK_ACCESS_KEY="your_access_key"
pytest --browser=browserstack -m smoke
```

Capabilities are defined in `browserstack.yml`; credentials are read from environment variables. See [browserstack.md](browserstack.md).

---

## 11. Environment Variables

After install, copy the template and fill in non-secret values (or rely on `.env`):

```bash
cp .env.example .env        # Linux/macOS
Copy-Item .env.example .env # Windows PowerShell
```

The framework resolves `${VAR}` placeholders in `config.ini` from environment variables / `.env`. Credentials such as `APP_USERNAME`, `APP_PASSWORD`, `BROWSERSTACK_USERNAME`, and `BROWSERSTACK_ACCESS_KEY` must be provided or the corresponding tests will fail to resolve configuration.

---

## 12. Troubleshooting the Install

| Symptom | Fix |
|---------|-----|
| `pytest` not recognized | venv not activated; activate it, or run `python -m pytest`. |
| `ModuleNotFoundError` | `pip install -r requirements.txt` again inside the activated venv. |
| Driver binary not found | Confirm the browser is installed; `webdriver-manager` + Selenium Manager handle the rest. |
| Allure command not found | Install the Allure CLI (Python package does not include it). |
| Import errors on Windows path names | Run from the repository root. |

See [troubleshooting.md](troubleshooting.md) for more.