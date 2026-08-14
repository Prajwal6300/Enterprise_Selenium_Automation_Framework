# Docker

Containerize the Selenium test suite with the provided `Dockerfile` and `docker-compose.yml`.

---

## 1. Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Builds a `python:3.12-slim` image with Chromium + Firefox ESR, installs requirements, and defaults to running the full suite |
| `docker-compose.yml` | Orchestrates a single container with env vars and report volume mounts |

---

## 2. Dockerfile Highlights

```dockerfile
FROM python:3.12-slim
...
RUN apt-get install -y chromium firefox-esr ...
CMD ["pytest", "--browser=chrome", "--headless", "-n", "auto", "--reruns", "1"]
```

- Base image: `python:3.12-slim`
- Browsers installed: **Chromium** and **Firefox ESR**
- Default command: Chrome headless, auto-parallel workers, 1 rerun

---

## 3. Build and Run Manually

```bash
# Build
docker build -t enterprise-selenium-framework .

# Run, mounting report/screenshot/log output
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -v ${PWD}/screenshots:/app/screenshots \
  -v ${PWD}/logs:/app/logs \
  enterprise-selenium-framework
```

After the run, `reports/`, `screenshots/`, and `logs/` are populated on your host.

### Overriding the command

```bash
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -v ${PWD}/screenshots:/app/screenshots \
  -v ${PWD}/logs:/app/logs \
  enterprise-selenium-framework \
  pytest --browser=chrome --headless -m smoke
```

---

## 4. Using docker-compose

`docker-compose.yml` defines the `test-automation` service with:

- Environment: `BROWSER=chrome`, `HEADLESS=true`, `ENV=qa`, plus BrowserStack credential passthrough
- Volumes: `./reports`, `./screenshots`, `./logs`
- Command: `pytest --browser=chrome --headless -n 2 --reruns 1 --html=reports/html/report.html --alluredir=reports/allure-results`

```bash
docker compose up --build
```

The BrowserStack variables are passed from your shell:

```bash
$env:BROWSERSTACK_USERNAME="your_username"   # PowerShell
$env:BROWSERSTACK_ACCESS_KEY="your_access_key"
docker compose up --build
```

---

## 5. Outputs

After a container run, on the host:

```text
reports/
├── dashboard.html
├── html/report.html
├── junit/results.xml
├── allure-results/
└── executions/EXEC-*.json
screenshots/failures/*.png
logs/framework.log
```

---

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Container exits with browser error | Confirm Chromium/Firefox present; run with `--headless` (default) |
| Empty reports | Ensure the `-v` volume mounts point to the working directory |
| Slow first build | Expected — image downloads browsers; layer cache helps on rebuild |
| Edge not available | The image installs Chromium + Firefox ESR only; use Chrome/Firefox inside Docker |

See [troubleshooting.md](troubleshooting.md) for general issues.
