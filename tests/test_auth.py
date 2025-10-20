"""
Tests for authentication endpoints.
"""
import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "password123",
            "full_name": "New User"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["full_name"] == "New User"
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registration with existing email fails."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "password123",
            "full_name": "Duplicate User"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    """Test registration with invalid email format."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "password": "password123",
            "full_name": "Invalid Email"
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_short_password(client):
    """Test registration with password too short."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@test.com",
            "password": "short",
            "full_name": "Short Password"
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_success(client, test_user):
    """Test successful login returns tokens."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0


def test_login_wrong_password(client, test_user):
    """Test login with wrong password fails."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with non-existent user fails."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@test.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_inactive_user(client, db, test_user):
    """Test login with inactive account fails."""
    # Deactivate user
    test_user.is_active = False
    db.commit()
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "inactive" in response.json()["detail"].lower()


def test_refresh_token_success(client, test_user):
    """Test refreshing access token with valid refresh token."""
    # First login to get tokens
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123"
        }
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh token
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert len(data["access_token"]) > 0


def test_refresh_token_invalid(client):
    """Test refresh with invalid token fails."""
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid.token.here"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_with_access_token_fails(client, user_token):
    """Test refresh with access token instead of refresh token fails."""
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": user_token}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


"""
TEST BEST PRACTICES:

1. TEST NAMING
   - Use descriptive names: test_what_when_expected
   - Examples: test_login_success, test_login_wrong_password

2. TEST STRUCTURE (AAA Pattern)
   - Arrange: Set up test data
   - Act: Call the function/endpoint
   - Assert: Check results

3. ASSERTIONS
   - Check status code first
   - Then check response data
   - Be specific (not just "success")

4. TEST COVERAGE
   - Happy path (success case)
   - Error cases (validation, auth, etc.)
   - Edge cases (inactive user, etc.)

5. FIXTURES
   - Use fixtures for common setup
   - Keep tests independent
   - Each test should work alone

RUNNING TESTS:

All tests:
    pytest

Single file:
    pytest tests/test_auth.py

Single test:
    pytest tests/test_auth.py::test_login_success

With coverage:
    pytest --cov=app --cov-report=html

Verbose output:
    pytest -v

Show print statements:
    pytest -s

WHAT TO TEST:

✓ Happy paths (successful operations)
✓ Validation errors (bad input)
✓ Authentication failures
✓ Authorization failures
✓ Edge cases (inactive users, duplicates)
✓ Security (password not in response)

✗ Don't test framework code
✗ Don't test external libraries
✗ Don't test database internals

TEST ORGANIZATION:

tests/
├── conftest.py          # Fixtures
├── test_auth.py         # Auth endpoints
├── test_users.py        # User endpoints
├── test_crud.py         # CRUD functions
└── test_security.py     # Security functions

MOCKING:

For external services:

from unittest.mock import patch

@patch('app.email.send_email')
def test_register_sends_email(mock_send, client):
    client.post("/api/v1/auth/register", json={...})
    mock_send.assert_called_once()

PARAMETRIZED TESTS:

@pytest.mark.parametrize("email,password,expected", [
    ("valid@test.com", "password123", 201),
    ("invalid", "password123", 422),
    ("valid@test.com", "short", 422),
])
def test_register_various_inputs(client, email, password, expected):
    response = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == expected
"""