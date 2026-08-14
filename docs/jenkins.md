# Jenkins

Run the suite in Jenkins using the declarative **`Jenkinsfile`** at the repository root.

---

## 1. Pipeline Overview

| Stage | Steps |
|-------|-------|
| **Checkout** | `checkout scm` |
| **Setup** | Create `.venv`, upgrade pip, install `requirements.txt` |
| **Test** | Run pytest with `--browser=<param> --headless? -n auto --reruns 1` and JUnit output |

### Build parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `BROWSER` | choice | `chrome` | `chrome`, `firefox`, `edge`, `browserstack` |
| `HEADLESS` | boolean | `true` | — |

---

## 2. Post-Build Reporting

In the `post { always { ... } }` block, the pipeline:

1. **Publishes the dashboard** — `publishHTML` for `reports/dashboard.html` as *"Enterprise Test Automation Dashboard"*, linking to the last build.
2. **Archives artifacts** — screenshots (`screenshots/**/*.png`), logs (`logs/**/*.log`), and all reports (`reports/**/*`).
3. **Records JUnit results** — `junit` reads `reports/junit/results.xml`.

---

## 3. Setting Up a Job

1. Create a **Multibranch Pipeline** (or Pipeline) job pointing at the repository.
2. Pipeline script: **Pipeline script from SCM** → `Jenkinsfile`.
3. Ensure the agent has:
   - Python 3.10+ available on `PATH`
   - The target browser(s) installed (Chrome/Firefox/Edge) for local runs, **or** BrowserStack credentials for `--browser=browserstack`

---

## 4. BrowserStack in Jenkins

When `BROWSER=browserstack`, set credentials as environment variables on the agent (or Jenkins credentials binding):

```text
BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESS_KEY
```

They are consumed by `ConfigReader` from the `[browserstack]` section of `src/config/config.ini`.

---

## 5. Interpreting Results

- The **publishHTML** report is the executive dashboard (`reports/dashboard.html`).
- The **JUnit** trend shows pass/fail history per test.
- **Archive** contains evidence: failure screenshots and `logs/framework.log`.

---

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `python: command not found` | Install Python on the agent and ensure it is on `PATH` |
| Browser not installed on agent | Install Chrome/Firefox/Edge, or switch to `--browser=browserstack` |
| JUnit result empty | Check `reports/junit/results.xml` exists (pytest generates it via `addopts`/`--junitxml`) |
| Dashboard missing | `publishHTML` uses `allowMissing: true`, so verify `reports/dashboard.html` was generated |

See [troubleshooting.md](troubleshooting.md) for general issues.
