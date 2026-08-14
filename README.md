# 🚀 Enterprise Selenium Python Test Automation Framework

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/selenium-v4.28.1-green.svg)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-v9.1.1-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20%7C%20Jenkins-orange.svg)](.github/workflows/regression.yml)
[![Cloud Grid](https://img.shields.io/badge/Cloud%20Grid-BrowserStack-informational.svg)](browserstack.yml)   

An **enterprise-grade, scalable, and modular test automation framework** built using **Python**, **Selenium WebDriver**, **pytest**, and the **Page Object Model (POM)** pattern.

This framework is designed for production Web UI testing, REST API automation, database data-integrity validation, cross-browser cloud execution (BrowserStack), Docker containerization, and continuous integration (Jenkins & GitHub Actions). 

---

## 📸 Enterprise Dashboard Preview

The framework generates a commercial-grade, light-themed executive dashboard (`reports/dashboard.html`) after every test execution:

- **Executive Summary KPI Cards**: Total Tests, Passed, Failed, Skipped, Execution Time, and Success Rate with count-up animations.
- **Interactive Chart.js Visualizers**: Pass vs Fail Doughnut, Runtime Trend Line Chart, Module Distribution Bar Chart, Test Duration Breakdown, Browser Breakdown, and Quality Score Gauge.
- **Searchable, Sortable & Paginated Test Table**: Real-time filtering, column sorting, pagination controls, failure screenshot inspection modals, and log code viewer modals.
- **Multi-Format Reports Export**: PDF, Excel, and CSV table generation.

---

## 🏗️ Architecture & Component Design

```mermaid
graph TD
    A[Pytest Runner / CLI] --> B[conftest.py Hooks & Fixtures]
    B --> C[BrowserFactory / Selenium Manager]
    B --> D[ConfigReader & DataProvider]
    
    C --> E[Selenium WebDrivers - Chrome / Firefox / Edge / BrowserStack]
    D --> F[Excel / CSV / JSON Test Data]

    subgraph "Core Architecture Layer"
        G[BaseTest & BasePage]
        H[WaitHelper & Screenshot & Logger]
        I[APIClient & DBUtility]
    end

    subgraph "Page Object Model (POM)"
        J[LoginPage]
        K[HomePage]
        L[ProductPage]
        M[CartPage]
        N[CheckoutPage]
    end   

    subgraph "Test Execution Suites"
        O[test_login.py]
        P[test_search.py]
        Q[test_cart.py]
        R[test_checkout.py]
        S[test_logout.py]
        T[test_api_workflow.py]
        U[test_db_validation.py]
    end

    E --> G
    F --> G
    G --> J & K & L & M & N
    J & K & L & M & N --> O & P & Q & R & S
    I --> T & U

    O & P & Q & R & S & T & U --> V[Light Enterprise Dashboard / Allure Reports / Failure Screenshots]
```

---

## 📂 Repository Directory Layout

```
Enterprise_Selenium_Python_Automation_Framework/
├── .github/
│   └── workflows/
│       └── regression.yml          # GitHub Actions CI/CD pipeline
├── ci/                             # CI scripts and configs
├── docker/                         # Docker environment configurations
├── docs/                           # Framework architecture documentation
├── drivers/                        # Local driver cache directory
├── logs/                           # Automated framework execution logs
├── reports/                        # Execution HTML, Allure, & JUnit XML reports
│   └── dashboard.html              # Premium Enterprise Executive HTML Dashboard
├── screenshots/                    # Failure screenshot capture store
│   └── failures/
├── src/
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
```

---

## ⚡ Quick Start & Installation & run

### 1. Prerequisites
- Python 3.10+ installed
- Git installed
- Google Chrome / Mozilla Firefox / Microsoft Edge browser

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/Enterprise_Selenium_Python_Automation_Framework.git
cd Enterprise_Selenium_Python_Automation_Framework

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
```

---

## 🚀 Execution Commands

### Local Web Execution
```bash
# Execute suite headlessly on Chrome (Default)
pytest --browser=chrome --headless

# Execute suite on Firefox or Edge
pytest --browser=firefox --headless
pytest --browser=edge --headless
```

### Parallel Execution (pytest-xdist)
```bash
# Run test suite across CPU cores in parallel
pytest -n auto --headless
```

### Pytest Marker Filtering
```bash
pytest -m smoke --headless       # Run Smoke suite
pytest -m regression --headless  # Run Regression suite
pytest -m api                    # Run REST API suite
pytest -m db                     # Run Database Validation suite
```

---

## ☁️ Cloud & Container Execution

### BrowserStack Cloud Grid
```bash
# Set BrowserStack Credentials
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"

# Execute suite on BrowserStack
pytest --browser=browserstack
```

### Docker Containerization
```bash
# Build and run container suite via Docker Compose
docker-compose up --build
```

---

## 🛠️ CI/CD Pipeline Support

- **GitHub Actions**: Configured in `.github/workflows/regression.yml`. Automatically runs regression suite on every push and pull request to `main`.
- **Jenkins CI**: Configured in `Jenkinsfile`. Includes declarative stages for dependency installation, parallel execution, HTML report publishing (`reports/dashboard.html`), and failure screenshot archiving.

---

## ❓ Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `WebDriverException` | Missing or outdated browser binary | The framework uses Selenium 4's built-in `SeleniumManager` with automatic fallback. Ensure browser is installed. |
| `FileNotFoundError` | Excel data file missing | Run `pytest` commands directly from the project root directory. |
| `MemoryError` in driver manager | Network rate limit on driver API | `BrowserFactory` automatically handles fallbacks without failing test setup. |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
