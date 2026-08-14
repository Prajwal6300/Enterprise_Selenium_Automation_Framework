# GitHub Actions

Continuous regression runs via the workflow at **`.github/workflows/regression.yml`** (workflow name: *Enterprise Selenium Test Automation Pipeline*).

---

## 1. Triggers

| Trigger | Detail |
|---------|--------|
| `push` | Branches `main`, `master`, `develop` |
| `pull_request` | Branches `main`, `master` |
| `schedule` | Daily at `00:00` UTC (`cron: '0 0 * * *'`) |
| `workflow_dispatch` | Manual trigger with inputs `browser` (chrome/firefox/edge) and `headless` (boolean) |

---

## 2. Job Summary

Runs on `ubuntu-latest` with Python **3.12**:

| Step | Purpose |
|------|---------|
| Checkout | `actions/checkout@v4` |
| Set up Python | `actions/setup-python@v5`, version `3.12`, pip cache |
| Install Chrome | `google-chrome-stable` |
| Install Firefox ESR | When `browser` is `firefox` or `chrome` |
| Install Edge | When `browser` is `edge` (Microsoft repo) |
| Install deps | `pip install -r requirements.txt` |
| Execute pytest | `--browser=<input> <--headless> -n 2 --reruns 1` with HTML, Allure, JUnit flags |

The test step sets environment variables `CI_SYSTEM=GitHub Actions` and `HEADLESS=<input>`.

---

## 3. Artifacts Uploaded (always, even on failure)

| Artifact | Path |
|----------|------|
| `executive-dashboard` | `reports/dashboard.html` |
| `html-test-report` | `reports/html/` |
| `junit-xml-results` | `reports/junit/` |
| `execution-telemetry` | `reports/executions/` |
| `allure-results` | `reports/allure-results/` |
| `failure-screenshots` | `screenshots/failures/` |

All use `actions/upload-artifact@v4` with `if: always()`.

---

## 4. Manual Run

From the **Actions** tab → *Enterprise Selenium Test Automation Pipeline* → **Run workflow**:

```text
browser : chrome | firefox | edge
headless: true/false
```

---

## 5. Scheduling

The daily `00:00 UTC` cron keeps a nightly regression baseline. Adjust `cron` in the `schedule` block as needed (GitHub only guarantees best-effort scheduling).

---

## 6. Downloading Results

From the workflow run page → **Artifacts**, download the dashboard/HTML/JUnit/Allure/telemetry/screenshots zips.

---

## 7. Notes & Limitations

- **Default browser** in `workflow_dispatch` is `chrome`; the workflow uses `${{ inputs.browser || 'chrome' }}` as a fallback for push/PR/schedule runs.
- **Headless** is enabled by default (`HEADLESS` input default `true`); the step converts it to the `--headless` flag.
- BrowserStack is **not** configured in this workflow — use `workflow_dispatch` on a self-hosted runner or [Jenkins](jenkins.md) / [BrowserStack](browserstack.md) for cloud execution.
- The full 181-test suite may exceed a single CI run's patience; use `-m smoke` or `-m regression` in the `pytest` step to scope runs.

See [troubleshooting.md](troubleshooting.md) for general issues.
