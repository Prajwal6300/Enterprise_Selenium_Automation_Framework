"""REST API Schema, Header, and Business Data Validation Test Suite.

Validates:
1. Status code validation on GET /posts
2. Response headers Content-Type (application/json)
3. Response body JSON schema required keys (id, title, body, userId)
4. Field data type validation (id is int, title is str, userId is int)
5. Query parameter filtering (GET /posts?userId=1 returns only userId=1)
6. Response performance SLA validation (< 3.0s latency)
7. POST payload integrity echo validation
8. PUT updated payload reflection
"""

from __future__ import annotations

import pytest
from src.services.api_client import APIClient
from src.services.user_api import UserAPIService
from src.utils.logger import get_logger

logger = get_logger("TestAPIValidation")


@pytest.mark.api
@pytest.mark.regression
class TestAPIValidation:
    """Validation test suite for REST API schemas, headers, status codes, and data formats."""

    @pytest.fixture(autouse=True)
    def setup_api(self):
        """Initialize API service before each test."""
        self.api_service = UserAPIService()
        self.client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    def test_api_status_code_success_200(self):
        """1. Verify GET requests to valid resources return HTTP 200 OK."""
        logger.info("Executing test_api_status_code_success_200")
        response = self.api_service.get_user_by_id(post_id=1)
        APIClient.validate_status_code(response, 200)
        logger.info("test_api_status_code_success_200 passed")

    def test_api_response_headers_content_type(self):
        """2. Verify API response headers include 'Content-Type: application/json'."""
        logger.info("Executing test_api_response_headers_content_type")
        response = self.api_service.get_users(user_id=1)
        APIClient.validate_status_code(response, 200)
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Expected JSON Content-Type, got '{content_type}'"
        logger.info("test_api_response_headers_content_type passed")

    def test_api_response_schema_required_keys(self):
        """3. Verify single record response contains all required schema keys."""
        logger.info("Executing test_api_response_schema_required_keys")
        response = self.api_service.get_user_by_id(post_id=2)
        APIClient.validate_status_code(response, 200)
        data = response.json()
        required_keys = ["id", "title", "body", "userId"]
        for key in required_keys:
            assert key in data, f"Required key '{key}' missing from API response schema"
        logger.info("test_api_response_schema_required_keys passed")

    def test_api_field_data_types_validation(self):
        """4. Verify response fields match strict data types (int, str)."""
        logger.info("Executing test_api_field_data_types_validation")
        response = self.api_service.get_user_by_id(post_id=3)
        data = response.json()
        assert isinstance(data["id"], int), f"Expected 'id' to be int, got {type(data['id'])}"
        assert isinstance(data["title"], str), f"Expected 'title' to be str, got {type(data['title'])}"
        assert isinstance(data["body"], str), f"Expected 'body' to be str, got {type(data['body'])}"
        assert isinstance(data["userId"], int), f"Expected 'userId' to be int, got {type(data['userId'])}"
        logger.info("test_api_field_data_types_validation passed")

    def test_api_query_parameter_filtering(self):
        """5. Verify GET /posts with query parameter filters records accordingly."""
        logger.info("Executing test_api_query_parameter_filtering")
        response = self.api_service.get_users(user_id=2)
        APIClient.validate_status_code(response, 200)
        records = response.json()
        assert isinstance(records, list) and len(records) > 0
        for r in records:
            assert r["userId"] == 2, f"Expected userId=2, got {r['userId']}"
        logger.info("test_api_query_parameter_filtering passed with %d records", len(records))

    def test_api_response_time_sla(self):
        """6. Verify API response is returned within performance SLA (< 3.0s)."""
        logger.info("Executing test_api_response_time_sla")
        response = self.api_service.get_user_by_id(post_id=1)
        APIClient.validate_status_code(response, 200)
        elapsed = response.elapsed.total_seconds()
        assert elapsed < 3.0, f"Response time {elapsed}s exceeded SLA limit of 3.0s"
        logger.info("test_api_response_time_sla passed in %0.3fs", elapsed)

    def test_api_post_creation_payload_echo(self):
        """7. Verify POST /posts creates resource and echoes sent data."""
        logger.info("Executing test_api_post_creation_payload_echo")
        test_title = "Enterprise Test Validation Suite"
        test_body = "Comprehensive SDET Automation Framework"
        response = self.api_service.create_user(title=test_title, body=test_body, user_id=10)
        
        APIClient.validate_status_code(response, 201)
        APIClient.validate_json_key(response, "title", test_title)
        APIClient.validate_json_key(response, "body", test_body)
        APIClient.validate_json_key(response, "id")
        logger.info("test_api_post_creation_payload_echo passed")

    def test_api_put_update_payload_echo(self):
        """8. Verify PUT /posts/1 updates resource and returns updated content."""
        logger.info("Executing test_api_put_update_payload_echo")
        updated_title = "Updated Senior QA Title"
        updated_body = "Updated Automation Description"
        response = self.api_service.update_user(post_id=1, title=updated_title, body=updated_body, user_id=1)
        
        APIClient.validate_status_code(response, 200)
        APIClient.validate_json_key(response, "title", updated_title)
        APIClient.validate_json_key(response, "body", updated_body)
        logger.info("test_api_put_update_payload_echo passed")
