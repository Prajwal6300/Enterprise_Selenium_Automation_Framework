# Configuration

All runtime configuration is centralized in **`src/config/config.ini`** and read by **`ConfigReader`** (`src/config/config_reader.py`). There is **no `config/config.ini` at the repository root** — the file lives under `src/config/`.

---

## 1. How Configuration Is Loaded

`ConfigReader` is a singleton that:

1. Parses `src/config/config.ini` using `configparser` with interpolation.
2. Resolves `${VAR}` placeholders against environment variables and the local `.env` file (via python-dotenv).
3. Exposes typed getters:
   - `get_framework()` — active environment, default browser, headless default
   - `get_environment()` — base URL, credentials, timeouts for the active env
   - `get_browser_config()` — per-browser options
   - `get_browserstack_capabilities()` — cloud capabilities
   - `get_timeouts()` — wait/load/retry thresholds
   - `get(section, key)` — generic access

This means **secrets (passwords, API keys, BrowserStack credentials) never appear in source files**. Provide them as environment variables or in `.env`.

---

## 2. Config File Location

```text
src/config/config.ini
```

A safe template for environment variables is provided at the repository root: `.env.example`. Copy it to `.env` and fill in values:

```bash
cp .env.example .env        # Linux/macOS
Copy-Item .env.example .env # Windows PowerShell
```

---

## 3. Config File Sections

### 3.1 `[framework]`

| Key | Default | Purpose |
|-----|---------|---------|
| `environment` | `qa` | Active environment section (`qa`, `staging`, `production`) |
| `default_browser` | `chrome` | Browser used when no `--browser` flag / `BROWSER` env is given |
| `default_headless` | `false` | Headless mode when no `--headless` flag / `HEADLESS` env is given |

### 3.2 `[qa]`, `[staging]`, `[production]`

Environment-specific settings (the active one is selected by `[framework].environment`):

| Key | Purpose |
|-----|---------|
| `base_url` | Application base URL (SauceDemo) |
| `username` / `password` | Login credentials (typically `${VAR}` placeholders) |
| `app_username` / `app_password` | Alternate credential keys resolved from env |

### 3.3 `[chrome]`, `[firefox]`, `[edge]`

Per-browser settings:

| Key | Purpose |
|-----|---------|
| `headless` | Headless default for this browser |
| `window_width` / `window_height` | Browser window size |

### 3.4 `[browserstack]`

| Key | Purpose |
|-----|---------|
| `username` / `access_key` | BrowserStack credentials (env placeholders) |
| `browser`, `os`, `os_version`, `browser_version` | Default cloud capability overrides |
| `local` | Enable BrowserStack Local tunnel |

The full capability matrix lives in `browserstack.yml` at the repository root (see [browserstack.md](browserstack.md)).

### 3.5 `[timeouts]`

| Key | Default | Purpose |
|-----|---------|---------|
| `implicit_wait` | `10` | Selenium implicit wait (seconds) |
| `explicit_wait` | `15` | Default explicit-wait timeout (seconds) |
| `page_load_wait` | `30` | Page-load readiness timeout (seconds) |
| `api_timeout` | `10` | API request timeout (seconds) |
| `db_timeout` | `5` | Database operation timeout (seconds) |
| `retry_count` | `3` | API retry / soft-assert retries |

---

## 4. Precedence

Values are resolved in this order (highest wins):

1. **CLI flags** — `--browser`, `--headless`
2. **Environment variables** — `BROWSER`, `HEADLESS`, `ENV`, `BASE_URL`, `APP_USERNAME`, `APP_PASSWORD`, `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`, etc.
3. **`.env` file** — loaded by python-dotenv
4. **`config.ini`** — section defaults

Example: `pytest --browser=firefox` overrides the `default_browser=chrome` from `[framework]` and the `BROWSER` environment variable.

---

## 5. Supported Environment Variables

| Variable | Purpose |
|----------|---------|
| `BROWSER` | Browser name: `chrome`, `firefox`, `edge`, `browserstack` |
| `HEADLESS` | `true`/`false` |
| `ENV` | Active environment: `qa`, `staging`, `production` |
| `BASE_URL` | Overrides the environment `base_url` |
| `APP_USERNAME` | UI login username |
| `APP_PASSWORD` | UI login password |
| `BROWSERSTACK_USERNAME` | BrowserStack username |
| `BROWSERSTACK_ACCESS_KEY` | BrowserStack access key |

---

## 6. Environment Switching

```bash
# QA (default)
pytest

# Staging
$env:ENV="staging"            # PowerShell
export ENV=staging            # Bash
pytest --browser=chrome --headless
```

The active environment changes which `base_url`, credentials, and timeouts `ConfigReader.get_environment()` returns.

---

## 7. Important Limitation

**Changing `base_url` alone does not make the framework automate another website.**

The Page Objects in `src/pages/` contain locators specific to **SauceDemo's DOM** (e.g., `#user-name`, `#login-button`, `.inventory_item`). Pointing `base_url` at a different site will produce `LocatorNotFoundError` because the selectors do not match.

To automate a different application you must write new Page Objects for that application's markup (see [development-guide.md](development-guide.md)). The framework's infrastructure — waits, screenshots, logging, reporting, data providers — is reusable as-is.

---

## 8. Validation Checklist

After changing configuration:

```bash
# Confirm the config parses and shows the active environment
python -m pytest --collect-only -q

# Quick smoke to prove the browser + base_url combo works
pytest -m smoke --browser=chrome --headless
```
