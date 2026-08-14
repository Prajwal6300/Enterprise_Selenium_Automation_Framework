"""Production-Ready REST API Automation Test Suite.

Validates authentication, GET list, GET single, POST creation, PUT update,
DELETE removal, Bearer Token setup, status codes, and JSON response schema validations.
"""

from __future__ import annotations

import pytest
from src.services.api_client import APIClient
from src.services.user_api import UserAPIService
from src.utils.logger import get_logger

logger = get_logger("TestAPIWorkflow")


@pytest.mark.api
class TestAPIWorkflow:
    """Test suite covering REST API requests and validations."""

    @pytest.fixture(autouse=True)
    def setup_api(self):
        """Initialize API service before each test."""
        self.api_service = UserAPIService()

    def test_login_api_success(self):
        """Verify login API authenticates user and returns created resource ID."""
        logger.info("Executing test_login_api_success")
        response = self.api_service.login(username="standard_user", password="secret_sauce")
        
        APIClient.validate_status_code(response, 201)
        res_id = APIClient.validate_json_key(response, "id")
        assert res_id is not None, "Login API should return valid resource ID"
        logger.info("Login API test passed with resource ID: %s", res_id)

    def test_get_users_list_validation(self):
        """Verify GET API returns records with status code 200."""
        logger.info("Executing test_get_users_list_validation")
        response = self.api_service.get_users(user_id=1)
        
        APIClient.validate_status_code(response, 200)
        json_data = response.json()
        assert isinstance(json_data, list), "Response data should be a list"
        assert len(json_data) > 0, "Users data list should not be empty"
        logger.info("GET users list test passed")

    def test_post_create_user(self):
        """Verify POST API creates a new record with generated ID."""
        logger.info("Executing test_post_create_user")
        response = self.api_service.create_user(
            title="Enterprise SDET Test",
            body="Automation Framework Architect",
            user_id=1
        )
        
        APIClient.validate_status_code(response, 201)
        APIClient.validate_json_key(response, "title", "Enterprise SDET Test")
        APIClient.validate_json_key(response, "body", "Automation Framework Architect")
        APIClient.validate_json_key(response, "id")
        logger.info("POST create user test passed")

    def test_put_update_user(self):
        """Verify PUT API updates existing record details."""
        logger.info("Executing test_put_update_user")
        response = self.api_service.update_user(
            post_id=1,
            title="Updated Lead SDET",
            body="Principal QA Engineer",
            user_id=1
        )
        
        APIClient.validate_status_code(response, 200)
        APIClient.validate_json_key(response, "title", "Updated Lead SDET")
        APIClient.validate_json_key(response, "body", "Principal QA Engineer")
        logger.info("PUT update user test passed")

    def test_delete_user(self):
        """Verify DELETE API removes record and returns HTTP 200 OK."""
        logger.info("Executing test_delete_user")
        response = self.api_service.delete_user(post_id=1)
        
        APIClient.validate_status_code(response, 200)
        logger.info("DELETE user test passed")

    def test_get_single_resource_and_schema_validation(self):
        """Verify GET by ID returns valid schema with id, title, body, and userId keys."""
        logger.info("Executing test_get_single_resource_and_schema_validation")
        response = self.api_service.get_user_by_id(post_id=1)
        
        APIClient.validate_status_code(response, 200)
        data = response.json()
        assert isinstance(data, dict), "Response must be a JSON object"
        for required_key in ["id", "title", "body", "userId"]:
            assert required_key in data, f"Required schema key '{required_key}' missing from API response"
        assert data["id"] == 1, f"Expected post id 1, got {data['id']}"
        logger.info("test_get_single_resource_and_schema_validation passed")

    def test_get_invalid_endpoint_returns_404(self):
        """Verify sending request to non-existent endpoint returns HTTP 404 Not Found."""
        logger.info("Executing test_get_invalid_endpoint_returns_404")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        response = client.get("non_existent_resource_endpoint_xyz")
        
        assert response.status_code == 404, f"Expected 404 for invalid endpoint, got {response.status_code}"
        logger.info("test_get_invalid_endpoint_returns_404 passed")

    def test_get_invalid_resource_id_returns_404(self):
        """Verify requesting non-existent record ID returns HTTP 404."""
        logger.info("Executing test_get_invalid_resource_id_returns_404")
        response = self.api_service.get_user_by_id(post_id=9999999)
        
        assert response.status_code == 404, f"Expected 404 for non-existent resource ID, got {response.status_code}"
        logger.info("test_get_invalid_resource_id_returns_404 passed")

    def test_api_response_headers_and_content_type(self):
        """Verify API response contains Content-Type application/json header."""
        logger.info("Executing test_api_response_headers_and_content_type")
        response = self.api_service.get_users(user_id=1)
        
        APIClient.validate_status_code(response, 200)
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Expected JSON Content-Type header, got '{content_type}'"
        logger.info("test_api_response_headers_and_content_type passed")

    def test_api_response_time_threshold(self):
        """Verify API response is returned within performance SLA threshold (< 3000ms)."""
        logger.info("Executing test_api_response_time_threshold")
        response = self.api_service.get_user_by_id(post_id=1)
        
        APIClient.validate_status_code(response, 200)
        elapsed_seconds = response.elapsed.total_seconds()
        assert elapsed_seconds < 3.0, f"API response exceeded 3.0s SLA limit: {elapsed_seconds}s"
        logger.info("test_api_response_time_threshold passed in %0.3fs", elapsed_seconds)

    def test_bearer_token_authorization_header(self):
        """Verify setting bearer token properly formats authorization request header."""
        logger.info("Executing test_bearer_token_authorization_header")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        client.set_bearer_token("sample_jwt_bearer_token_12345")
        
        assert client.headers["Authorization"] == "Bearer sample_jwt_bearer_token_12345", (
            "Authorization header failed to format Bearer token string"
        )
        logger.info("Bearer token test passed")

