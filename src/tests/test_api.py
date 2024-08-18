"""Tests for the API endpoints."""

from collections.abc import Iterator
from datetime import datetime

import pytest
from flask.testing import FlaskClient

from web.app import app

SUCCESS = 200


@pytest.fixture
def client() -> Iterator["FlaskClient"]:
    """Fixture to return a test client for the Flask app."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client: FlaskClient) -> None:
    """Test the health endpoint."""
    response = client.get("/api/v1/health")

    assert response.status_code == SUCCESS
    assert response.json.get("status") == "OK"
    assert datetime.fromisoformat(response.json.get("lastChecked"))


def test_chat_completions(client: FlaskClient) -> None:
    """Test the chat completions endpoint."""
    response = client.post(
        "/api/v1/chat/completions",
        json={"query": "Hello, how are you?"},
    )

    assert response.status_code == SUCCESS
    assert response.json.get("response") != ""
