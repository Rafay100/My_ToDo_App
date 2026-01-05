from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.models import Todo

def test_create_todo_requires_auth(client: TestClient):
    # Should fail without session cookie
    response = client.post("/api/v1/todos/?title=Test+Task")
    assert response.status_code == 401

# Integration tests for CRUD with mocked auth would go here
