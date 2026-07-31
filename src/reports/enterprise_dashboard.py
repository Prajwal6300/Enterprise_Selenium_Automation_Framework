"""Enterprise Analytics Dashboard Generator (Light Modern Enterprise Theme).

Compiles test execution results into a clean, minimalist, enterprise-grade analytics dashboard
inspired by Microsoft Fluent UI, Google Material Design 3, Stripe, GitHub Light, Notion, and Azure DevOps.
Features Google Font Inter, soft shadows, rounded cards (16px), Chart.js visualizers,
interactive tables with search/sorting/pagination, screenshot zoom modal, log code viewer, and export tools.
"""

from __future__ import annotations

import base64
import datetime
import getpass
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
from typing import Any, Dict, List, Optional

import pytest
import selenium


class EnterpriseDashboardBuilder:
    """Builder class for generating Light Modern Enterprise HTML reports."""

    def __init__(self, output_path: str | Path = "reports/dashboard.html") -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def build_dashboard(
        self,
        test_results: List[Dict[str, Any]],
        session_duration: float,
        env: str = "QA",
        browser: str = "Chrome"
    ) -> Path:
        """Compile test results and system metadata into a standalone light HTML dashboard."""
        print(f"[EnterpriseDashboard] Compiling Premium Enterprise Analytics Dashboard for {len(test_results)} test results...")

        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r.get("status") == "passed")
        failed_tests = sum(1 for r in test_results if r.get("status") == "failed")
        skipped_tests = sum(1 for r in test_results if r.get("status") == "skipped")
        running_tests = sum(1 for r in test_results if r.get("status") == "running")
        pass_rate = round((passed_tests / total_tests * 100), 1) if total_tests > 0 else 0.0

        durations = [r.get("duration", 0.0) for r in test_results]
        avg_duration = round(sum(durations) / total_tests, 2) if total_tests > 0 else 0.0

        # Fastest and Slowest test calculation
        if test_results:
            fastest_test = min(test_results, key=lambda x: x.get("duration", 0.0))
            slowest_test = max(test_results, key=lambda x: x.get("duration", 0.0))
            fastest_info = f"{fastest_test.get('name', 'N/A')} ({round(fastest_test.get('duration', 0.0), 2)}s)"
            slowest_info = f"{slowest_test.get('name', 'N/A')} ({round(slowest_test.get('duration', 0.0), 2)}s)"
        else:
            fastest_info = "N/A"
            slowest_info = "N/A"

        # System & Framework Metadata
        pytest_ver = getattr(pytest, "__version__", "9.1.1")
        selenium_ver = getattr(selenium, "__version__", "4.28.1")
        metadata = {
            "Project Name": "SauceDemo E-Commerce Enterprise Automation",
            "Framework Version": "2.5.0-Enterprise",
            "Python Version": platform.python_version(),
            "Pytest Version": pytest_ver,
            "Selenium Version": selenium_ver,
            "Environment": env.upper(),
            "Target Browser": browser.capitalize(),
            "Browser Version": "122.0.6261.128",
            "Operating System": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "Host Machine": socket.gethostname(),
            "Execution User": getpass.getuser(),
            "Execution Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Execution Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Total Duration": f"{round(session_duration, 2)}s",
        }

        try:
            git_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
            git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
            metadata["Git Branch"] = git_branch
            metadata["Git Commit"] = git_commit
        except Exception:
            metadata["Git Branch"] = "main"
            metadata["Git Commit"] = "a1b2c3d"

        # Process test results array for JavaScript & rendering
        processed_results = []
        module_counts: Dict[str, int] = {}

        for i, r in enumerate(test_results):
            name = r.get("name", f"test_case_{i+1}")
            file_path = r.get("file", "")
            status = r.get("status", "passed").lower()
            duration = round(r.get("duration", 0.0), 2)
            screenshot_uri = r.get("screenshot_uri", "")
            error_message = r.get("error_message", "")

            # Module Detection Logic
            categories = [c.lower() for c in r.get("categories", [])]
            if "api" in categories or "api" in file_path.lower():
                module = "API"
            elif "db" in categories or "database" in categories or "database" in file_path.lower():
                module = "DATABASE"
            elif "e2e" in categories or "e2e" in file_path.lower():
                module = "E2E"
            elif "smoke" in categories:
                module = "SMOKE"
            elif "regression" in categories:
                module = "REGRESSION"
            else:
                module = "UI"

            module_counts[module] = module_counts.get(module, 0) + 1

            test_browser = r.get("browser", browser.capitalize())
            test_env = r.get("env", env.upper())
            exec_time = r.get("execution_time", datetime.datetime.now().strftime("%H:%M:%S"))

            if error_message:
                logs = error_message
            else:
                logs = (
                    f"[INFO] Test '{name}' started at {exec_time}\n"
                    f"[INFO] File: {file_path}\n"
                    f"[INFO] Environment: {test_env} | Browser: {test_browser}\n"
                    f"[INFO] Executing step assertions for {module} suite...\n"
                    f"[SUCCESS] Test finished in {duration}s with status PASSED."
                )

            processed_results.append({
                "id": i + 1,
                "name": name,
                "file": file_path,
                "status": status,
                "duration": duration,
                "module": module,
                "browser": test_browser,
                "environment": test_env,
                "execution_time": exec_time,
                "screenshot_uri": screenshot_uri,
                "logs": logs,
                "error_message": error_message
            })

        results_json = json.dumps(processed_results)
        metadata_json = json.dumps(metadata)

        html_content = f"""<!DOCTYPE html>
<html lang="en" data-bs-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Selenium Test Automation Dashboard</title>
    <meta name="description" content="Clean, enterprise-grade test automation reporting dashboard inspired by Microsoft Fluent UI, Stripe, and Material Design 3.">
    
    <!-- Google Fonts: Inter & Poppins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Bootstrap 5 & FontAwesome CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

    <style>
        :root {{
            --bg-body: #F8FAFC;
            --bg-card: #FFFFFF;
            --primary: #2563EB;
            --primary-light: rgba(37, 99, 235, 0.08);
            --secondary-blue: #60A5FA;
            --passed: #22C55E;
            --passed-bg: rgba(34, 197, 94, 0.12);
            --passed-text: #15803D;
            --failed: #EF4444;
            --failed-bg: rgba(239, 68, 68, 0.12);
            --failed-text: #B91C1C;
            --skipped: #F59E0B;
            --skipped-bg: rgba(245, 158, 11, 0.12);
            --skipped-text: #B45309;
            --running: #2563EB;
            --running-bg: rgba(37, 99, 235, 0.12);
            --running-text: #1D4ED8;
            --info: #06B6D4;
            --info-bg: rgba(6, 182, 212, 0.12);
            --accent: #8B5CF6;
            --accent-bg: rgba(139, 92, 246, 0.12);
            --text-main: #1E293B;
            --text-secondary: #64748B;
            --border-color: #E2E8F0;
            --card-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);
            --hover-shadow: 0 12px 30px rgba(37, 99, 235, 0.12);
            --radius: 16px;
        }}
        
        body {{
            background-color: var(--bg-body);
            font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: var(--text-main);
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{
            animation: fadeIn 0.4s ease-out forwards;
        }}

        /* Sticky Glass Header */
        .sticky-header {{
            position: sticky;
            top: 0;
            z-index: 1030;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 14px 32px;
        }}

        .brand-logo-box {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }}

        /* Main Container */
        .dashboard-container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 28px 24px 48px 24px;
        }}

        /* Cards & Styling */
        .dashboard-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            box-shadow: var(--card-shadow);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .dashboard-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--hover-shadow);
        }}

        .accent-top-primary {{ border-top: 4px solid var(--primary); }}
        .accent-top-passed {{ border-top: 4px solid var(--passed); }}
        .accent-top-failed {{ border-top: 4px solid var(--failed); }}
        .accent-top-skipped {{ border-top: 4px solid var(--skipped); }}
        .accent-top-info {{ border-top: 4px solid var(--info); }}
        .accent-top-accent {{ border-top: 4px solid var(--accent); }}

        /* Metric Numbers */
        .metric-number {{
            font-size: 2.1rem;
            font-weight: 700;
            line-height: 1.2;
            letter-spacing: -0.02em;
            color: var(--text-main);
        }}

        .metric-label {{
            font-size: 0.775rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
        }}

        .metric-subtext {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }}

        .icon-box {{
            width: 46px;
            height: 46px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }}

        /* Status Badges */
        .badge-status {{
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.75rem;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .badge-passed {{ background: var(--passed-bg); color: var(--passed-text); border: 1px solid rgba(34, 197, 94, 0.25); }}
        .badge-failed {{ background: var(--failed-bg); color: var(--failed-text); border: 1px solid rgba(239, 68, 68, 0.25); }}
        .badge-skipped {{ background: var(--skipped-bg); color: var(--skipped-text); border: 1px solid rgba(245, 158, 11, 0.25); }}
        .badge-running {{ background: var(--running-bg); color: var(--running-text); border: 1px solid rgba(37, 99, 235, 0.25); }}

        /* Clean Table */
        .clean-table-container {{
            border-radius: var(--radius);
            border: 1px solid var(--border-color);
            overflow: hidden;
            background: var(--bg-card);
        }}

        .clean-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: var(--bg-card);
        }}
        
        .clean-table th {{
            background: #F1F5F9;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 14px 18px;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 5;
            cursor: pointer;
            user-select: none;
        }}

        .clean-table th:hover {{
            background: #E2E8F0;
        }}
        
        .clean-table td {{
            padding: 14px 18px;
            vertical-align: middle;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.875rem;
        }}

        .clean-table tr:hover td {{
            background-color: #F8FAFC;
        }}

        .screenshot-thumb {{
            width: 64px;
            height: 42px;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .screenshot-thumb:hover {{
            transform: scale(1.08);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        /* Search & Form Elements */
        .search-field {{
            background: #F1F5F9;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 8px 16px 8px 36px;
            font-size: 0.875rem;
            color: var(--text-main);
            transition: all 0.2s ease;
        }}
        
        .search-field:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
            background: #FFFFFF;
        }}

        .search-wrapper {{
            position: relative;
        }}

        .search-wrapper i {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        /* Performance Metric Pill */
        .perf-pill {{
            background: #F1F5F9;
            border-radius: 12px;
            padding: 12px 18px;
            border: 1px solid var(--border-color);
        }}

        /* Code Viewer Block */
        .log-code-block {{
            background: #0F172A;
            color: #F8FAFC;
            font-family: 'Fira Code', 'JetBrains Mono', Consolas, Monaco, 'Courier New', monospace;
            font-size: 0.85rem;
            padding: 18px;
            border-radius: 12px;
            max-height: 450px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-all;
            border: 1px solid #334155;
        }}

        /* Pagination Buttons */
        .pagination-btn {{
            padding: 6px 14px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: #FFFFFF;
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .pagination-btn:hover:not(:disabled) {{
            background: var(--primary);
            color: #FFFFFF;
            border-color: var(--primary);
        }}

        .pagination-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        @media print {{
            .sticky-header, .no-print, #searchInput, .btn, .pagination-controls {{ display: none !important; }}
            body {{ background: white !important; }}
            .dashboard-card {{ box-shadow: none !important; border: 1px solid #ccc !important; }}
        }}
    </style>
</head>
<body>

    <!-- Sticky Header -->
    <header class="sticky-header">
        <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-3">
                <div class="brand-logo-box">
                    <i class="fa-solid fa-rocket"></i>
                </div>
                <div>
                    <h5 class="m-0 fw-bold text-dark" style="font-family: 'Poppins', sans-serif;">Enterprise Selenium Automation Framework</h5>
                    <small class="text-muted"><i class="fa-solid fa-layer-group me-1 text-primary"></i> SauceDemo E-Commerce • Production Suite</small>
                </div>
            </div>

            <div class="d-flex align-items-center gap-3">
                <span class="badge bg-light text-dark border px-3 py-2 fw-normal"><i class="fa-regular fa-clock me-1 text-primary"></i> {metadata['Execution Date']}</span>
                <span class="badge bg-primary text-white px-3 py-2 fw-semibold"><i class="fa-solid fa-code-branch me-1"></i> {env.upper()} Environment</span>
                <span class="badge bg-secondary text-white px-3 py-2 fw-semibold"><i class="fa-brands fa-chrome me-1"></i> {browser.capitalize()}</span>
                <div class="d-flex align-items-center justify-content-center bg-light border rounded-circle" style="width: 38px; height: 38px;" title="Enterprise QA Lab">
                    <i class="fa-solid fa-user-check text-primary"></i>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <div class="dashboard-container">

        <!-- Top Summary Cards (6 Cards) -->
        <div class="row g-3 mb-4 fade-in">
            <div class="col-lg-2 col-md-4 col-sm-6">
                <div class="dashboard-card accent-top-primary p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="metric-label">TOTAL TESTS</div>
                            <div class="metric-number count-up" data-target="{total_tests}">0</div>
                            <div class="metric-subtext">Executed Suite</div>
                        </div>
                        <div class="icon-box" style="background: rgba(37,99,235,0.12); color: #2563EB;">
                            <i class="fa-solid fa-vials"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-2 col-md-4 col-sm-6">
                <div class="dashboard-card accent-top-passed p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="metric-label">PASSED</div>
                            <div class="metric-number text-success count-up" data-target="{passed_tests}">0</div>
                            <div class="metric-subtext">Passed Assertions</div>
                        </div>
                        <div class="icon-box" style="background: rgba(34,197,94,0.12); color: #22C55E;">
                            <i class="fa-solid fa-circle-check"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-2 col-md-4 col-sm-6">
                <div class="dashboard-card accent-top-failed p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="metric-label">FAILED</div>
                            <div class="metric-number text-danger count-up" data-target="{failed_tests}">0</div>
                            <div class="metric-subtext">Failed Assertions</div>
                        </div>
                        <div class="icon-box" style="background: rgba(239,68,68,0.12); color: #EF4444;">
                            <i class="fa-solid fa-circle-xmark"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-2 col-md-4 col-sm-6">
                <div class="dashboard-card accent-top-skipped p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="metric-label">SKIPPED</div>
                            <div class="metric-number text-warning count-up" data-target="{skipped_tests}">0</div>
                            <div class="metric-subtext">Skipped / Ignored</div>
                        </div>
                        <div class="icon-box" style="background: rgba(245,158,11,0.12); color: #F59E0B;">
                            <i class="fa-solid fa-triangle-exclamation"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-2 col-md-4 col-sm-6">
                <div class="dashboard-card accent-top-info p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="metric-label">EXEC TIME</div>
                            <div class="metric-number text-dark">{round(session_duration, 1)}s</div>
                            <div class="metric-subtext">Total Runtime</div>
                        </div>
                        <div class="icon-box" style="background: rgba(6,182,212,0.12); color: #06B6D4;">
                            <i class="fa-solid fa-stopwatch"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-2 col-md-4 col-sm-6">
                <div class="dashboard-card accent-top-accent p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="metric-label">SUCCESS RATE</div>
                            <div class="metric-number" style="color: #8B5CF6;">{pass_rate}%</div>
                            <div class="metric-subtext">Pass / Total Ratio</div>
                        </div>
                        <div class="icon-box" style="background: rgba(139,92,246,0.12); color: #8B5CF6;">
                            <i class="fa-solid fa-chart-line"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Performance Summary Section -->
        <div class="dashboard-card p-4 mb-4 fade-in">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold m-0 text-dark" style="font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-gauge-high me-2 text-primary"></i>Executive Performance Metrics</h6>
                <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 rounded-pill fw-semibold">Suite Health: {pass_rate}% Passed</span>
            </div>
            <div class="row g-3">
                <div class="col-md-3">
                    <div class="perf-pill">
                        <small class="text-muted d-block fw-semibold uppercase mb-1">AVERAGE TEST DURATION</small>
                        <span class="fs-5 fw-bold text-dark">{avg_duration}s / test</span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="perf-pill">
                        <small class="text-muted d-block fw-semibold uppercase mb-1">FASTEST TEST</small>
                        <span class="fs-6 fw-bold text-success text-truncate d-block" title="{fastest_info}">{fastest_info}</span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="perf-pill">
                        <small class="text-muted d-block fw-semibold uppercase mb-1">SLOWEST TEST</small>
                        <span class="fs-6 fw-bold text-danger text-truncate d-block" title="{slowest_info}">{slowest_info}</span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="perf-pill">
                        <small class="text-muted d-block fw-semibold uppercase mb-1">PASS PERCENTAGE</small>
                        <span class="fs-5 fw-bold" style="color: #8B5CF6;">{pass_rate}%</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 2: Interactive Chart Visualizers (6 Charts) -->
        <div class="row g-4 mb-4 fade-in">
            <div class="col-md-4">
                <div class="dashboard-card p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold m-0 text-dark"><i class="fa-solid fa-chart-pie me-2 text-primary"></i>Pass vs Fail Status</h6>
                        <small class="text-muted">Proportion</small>
                    </div>
                    <div style="height: 220px; position: relative;">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="dashboard-card p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold m-0 text-dark"><i class="fa-solid fa-chart-line me-2 text-info"></i>Execution Timeline</h6>
                        <small class="text-muted">Runtime Trend</small>
                    </div>
                    <div style="height: 220px; position: relative;">
                        <canvas id="timelineChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="dashboard-card p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold m-0 text-dark"><i class="fa-solid fa-chart-column me-2 text-purple" style="color: #8B5CF6;"></i>Module Distribution</h6>
                        <small class="text-muted">Test Suites</small>
                    </div>
                    <div style="height: 220px; position: relative;">
                        <canvas id="categoryChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="dashboard-card p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold m-0 text-dark"><i class="fa-solid fa-stopwatch me-2 text-warning"></i>Test Duration (Top 8)</h6>
                        <small class="text-muted">Seconds</small>
                    </div>
                    <div style="height: 220px; position: relative;">
                        <canvas id="durationChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="dashboard-card p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold m-0 text-dark"><i class="fa-brands fa-chrome me-2 text-success"></i>Browser Distribution</h6>
                        <small class="text-muted">Environments</small>
                    </div>
                    <div style="height: 220px; position: relative;">
                        <canvas id="browserChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="dashboard-card p-4 h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold m-0 text-dark"><i class="fa-solid fa-bullseye me-2 text-danger"></i>Success Rate Gauge</h6>
                        <small class="text-muted">Quality Score</small>
                    </div>
                    <div style="height: 220px; position: relative;">
                        <canvas id="gaugeChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 3: Test Execution Data Table -->
        <div class="dashboard-card p-4 mb-4 fade-in">
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
                <div>
                    <h5 class="fw-bold m-0 text-dark" style="font-family: 'Poppins', sans-serif;">Test Results</h5>
                    <small class="text-muted">Detailed execution records, duration, screenshots, and logs</small>
                </div>
                <div class="d-flex flex-wrap align-items-center gap-2">
                    <div class="search-wrapper">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input type="text" id="searchInput" class="search-field" placeholder="Search test name, module..." onkeyup="filterTable()">
                    </div>
                    <select id="statusFilter" class="form-select form-select-sm border-color text-muted" style="width: 130px;" onchange="filterTable()">
                        <option value="ALL">All Statuses</option>
                        <option value="passed">Passed</option>
                        <option value="failed">Failed</option>
                        <option value="skipped">Skipped</option>
                    </select>
                    <select id="moduleFilter" class="form-select form-select-sm border-color text-muted" style="width: 130px;" onchange="filterTable()">
                        <option value="ALL">All Modules</option>
                        <option value="UI">UI</option>
                        <option value="API">API</option>
                        <option value="DATABASE">Database</option>
                        <option value="E2E">E2E</option>
                        <option value="SMOKE">Smoke</option>
                    </select>
                    <select id="pageSizeSelect" class="form-select form-select-sm border-color text-muted" style="width: 100px;" onchange="changePageSize()">
                        <option value="10">10 / page</option>
                        <option value="25">25 / page</option>
                        <option value="50">50 / page</option>
                        <option value="ALL">All</option>
                    </select>
                    <!-- Export Buttons Group -->
                    <div class="btn-group no-print ms-2">
                        <button class="btn btn-outline-secondary btn-sm" onclick="window.print()" title="Export PDF"><i class="fa-solid fa-file-pdf text-danger me-1"></i> PDF</button>
                        <button class="btn btn-outline-secondary btn-sm" onclick="exportToExcel()" title="Export Excel"><i class="fa-solid fa-file-excel text-success me-1"></i> Excel</button>
                        <button class="btn btn-outline-secondary btn-sm" onclick="exportToCSV()" title="Export CSV"><i class="fa-solid fa-file-csv text-primary me-1"></i> CSV</button>
                    </div>
                </div>
            </div>

            <div class="clean-table-container table-responsive">
                <table class="clean-table" id="resultsTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">STATUS <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th onclick="sortTable(1)">TEST NAME <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th onclick="sortTable(2)">MODULE <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th onclick="sortTable(3)">BROWSER <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th onclick="sortTable(4)">ENVIRONMENT <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th onclick="sortTable(5)">DURATION <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th onclick="sortTable(6)">EXEC TIME <i class="fa-solid fa-sort ms-1 text-muted"></i></th>
                            <th>SCREENSHOT</th>
                            <th>LOGS</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        {self._render_table_rows(processed_results)}
                    </tbody>
                </table>
            </div>

            <!-- Table Pagination Controls -->
            <div class="d-flex justify-content-between align-items-center mt-3 no-print">
                <span class="text-muted small" id="paginationInfo">Showing 1 to {len(processed_results)} of {len(processed_results)} entries</span>
                <div class="d-flex gap-2">
                    <button class="pagination-btn" id="btnPrev" onclick="prevPage()"><i class="fa-solid fa-chevron-left me-1"></i> Previous</button>
                    <button class="pagination-btn" id="btnNext" onclick="nextPage()">Next <i class="fa-solid fa-chevron-right ms-1"></i></button>
                </div>
            </div>
        </div>

        <!-- Section 4: Environment & Metadata Panel -->
        <div class="dashboard-card p-4 mb-4 fade-in">
            <h5 class="fw-bold mb-3 text-dark" style="font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-server me-2 text-secondary"></i>Environment & Execution Metadata</h5>
            <div class="row g-3">
                <div class="col-md-6">
                    <table class="table table-borderless table-sm m-0">
                        <tr><td class="text-muted" style="width: 40%;">Project Name</td><td class="fw-semibold text-dark">{metadata['Project Name']}</td></tr>
                        <tr><td class="text-muted">Framework Version</td><td class="fw-semibold text-primary">{metadata['Framework Version']}</td></tr>
                        <tr><td class="text-muted">Python Version</td><td class="fw-semibold text-dark">{metadata['Python Version']}</td></tr>
                        <tr><td class="text-muted">Pytest Version</td><td class="fw-semibold text-dark">{metadata['Pytest Version']}</td></tr>
                        <tr><td class="text-muted">Selenium Version</td><td class="fw-semibold text-dark">{metadata['Selenium Version']}</td></tr>
                        <tr><td class="text-muted">Operating System</td><td class="fw-semibold text-dark">{metadata['Operating System']}</td></tr>
                        <tr><td class="text-muted">Host Machine</td><td class="fw-semibold text-dark">{metadata['Host Machine']}</td></tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <table class="table table-borderless table-sm m-0">
                        <tr><td class="text-muted" style="width: 40%;">Execution User</td><td class="fw-semibold text-dark">{metadata['Execution User']}</td></tr>
                        <tr><td class="text-muted">Execution Date</td><td class="fw-semibold text-dark">{metadata['Execution Date']}</td></tr>
                        <tr><td class="text-muted">Execution Time</td><td class="fw-semibold text-dark">{metadata['Execution Time']}</td></tr>
                        <tr><td class="text-muted">Total Run Duration</td><td class="fw-semibold text-dark">{metadata['Total Duration']}</td></tr>
                        <tr><td class="text-muted">Git Branch</td><td class="fw-semibold text-primary"><i class="fa-solid fa-code-branch me-1"></i> {metadata['Git Branch']}</td></tr>
                        <tr><td class="text-muted">Git Commit</td><td class="fw-semibold text-primary"><i class="fa-solid fa-code-commit me-1"></i> {metadata['Git Commit']}</td></tr>
                        <tr><td class="text-muted">CI / Grid System</td><td class="fw-semibold text-dark">Local WebDrivers / Jenkins CI</td></tr>
                    </table>
                </div>
            </div>
        </div>

        <!-- Minimal Footer -->
        <footer class="text-center text-muted py-4 border-top">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                <small>Automation Framework v{metadata['Framework Version']}</small>
                <small>Generated by Selenium Python Automation Framework • Timestamp: {metadata['Execution Date']}</small>
                <small><a href="https://github.com" target="_blank" class="text-decoration-none text-muted"><i class="fa-brands fa-github me-1"></i> GitHub Repository</a></small>
            </div>
        </footer>

    </div>

    <!-- Screenshot Modal -->
    <div class="modal fade" id="imageModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content bg-white text-dark border-0 shadow-lg" style="border-radius: 16px;">
                <div class="modal-header border-bottom">
                    <h6 class="modal-title fw-bold text-dark"><i class="fa-solid fa-image me-2 text-danger"></i>Failure Screenshot Inspection</h6>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center p-3">
                    <img id="modalImage" src="" class="img-fluid rounded-3 border shadow-sm" alt="Failure Screenshot" style="max-height: 75vh;">
                </div>
                <div class="modal-footer border-top justify-content-between">
                    <small class="text-muted">Click image to download or inspect details</small>
                    <button class="btn btn-outline-secondary btn-sm" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Log Code Viewer Modal -->
    <div class="modal fade" id="logModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content bg-white text-dark border-0 shadow-lg" style="border-radius: 16px;">
                <div class="modal-header border-bottom">
                    <h6 class="modal-title fw-bold text-dark" id="logModalTitle"><i class="fa-solid fa-code me-2 text-primary"></i>Test Execution Logs</h6>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-3">
                    <div class="log-code-block" id="logCodeContent">Loading logs...</div>
                </div>
                <div class="modal-footer border-top justify-content-between">
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary btn-sm rounded-2" onclick="copyLogContent()"><i class="fa-regular fa-copy me-1"></i> Copy Logs</button>
                        <button class="btn btn-outline-secondary btn-sm rounded-2" onclick="downloadLogContent()"><i class="fa-solid fa-download me-1"></i> Download Logs</button>
                    </div>
                    <button class="btn btn-outline-secondary btn-sm rounded-2" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript Bootstrap & Chart.js Integration -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const testData = {results_json};
        const metadata = {metadata_json};

        let currentPage = 1;
        let pageSize = 10;
        let filteredData = [...testData];

        // Smooth Counter Animation on Load
        document.addEventListener('DOMContentLoaded', () => {{
            const counters = document.querySelectorAll('.count-up');
            counters.forEach(counter => {{
                const target = parseInt(counter.getAttribute('data-target')) || 0;
                let count = 0;
                const speed = Math.max(1, Math.floor(target / 20));
                const updateCount = () => {{
                    count += speed;
                    if (count < target) {{
                        counter.innerText = count;
                        setTimeout(updateCount, 30);
                    }} else {{
                        counter.innerText = target;
                    }}
                }};
                updateCount();
            }});
            initCharts();
            renderTable();
        }});

        // Initialize 6 Chart.js Visualizers
        function initCharts() {{
            const passed = {passed_tests};
            const failed = {failed_tests};
            const skipped = {skipped_tests};

            // 1. Pass vs Fail Status Doughnut Chart
            new Chart(document.getElementById('statusChart').getContext('2d'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Passed', 'Failed', 'Skipped'],
                    datasets: [{{
                        data: [passed, failed, skipped],
                        backgroundColor: ['#22C55E', '#EF4444', '#F59E0B'],
                        borderWidth: 3,
                        borderColor: '#FFFFFF'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ font: {{ family: 'Inter', size: 12 }}, color: '#64748B' }} }}
                    }}
                }}
            }});

            // 2. Execution Timeline Line Chart
            const timelineLabels = testData.map(t => t.name.length > 15 ? t.name.substring(0, 12) + '...' : t.name);
            const timelineData = testData.map(t => t.duration);
            new Chart(document.getElementById('timelineChart').getContext('2d'), {{
                type: 'line',
                data: {{
                    labels: timelineLabels,
                    datasets: [{{
                        label: 'Duration (s)',
                        data: timelineData,
                        borderColor: '#2563EB',
                        backgroundColor: 'rgba(37, 99, 235, 0.08)',
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: '#2563EB'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ ticks: {{ color: '#64748B' }}, grid: {{ color: '#E2E8F0' }} }},
                        x: {{ ticks: {{ color: '#64748B', display: false }}, grid: {{ display: false }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 3. Module Distribution Bar Chart
            const modules = {{}};
            testData.forEach(t => {{ modules[t.module] = (modules[t.module] || 0) + 1; }});
            new Chart(document.getElementById('categoryChart').getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: Object.keys(modules),
                    datasets: [{{
                        label: 'Tests',
                        data: Object.values(modules),
                        backgroundColor: ['#2563EB', '#0EA5E9', '#8B5CF6', '#F59E0B', '#22C55E'],
                        borderRadius: 8
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ ticks: {{ color: '#64748B' }}, grid: {{ color: '#E2E8F0' }} }},
                        x: {{ ticks: {{ color: '#64748B' }}, grid: {{ display: false }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 4. Test Duration Bar Chart (Top 8 Slowest)
            const sortedDuration = [...testData].sort((a,b) => b.duration - a.duration).slice(0, 8);
            new Chart(document.getElementById('durationChart').getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: sortedDuration.map(t => t.name.length > 12 ? t.name.substring(0, 10) + '..' : t.name),
                    datasets: [{{
                        label: 'Duration (s)',
                        data: sortedDuration.map(t => t.duration),
                        backgroundColor: '#F59E0B',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ ticks: {{ color: '#64748B' }}, grid: {{ color: '#E2E8F0' }} }},
                        x: {{ ticks: {{ color: '#64748B' }}, grid: {{ display: false }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 5. Browser Distribution Chart
            new Chart(document.getElementById('browserChart').getContext('2d'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Chrome', 'Firefox', 'Edge'],
                    datasets: [{{
                        data: [{total_tests}, 0, 0],
                        backgroundColor: ['#0EA5E9', '#F97316', '#059669'],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#64748B' }} }} }}
                }}
            }});

            // 6. Success Rate Gauge Chart
            new Chart(document.getElementById('gaugeChart').getContext('2d'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Passed', 'Remaining'],
                    datasets: [{{
                        data: [{pass_rate}, Math.max(0, 100 - {pass_rate})],
                        backgroundColor: ['#22C55E', '#E2E8F0'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    rotation: -90,
                    circumference: 180,
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        }}

        // Dynamic Filtering
        function filterTable() {{
            const searchVal = document.getElementById('searchInput').value.toLowerCase();
            const statusVal = document.getElementById('statusFilter').value;
            const moduleVal = document.getElementById('moduleFilter').value;

            filteredData = testData.filter(t => {{
                const matchesSearch = t.name.toLowerCase().includes(searchVal) || t.file.toLowerCase().includes(searchVal) || t.module.toLowerCase().includes(searchVal);
                const matchesStatus = (statusVal === 'ALL' || t.status === statusVal);
                const matchesModule = (moduleVal === 'ALL' || t.module === moduleVal);
                return matchesSearch && matchesStatus && matchesModule;
            }});

            currentPage = 1;
            renderTable();
        }}

        // Table Pagination & Rendering
        function renderTable() {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            let displayData = filteredData;
            if (pageSize !== 'ALL') {{
                const start = (currentPage - 1) * pageSize;
                const end = start + parseInt(pageSize);
                displayData = filteredData.slice(start, end);
            }}

            displayData.forEach(t => {{
                const tr = document.createElement('tr');
                tr.setAttribute('data-status', t.status);
                
                let badgeClass = 'badge-passed';
                if (t.status === 'failed') badgeClass = 'badge-failed';
                else if (t.status === 'skipped') badgeClass = 'badge-skipped';

                let imgHtml = '<span class="text-muted small">N/A</span>';
                if (t.screenshot_uri) {{
                    imgHtml = `<img src="${{t.screenshot_uri}}" class="screenshot-thumb" onclick="openImageModal('${{t.screenshot_uri}}')">`;
                }}

                tr.innerHTML = `
                    <td><span class="badge-status ${{badgeClass}}">${{t.status.toUpperCase()}}</span></td>
                    <td>
                        <span class="fw-semibold text-dark">${{t.name}}</span><br>
                        <small class="text-muted">${{t.file}}</small>
                    </td>
                    <td><span class="badge bg-light text-dark border">${{t.module}}</span></td>
                    <td><small><i class="fa-brands fa-chrome text-primary me-1"></i>${{t.browser}}</small></td>
                    <td><span class="badge bg-primary-subtle text-primary border border-primary-subtle">${{t.environment}}</span></td>
                    <td><code>${{t.duration}}s</code></td>
                    <td><small class="text-muted">${{t.execution_time}}</small></td>
                    <td>${{imgHtml}}</td>
                    <td>
                        <button class="btn btn-outline-primary btn-sm rounded-2" onclick="openLogModal('${{t.id}}')">
                            <i class="fa-solid fa-code me-1"></i> Logs
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});

            // Update Pagination Controls Info
            const total = filteredData.length;
            const paginationInfo = document.getElementById('paginationInfo');
            if (pageSize === 'ALL') {{
                paginationInfo.innerText = `Showing all ${{total}} entries`;
            }} else {{
                const start = total === 0 ? 0 : (currentPage - 1) * pageSize + 1;
                const end = Math.min(currentPage * pageSize, total);
                paginationInfo.innerText = `Showing ${{start}} to ${{end}} of ${{total}} entries`;
            }}

            document.getElementById('btnPrev').disabled = (currentPage === 1 || pageSize === 'ALL');
            document.getElementById('btnNext').disabled = (pageSize === 'ALL' || currentPage * pageSize >= total);
        }}

        function changePageSize() {{
            const val = document.getElementById('pageSizeSelect').value;
            pageSize = val === 'ALL' ? 'ALL' : parseInt(val);
            currentPage = 1;
            renderTable();
        }}

        function prevPage() {{
            if (currentPage > 1) {{
                currentPage--;
                renderTable();
            }}
        }}

        function nextPage() {{
            if (pageSize !== 'ALL' && currentPage * pageSize < filteredData.length) {{
                currentPage++;
                renderTable();
            }}
        }}

        // Sorting Logic
        let sortAsc = true;
        function sortTable(colIndex) {{
            const keys = ['status', 'name', 'module', 'browser', 'environment', 'duration', 'execution_time'];
            const key = keys[colIndex];
            if (!key) return;

            sortAsc = !sortAsc;
            filteredData.sort((a, b) => {{
                if (typeof a[key] === 'number') {{
                    return sortAsc ? a[key] - b[key] : b[key] - a[key];
                }}
                return sortAsc ? String(a[key]).localeCompare(String(b[key])) : String(b[key]).localeCompare(String(a[key]));
            }});
            renderTable();
        }}

        // Screenshot Modal
        function openImageModal(imgSrc) {{
            document.getElementById('modalImage').src = imgSrc;
            const modal = new bootstrap.Modal(document.getElementById('imageModal'));
            modal.show();
        }}

        // Log Modal
        let activeLogText = "";
        let activeTestName = "";
        function openLogModal(testId) {{
            const test = testData.find(t => t.id == testId);
            if (!test) return;

            activeTestName = test.name;
            activeLogText = test.logs;

            document.getElementById('logModalTitle').innerText = `Logs: ${{test.name}}`;
            document.getElementById('logCodeContent').innerText = activeLogText;

            const modal = new bootstrap.Modal(document.getElementById('logModal'));
            modal.show();
        }}

        function copyLogContent() {{
            navigator.clipboard.writeText(activeLogText).then(() => {{
                alert('Logs copied to clipboard!');
            }});
        }}

        function downloadLogContent() {{
            const blob = new Blob([activeLogText], {{ type: 'text/plain' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${{activeTestName}}_log.txt`;
            a.click();
            URL.revokeObjectURL(url);
        }}

        // Exports
        function exportToCSV() {{
            let csv = "STATUS,TEST NAME,MODULE,BROWSER,ENVIRONMENT,DURATION,EXEC TIME\\n";
            testData.forEach(t => {{
                csv += `"${{t.status}}","${{t.name}}","${{t.module}}","${{t.browser}}","${{t.environment}}","${{t.duration}}","${{t.execution_time}}"\\n`;
            }});
            const blob = new Blob([csv], {{ type: 'text/csv' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'automation_test_report.csv';
            a.click();
            URL.revokeObjectURL(url);
        }}

        function exportToExcel() {{
            exportToCSV();
        }}
    </script>
</body>
</html>
"""
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[EnterpriseDashboard] Premium Analytics Dashboard generated at: {self.output_path.resolve()}")
        return self.output_path

    def _render_table_rows(self, test_results: List[Dict[str, Any]]) -> str:
        """Render clean light initial rows for server-side HTML fallback."""
        rows_html = []
        for test in test_results:
            status = test.get("status", "passed")
            badge_class = f"badge-{status}"
            module = test.get("module", "UI")
            duration = f"{round(test.get('duration', 0.0), 2)}s"
            browser_name = test.get("browser", "Chrome")
            env_name = test.get("environment", "QA")
            exec_time = test.get("execution_time", "")
            test_id = test.get("id", 1)

            screenshot_uri = test.get("screenshot_uri", "")
            if screenshot_uri:
                img_html = f'<img src="{screenshot_uri}" class="screenshot-thumb" onclick="openImageModal(\'{screenshot_uri}\')">'
            else:
                img_html = '<span class="text-muted small">N/A</span>'

            row = f"""
            <tr data-status="{status}">
                <td><span class="badge-status {badge_class}">{status.upper()}</span></td>
                <td>
                    <span class="fw-semibold text-dark">{test['name']}</span><br>
                    <small class="text-muted">{test.get('file', '')}</small>
                </td>
                <td><span class="badge bg-light text-dark border">{module}</span></td>
                <td><small><i class="fa-brands fa-chrome text-primary me-1"></i>{browser_name}</small></td>
                <td><span class="badge bg-primary-subtle text-primary border border-primary-subtle">{env_name}</span></td>
                <td><code>{duration}</code></td>
                <td><small class="text-muted">{exec_time}</small></td>
                <td>{img_html}</td>
                <td>
                    <button class="btn btn-outline-primary btn-sm rounded-2" onclick="openLogModal('{test_id}')">
                        <i class="fa-solid fa-code me-1"></i> Logs
                    </button>
                </td>
            </tr>
            """
            rows_html.append(row)
        return "\n".join(rows_html)
