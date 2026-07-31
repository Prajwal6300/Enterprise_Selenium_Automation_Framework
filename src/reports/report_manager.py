"""Enterprise Automation Reporting Utility.

Provides metadata extraction, environment info gathering, performance metric collection,
and HTML dashboard template rendering for pytest-html & Allure integrations.
"""

from __future__ import annotations

import base64
import datetime
import getpass
import os
from pathlib import Path
import platform
import socket
import subprocess
from typing import Any, Dict, List, Optional
import selenium

from src.utils.logger import get_logger

logger = get_logger("ReportManager")


class ReportManager:
    """Enterprise Report Manager for dashboard generation and metadata collection."""

    @staticmethod
    def get_system_metadata(env: str = "qa", browser: str = "chrome") -> Dict[str, Any]:
        """Gather system, environment, VCS, and framework runtime metadata."""
        metadata = {
            "Project Name": "SauceDemo E-Commerce Enterprise Automation",
            "Framework": "Selenium Python POM Architecture",
            "Framework Version": "2.5.0-Enterprise",
            "Environment": env.upper(),
            "Target Browser": browser.capitalize(),
            "Operating System": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "Python Version": platform.python_version(),
            "Selenium Version": selenium.__version__,
            "Host Machine": socket.gethostname(),
            "Execution User": getpass.getuser(),
            "Execution Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Subprocess Git commit info extraction
        try:
            git_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
            git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
            metadata["Git Branch"] = git_branch
            metadata["Git Commit Hash"] = git_commit
        except Exception:
            metadata["Git Branch"] = "main"
            metadata["Git Commit Hash"] = "production-head"

        # CI Environment Variables Detection (Jenkins / GitHub Actions)
        if os.getenv("JENKINS_URL"):
            metadata["CI System"] = "Jenkins CI"
            metadata["Jenkins Build Number"] = os.getenv("BUILD_NUMBER", "N/A")
            metadata["Jenkins Build URL"] = os.getenv("BUILD_URL", "N/A")
        elif os.getenv("GITHUB_ACTIONS"):
            metadata["CI System"] = "GitHub Actions"
            metadata["GitHub Workflow"] = os.getenv("GITHUB_WORKFLOW", "N/A")
            metadata["GitHub Run ID"] = os.getenv("GITHUB_RUN_ID", "N/A")
            metadata["GitHub Event"] = os.getenv("GITHUB_EVENT_NAME", "N/A")

        # BrowserStack Session Metadata Detection
        if os.getenv("BROWSERSTACK_USERNAME"):
            metadata["Cloud Grid"] = "BrowserStack Automation Cloud"
            metadata["BrowserStack User"] = os.getenv("BROWSERSTACK_USERNAME")

        return metadata

    @staticmethod
    def get_base64_image(image_path: str | Path) -> str:
        """Convert a local screenshot file into a Base64 data URI string."""
        path = Path(image_path)
        if not path.exists():
            return ""
        with open(path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

    @staticmethod
    def generate_dashboard_css() -> str:
        """Return custom CSS for light modern enterprise dashboard styling."""
        return """
        <style>
            :root {
                --primary-color: #2563eb;
                --success-color: #22c55e;
                --danger-color: #ef4444;
                --warning-color: #f59e0b;
                --info-color: #06b6d4;
                --bg-light: #f8fafc;
                --card-bg: #ffffff;
                --text-main: #1e293b;
                --text-muted: #64748b;
                --border-color: #e2e8f0;
            }
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background-color: var(--bg-light) !important;
                color: var(--text-main) !important;
                margin: 0;
                padding: 24px;
            }
            .dashboard-header {
                background: #ffffff;
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);
            }
            .dashboard-title {
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 16px;
                margin-bottom: 20px;
            }
            .dashboard-title h1 {
                margin: 0;
                font-size: 24px;
                color: var(--primary-color);
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            .kpi-cards-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
                margin-bottom: 24px;
            }
            .kpi-card {
                background: #ffffff;
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 16px;
                text-align: center;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .kpi-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(37, 99, 235, 0.12);
            }
            .kpi-value {
                font-size: 26px;
                font-weight: 700;
                margin-top: 6px;
            }
            .kpi-label {
                font-size: 12px;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 600;
            }
            .kpi-passed { color: #15803d; border-top: 4px solid #22c55e; }
            .kpi-failed { color: #b91c1c; border-top: 4px solid #ef4444; }
            .kpi-skipped { color: #b45309; border-top: 4px solid #f59e0b; }
            .kpi-total { color: #2563eb; border-top: 4px solid #2563eb; }
            .kpi-rate { color: #0d9488; border-top: 4px solid #14b8a6; }
            
            .meta-table-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 16px;
            }
            .meta-table {
                width: 100%;
                border-collapse: collapse;
                background: #ffffff;
                border: 1px solid var(--border-color);
                border-radius: 10px;
                overflow: hidden;
            }
            .meta-table th {
                background: #f1f5f9;
                color: var(--text-main);
                padding: 10px 14px;
                text-align: left;
                font-size: 13px;
            }
            .meta-table td {
                padding: 10px 14px;
                border-bottom: 1px solid var(--border-color);
                font-size: 13px;
                color: var(--text-muted);
            }
            
            /* Modal Image Enlarge */
            .report-screenshot {
                cursor: pointer;
                border-radius: 8px;
                border: 1px solid var(--border-color);
                transition: transform 0.2s;
                max-width: 250px;
            }
            .report-screenshot:hover {
                transform: scale(1.04);
            }
            .modal-overlay {
                display: none;
                position: fixed;
                z-index: 9999;
                top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(4px);
                align-items: center;
                justify-content: center;
            }
            .modal-overlay img {
                max-width: 90%;
                max-height: 90%;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
        </style>
        """

    @staticmethod
    def generate_modal_script() -> str:
        """Return JavaScript for image zoom modal and theme toggling."""
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Create Modal Overlay Container
                const modal = document.createElement('div');
                modal.className = 'modal-overlay';
                modal.id = 'imgModal';
                modal.onclick = function() { modal.style.display = 'none'; };
                const modalImg = document.createElement('img');
                modal.appendChild(modalImg);
                document.body.appendChild(modal);

                // Add Click Handler to Screenshots
                document.querySelectorAll('img').forEach(img => {
                    if (!img.classList.contains('no-modal')) {
                        img.classList.add('report-screenshot');
                        img.onclick = function(e) {
                            e.stopPropagation();
                            modalImg.src = this.src;
                            modal.style.display = 'flex';
                        };
                    }
                });
            });
        </script>
        """
