"""Email Report Utility.

Sends test execution HTML report and summary via SMTP email.
"""

from __future__ import annotations

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib
from typing import List, Optional

from src.utils.logger import get_logger

logger = get_logger("EmailReporter")


class EmailReporter:
    """SMTP Email Report Sender."""

    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, password: str) -> None:
        """Initialize email credentials and SMTP configuration."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password

    def send_report(self, recipient_emails: List[str], subject: str, body_html: str,
                    report_file_path: Optional[str] = None) -> bool:
        """Construct and send HTML test report email with optional attachment."""
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipient_emails)
            message["Subject"] = subject
            message.attach(MIMEText(body_html, "html"))

            if report_file_path and os.path.exists(report_file_path):
                file_path = Path(report_file_path)
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=file_path.name)
                part['Content-Disposition'] = f'attachment; filename="{file_path.name}"'
                message.attach(part)

            logger.info("Connecting to SMTP server %s:%d", self.smtp_server, self.smtp_port)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_emails, message.as_string())

            logger.info("Test Report Email sent successfully to %s", recipient_emails)
            return True
        except Exception as err:
            logger.error("Failed to send email report: %s", err)
            return False
