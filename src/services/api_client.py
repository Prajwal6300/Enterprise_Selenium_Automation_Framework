"""Enterprise REST API Client wrapper built on top of Python Requests.

Provides centralized HTTP request handling (GET, POST, PUT, DELETE),
Bearer Token authentication, automatic header management, response logging,
and validation helpers for status codes and JSON response schemas.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
import requests
from requests import Response

from src.utils.logger import get_logger

logger = get_logger("APIClient")


class APIClient:
    """Base HTTP Client for executing RESTful API calls with enterprise capabilities."""

    def __init__(self, base_url: str, token: Optional[str] = None) -> None:
        """Initialize API client with base URL and optional Bearer token.

        Args:
            base_url: Base endpoint URL (e.g. https://reqres.in)
            token: Optional Bearer authentication token string
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if token:
            self.set_bearer_token(token)

    def set_bearer_token(self, token: str) -> None:
        """Set Bearer Token header for authenticated endpoints."""
        self.headers["Authorization"] = f"Bearer {token}"
        logger.info("Bearer Token configured for API Client sessions.")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Response:
        """Execute GET HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = {**self.headers, **(headers or {})}
        logger.info("Sending GET request to %s with params %s", url, params)
        response = self.session.get(url, params=params, headers=req_headers, timeout=10)
        self._log_response(response)
        return response

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Response:
        """Execute POST HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = {**self.headers, **(headers or {})}
        logger.info("Sending POST request to %s with payload %s", url, data)
        response = self.session.post(url, json=data, headers=req_headers, timeout=10)
        self._log_response(response)
        return response

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Response:
        """Execute PUT HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = {**self.headers, **(headers or {})}
        logger.info("Sending PUT request to %s with payload %s", url, data)
        response = self.session.put(url, json=data, headers=req_headers, timeout=10)
        self._log_response(response)
        return response

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Response:
        """Execute DELETE HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = {**self.headers, **(headers or {})}
        logger.info("Sending DELETE request to %s", url)
        response = self.session.delete(url, headers=req_headers, timeout=10)
        self._log_response(response)
        return response

    @staticmethod
    def validate_status_code(response: Response, expected_status: int) -> None:
        """Validate that the API response status code matches expected status code."""
        actual_status = response.status_code
        assert actual_status == expected_status, (
            f"API Status Code Mismatch! Expected: {expected_status}, Got: {actual_status}. "
            f"Response Body: {response.text}"
        )

    @staticmethod
    def validate_json_key(response: Response, key: str, expected_value: Any = None) -> Any:
        """Validate presence and optionally exact value of a key in the JSON response."""
        json_data = response.json()
        assert key in json_data, f"Key '{key}' not found in JSON response body: {json_data}"
        if expected_value is not None:
            actual_value = json_data[key]
            assert actual_value == expected_value, (
                f"JSON Key '{key}' value mismatch. Expected: {expected_value}, Got: {actual_value}"
            )
        return json_data[key]

    def _log_response(self, response: Response) -> None:
        """Log status code and elapsed time for response tracking."""
        logger.info("Received Response: Status=%d, Elapsed=%s", response.status_code, response.elapsed)
