# BrowserStack

Run the Selenium suite on the **BrowserStack** cloud grid through `--browser=browserstack`.

---

## 1. Prerequisites

- A BrowserStack account.
- Environment variables or `.env` entries:

```bash
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

> **Never commit real credentials.** They are resolved from environment variables by `ConfigReader` and read from the `[browserstack]` section of `src/config/config.ini` (`${BROWSERSTACK_USERNAME}` / `${BROWSERSTACK_ACCESS_KEY}`).

---

## 2. Configuration Files

### 2.1 `browserstack.yml` (repository root)

The cloud capability matrix:

| Setting | Value |
|---------|-------|
| `framework` | `pytest` |
| Platform 1 | Windows 11 / Chrome (latest) |
| Platform 2 | OS X Ventura / Safari (latest) |
| `parallelsPerPlatform` | 2 |
| `browserstackLocal` | false |
| `debug` | true |
| `networkLogs` | true |
| `consoleLogs` | info |

Credentials are injected from `${BROWSERSTACK_USERNAME}` and `${BROWSERSTACK_ACCESS_KEY}`.

### 2.2 `src/config/config.ini` → `[browserstack]`

Runtime capabilities used by `BrowserFactory` for the local driver include browser, OS, OS version, browser version, and the `local` tunnel flag.

---

## 3. Running on BrowserStack

```bash
# PowerShell
$env:BROWSERSTACK_USERNAME="your_username"
$env:BROWSERSTACK_ACCESS_KEY="your_access_key"
pytest --browser=browserstack -m smoke

# Bash
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"
pytest --browser=browserstack -m smoke
```

`BrowserFactory._create_browserstack()` builds the cloud WebDriver using the resolved credentials and capabilities.

---

## 4. What Happens on the Grid

1. The test requests a browser via `--browser=browserstack`.
2. `BrowserFactory` creates a `WebDriver` pointed at BrowserStack's hub using your capabilities.
3. The same Page Objects, waits, screenshots, and reporting run unchanged.
4. Results, videos, and logs appear in your BrowserStack Automate dashboard.

---

## 5. Common Commands

```bash
# Smoke on the cloud
pytest --browser=browserstack -m smoke

# Full cloud regression
pytest --browser=browserstack -m regression

# Parallel cloud workers
pytest --browser=browserstack -n 4 -m smoke
```

---

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `BrowserInitializationError` / auth failure | Confirm `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY` are set |
| Locator timeouts on Safari | BrowserStack platform provisioning may be slower; increase `[timeouts].explicit_wait` |
| Build name not visible | Values in `browserstack.yml` (`buildName`, `projectName`) control grid grouping |

See [troubleshooting.md](troubleshooting.md) for general issues.
