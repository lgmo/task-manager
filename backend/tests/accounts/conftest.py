from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from django.conf import settings

from accounts.services.auth_service import AuthService


@pytest.fixture
def mocked_settings() -> Generator[None, None, None]:
    with patch.multiple(
        settings,
        AWS_DEFAULT_REGION="us-east-1",
        BASE_URL="https://base_url",
        COGNITO_CLIENT_ID="client_id",
        COGNITO_CLIENT_SECRET="client_secret",  # noqa: S106
        COGNITO_USER_POOL_ID="user_pool_id",
        COGNITO_DOMAIN="domain",
    ):
        yield


@pytest.fixture
def mock_cognito_client() -> Generator[MagicMock, None, None]:
    with patch("accounts.services.auth_service.boto3.client") as mock_client:
        mock_cognito = MagicMock()
        mock_client.return_value = mock_cognito
        yield mock_cognito


@pytest.fixture
def auth_service(
    mocked_settings: Generator[None, None, None],
    mock_cognito_client: MagicMock,
) -> AuthService:
    return AuthService()
