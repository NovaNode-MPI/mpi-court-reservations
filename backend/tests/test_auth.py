from __future__ import annotations

from tests.conftest import auth_headers, create_user, login_and_get_token


def assert_error(response, status_code: int, error_code: str, message: str) -> None:
    assert response.status_code == status_code
    body = response.json()
    assert body["error_code"] == error_code
    assert body["message"] == message
    assert body["details"] is None


def test_register_valid_user_returns_201(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "newuser@example.com"
    assert "id" in body
    assert "created_at" in body


def test_register_duplicate_email_returns_409(client):
    create_user(client, "duplicate@example.com")

    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
        },
    )

    assert_error(
        response,
        409,
        "conflict",
        "Email already registered",
    )


def test_login_valid_credentials_returns_200(client):
    create_user(client, "login@example.com")

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["access_token"], str)
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_invalid_credentials_returns_401(client):
    create_user(client, "wrongpass@example.com")

    response = client.post(
        "/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword",
        },
    )

    assert_error(
        response,
        401,
        "unauthorized",
        "Invalid credentials",
    )


def test_me_with_valid_token_returns_200(client):
    create_user(client, "me@example.com")
    token = login_and_get_token(client, "me@example.com")

    response = client.get(
        "/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "me@example.com"
    assert "id" in body
    assert "created_at" in body


def test_me_without_token_returns_401(client):
    response = client.get("/me")

    assert_error(
        response,
        401,
        "unauthorized",
        "Not authenticated",
    )