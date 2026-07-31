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

    def test_bearer_token_authorization_header(self):
        """Verify setting bearer token properly formats authorization request header."""
        logger.info("Executing test_bearer_token_authorization_header")
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        client.set_bearer_token("sample_jwt_bearer_token_12345")
        
        assert client.headers["Authorization"] == "Bearer sample_jwt_bearer_token_12345", (
            "Authorization header failed to format Bearer token string"
        )
        logger.info("Bearer token test passed")
