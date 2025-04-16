import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_endpoint():
    """
    Test the health endpoint to ensure the API is running and returns uptime info.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "uptime" in data

def test_auth_token_invalid_credentials():
    """
    Test the /auth/token endpoint with invalid credentials.
    The endpoint should return 401 Unauthorized.
    """
    response = client.post(
        "/auth/token",
        data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"

# Additional tests can be added for other endpoints.
# For example, one could test user registration and then retrieve /users/me with a valid token.
# However, those tests might require configuring a test database or further dependency injection.
