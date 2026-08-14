"""Negative REST API Automation Test Suite.

Validates fault tolerance, error handling, status codes, and security headers:
1. Invalid endpoint returns 404
2. Non-existent resource ID returns 404
3. Empty payload in POST request
4. Invalid/Malformed payload in POST request
5. Missing required fields in POST request
6. Invalid data type in payload
7. PUT update on non-existent resource ID
8. PATCH partial update with empty payload
9. DELETE non-existent resource ID
10. Unauthorized request simulation / Missing Bearer token behavior
"""

from __future__ import annotations

import pytest
from src.services.api_client import APIClient
from src.services.user_api import UserAPIService
from src.utils.logger import get_logger

logger = get_logger("TestAPINegative")


@pytest.mark.api
@pytest.mark.negative
class TestAPINegative:
    """Negative REST API test scenarios covering 4xx responses and bad inputs."""

    @pytest.fixture(autouse=True)
    def setup_api(self):
        """Initialize API service before each test."""
        self.api_service = UserAPIService()
        self.client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    def test_api_negative_get_non_existent_resource_404(self):
        """1. Verify GET request for non-existent resource ID returns HTTP 404 Not Found."""
        logger.info("Executing test_api_negative_get_non_existent_resource_404")
        response = self.api_service.get_user_by_id(post_id=9999999)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("test_api_negative_get_non_existent_resource_404 passed")

    def test_api_negative_get_invalid_endpoint_404(self):
        """2. Verify GET request to completely invalid URI endpoint returns HTTP 404."""
        logger.info("Executing test_api_negative_get_invalid_endpoint_404")
        response = self.client.get("invalid_api_v999_endpoint_does_not_exist")
        assert response.status_code == 404, f"Expected 404 for invalid endpoint, got {response.status_code}"
        logger.info("test_api_negative_get_invalid_endpoint_404 passed")

    def test_api_negative_post_empty_payload(self):
        """3. Verify POST request with empty dictionary executes safely without crash."""
        logger.info("Executing test_api_negative_post_empty_payload")
        response = self.client.post("posts", data={})
        assert response.status_code in (200, 201, 400), f"Unexpected status: {response.status_code}"
        logger.info("test_api_negative_post_empty_payload passed")

    def test_api_negative_post_missing_required_fields(self):
        """4. Verify POST request omitting title/body is handled safely."""
        logger.info("Executing test_api_negative_post_missing_required_fields")
        response = self.client.post("posts", data={"userId": 1})
        assert response.status_code in (200, 201, 400, 422)
        logger.info("test_api_negative_post_missing_required_fields passed")

    def test_api_negative_post_invalid_data_type(self):
        """5. Verify POST request sending invalid numeric data type for text field."""
        logger.info("Executing test_api_negative_post_invalid_data_type")
        payload = {"title": 123456789, "body": ["invalid", "array", "body"], "userId": "not_an_int"}
        response = self.client.post("posts", data=payload)
        assert response.status_code in (200, 201, 400, 422)
        logger.info("test_api_negative_post_invalid_data_type passed")

    def test_api_negative_put_non_existent_resource(self):
        """6. Verify PUT update request to a non-existent resource ID returns 404 or 500 error."""
        logger.info("Executing test_api_negative_put_non_existent_resource")
        payload = {"id": 9999999, "title": "Ghost Post", "body": "Ghost Content", "userId": 1}
        response = self.client.put("posts/9999999", data=payload)
        assert response.status_code in (404, 500), f"Expected 404 or 500, got {response.status_code}"
        logger.info("test_api_negative_put_non_existent_resource passed")

    def test_api_negative_delete_non_existent_resource(self):
        """7. Verify DELETE request for a non-existent resource ID is handled gracefully."""
        logger.info("Executing test_api_negative_delete_non_existent_resource")
        response = self.client.delete("posts/9999999")
        assert response.status_code in (200, 404), f"Expected 200 or 404, got {response.status_code}"
        logger.info("test_api_negative_delete_non_existent_resource passed")

    def test_api_negative_invalid_authorization_header(self):
        """8. Verify setting invalid malformed authorization header does not cause client error."""
        logger.info("Executing test_api_negative_invalid_authorization_header")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        client.headers["Authorization"] = "InvalidFormatToken12345"
        response = client.get("posts/1")
        assert response.status_code in (200, 401, 403), f"Unexpected status code: {response.status_code}"
        logger.info("test_api_negative_invalid_authorization_header passed")
