import uuid

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import UserModel, UserSessionModel
from accounts.services.auth_service import AuthService


@pytest.mark.django_db
def test_login_view(
    auth_service: AuthService,
    client: APIClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr(
        "accounts.views.auth_service.get_login_url",
        lambda: auth_service.get_login_url(),
    )
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123",
    }
    url = reverse("auth-get-login-url")

    # Act
    response = client.post(url, data=user_data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("login_url") == auth_service.get_login_url()


@pytest.mark.django_db
def test_oidc_callback_view(
    client: APIClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    access_token = "test_access_token"  # noqa: S105
    refresh_token = "test_refresh_token"  # noqa: S105
    tokens = {
        "cognito_id": str(uuid.uuid4()),
        "email": "test@example.com",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
    }
    monkeypatch.setattr(
        "accounts.views.auth_service.create_tokens",
        lambda auth_code: tokens,
    )
    url = reverse("auth-oidc-callback") + "?code=test_auth_code"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers.get("Location") == settings.FRONTEND_HOME_URL
    user = UserModel.objects.filter(email="test@example.com").first()
    assert user is not None
    assert str(user.cognito_id) == tokens["cognito_id"]
    session = UserSessionModel.objects.filter(user=user).first()
    assert session is not None
    assert str(session.id) == response.cookies.get("session_id").value
    assert session.access_token == access_token
    assert session.refresh_token == refresh_token
    assert session.expires_at is not None
    assert session.user.id == user.id


@pytest.mark.django_db
def test_oidc_callback_view_missing_code(client: APIClient) -> None:
    # Arrange
    url = reverse("auth-oidc-callback")

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get("error") == "Missing authorization code."


@pytest.mark.django_db
def test_logout_view(
    client: APIClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    access_token = "test_access_token"  # noqa: S105
    refresh_token = "test_refresh_token"  # noqa: S105
    tokens = {
        "cognito_id": str(uuid.uuid4()),
        "email": "test@example.com",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
    }
    monkeypatch.setattr(
        "accounts.views.auth_service.create_tokens",
        lambda auth_code: tokens,
    )
    url = reverse("auth-oidc-callback") + "?code=test_auth_code"
    response = client.get(url)
    url = reverse("auth-logout")

    # Assert
    session = UserSessionModel.objects.first()
    assert session is not None
    assert str(session.id) == response.cookies.get("session_id").value

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert "" == response.cookies.get("session_id").value


@pytest.mark.django_db
def test_refresh_tokens_view(
    client: APIClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    access_token = "test_access_token"  # noqa: S105
    refresh_token = "test_refresh_token"  # noqa: S105
    tokens = {
        "cognito_id": str(uuid.uuid4()),
        "email": "test@example.com",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
    }
    url = reverse("auth-oidc-callback") + "?code=test_auth_code"
    monkeypatch.setattr(
        "accounts.views.auth_service.create_tokens",
        lambda auth_code: tokens,
    )
    response = client.get(url)

    # Assert
    session = UserSessionModel.objects.first()
    assert session is not None
    assert str(session.id) == response.cookies.get("session_id").value

    # Arrange
    new_access_token = "test_new_access_token"  # noqa: S105
    tokens = {
        "access_token": new_access_token,
        "expires_in": 3600,
    }
    monkeypatch.setattr(
        "accounts.views.auth_service.refresh_tokens",
        lambda refresh_token: tokens,
    )
    url = reverse("auth-refresh-tokens")

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    new_session = UserSessionModel.objects.first()
    assert UserSessionModel.objects.count() == 1
    assert new_session is not None
    assert session.id == new_session.id
    assert str(new_session.id) == response.cookies.get("session_id").value
    assert session.access_token != new_session.access_token


@pytest.mark.django_db
def test_refresh_tokens_view_missing_refresh_token(client: APIClient) -> None:
    # Arrange
    url = reverse("auth-refresh-tokens")

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get("error") == "Missing session id."
