"""Normalized Execution Data Models for Enterprise QA Automation Platform.

Provides strongly typed data structures for test executions, test cases,
execution steps, assertions, failure analyses, screenshots, logs, and metrics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import datetime
from typing import Any, Dict, List, Optional


@dataclass
class TestStep:
    """Represents an individual step or assertion within a test execution."""
    name: str
    status: str = "passed"  # passed, failed, skipped, running
    duration: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().strftime("%H:%M:%S"))
    details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FailureDetail:
    """Captures granular diagnostic information for test failures."""
    error_type: str = ""
    error_message: str = ""
    stack_trace: str = ""
    failure_category: str = "AssertionError"  # e.g., ElementNotInteractable, Timeout, AssertionError
    screenshot_path: Optional[str] = None
    screenshot_uri: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TestResult:
    """Represents a single executed test case record."""
    test_id: str
    name: str
    class_name: str
    module: str
    file_path: str
    test_type: str = "UI"  # UI, API, Database, E2E, Smoke, Regression
    browser: str = "Chrome"
    environment: str = "QA"
    status: str = "PASSED"  # PASSED, FAILED, SKIPPED
    duration: float = 0.0
    start_time: str = ""
    end_time: str = ""
    steps: List[TestStep] = field(default_factory=list)
    assertions: List[str] = field(default_factory=list)
    failure: Optional[FailureDetail] = None
    log_snippet: str = ""
    screenshot_path: Optional[str] = None
    screenshot_uri: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.steps:
            data["steps"] = [s.to_dict() if isinstance(s, TestStep) else s for s in self.steps]
        if self.failure:
            data["failure"] = self.failure.to_dict() if isinstance(self.failure, FailureDetail) else self.failure
        return data


@dataclass
class ExecutionSummary:
    """Normalized top-level execution run summary."""
    execution_id: str
    timestamp: str
    date: str
    time: str
    environment: str = "QA"
    browser: str = "Chrome"
    branch: str = "main"
    commit_hash: str = "HEAD"
    ci_system: str = "Local"
    host_machine: str = ""
    operating_system: str = ""
    python_version: str = ""
    selenium_version: str = ""
    status: str = "PASSED"  # PASSED, FAILED, RUNNING, CANCELLED
    duration: float = 0.0
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    pass_rate: float = 100.0
    tests: List[TestResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["tests"] = [t.to_dict() if isinstance(t, TestResult) else t for t in self.tests]
        return data


@dataclass
class BrowserMetric:
    """Aggregated statistics per target browser."""
    browser: str
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    pass_rate: float = 0.0
    avg_duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnvironmentMetric:
    """Aggregated statistics per target environment."""
    environment: str
    total_executions: int = 0
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    avg_duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
