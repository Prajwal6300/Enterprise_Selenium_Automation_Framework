"""User Management REST API Service Object.

Encapsulates user/resource authentication, retrieval, creation, modification,
and deletion endpoint calls following the Service Object Pattern.
"""

from __future__ import annotations

from typing import Any, Dict
from requests import Response
from src.services.api_client import APIClient


class UserAPIService:
    """Service class for user and post REST API endpoints."""

    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com") -> None:
        """Initialize UserAPIService with base endpoint."""
        self.client = APIClient(base_url=base_url)

    def login(self, username: str = "standard_user", password: str = "secret_sauce") -> Response:
        """Execute user login authentication request."""
        payload = {"username": username, "password": password}
        return self.client.post("posts", data=payload)

    def get_users(self, user_id: int = 1) -> Response:
        """Fetch list of users/posts with query parameter."""
        return self.client.get("posts", params={"userId": user_id})

    def get_user_by_id(self, post_id: int = 1) -> Response:
        """Fetch details for a single record by ID."""
        return self.client.get(f"posts/{post_id}")

    def create_user(self, title: str, body: str, user_id: int = 1) -> Response:
        """Create a new resource record."""
        payload = {"title": title, "body": body, "userId": user_id}
        return self.client.post("posts", data=payload)

    def update_user(self, post_id: int, title: str, body: str, user_id: int = 1) -> Response:
        """Update existing resource record via PUT."""
        payload = {"id": post_id, "title": title, "body": body, "userId": user_id}
        return self.client.put(f"posts/{post_id}", data=payload)

    def delete_user(self, post_id: int) -> Response:
        """Delete resource record via DELETE."""
        return self.client.delete(f"posts/{post_id}")
