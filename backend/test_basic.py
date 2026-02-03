"""
Basic tests to verify the AI Todo Chatbot implementation
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from uuid import uuid4


client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_chat_endpoint_exists():
    """Test that the chat endpoint exists (without actually processing a message)"""
    # This test verifies the endpoint exists but doesn't actually trigger AI processing
    # since that would require API keys and external services
    user_id = str(uuid4())

    # We'll test with a mock request to verify the endpoint accepts requests
    response = client.post(f"/api/{user_id}/chat", json={
        "message": "test message",
        "conversation_id": str(uuid4())
    })

    # The endpoint should return a 422 (validation error) or 500 (due to missing API key)
    # rather than a 404 (not found), indicating the endpoint exists
    assert response.status_code in [422, 500, 401]  # 422 for validation error, 500 for API issues, 401 for auth issues


if __name__ == "__main__":
    pytest.main([__file__])