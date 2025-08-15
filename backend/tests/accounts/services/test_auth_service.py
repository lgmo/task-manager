import base64
import hashlib
import hmac
from unittest.mock import MagicMock, patch

import pytest
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from requests import Response

from accounts.services.auth_service import AuthService
from common.exceptions import CustomException


def test__get_secret_hash(auth_service: AuthService) -> None:
    # Arrange
    username = "testuser"
    client_id = auth_service._AuthService__cognito_client_id
    client_secret = auth_service._AuthService__cognito_client_secret

    message = f"{username}{client_id}".encode("utf-8")
    key = client_secret.encode("utf-8")
    expected_hash = base64.b64encode(
        hmac.new(key, message, digestmod=hashlib.sha256).digest()
    ).decode()

    # Act
    secret_hash = auth_service._get_secret_hash(username)

    # Assert
    assert secret_hash == expected_hash


def test__generate_token_action_url(auth_service: AuthService) -> None:
    # Arrange
    expected_url = (
        "https://domain.auth.us-east-1.amazoncognito.com/oauth2/token"
    )

    # Act
    res = auth_service._generate_token_action_url("token")

    # Assert
    assert res == expected_url


def test_get_login_url(auth_service: AuthService) -> None:
    # Arrange
    expected_login_url = (
        "https://domain.auth.us-east-1.amazoncognito.com/login?"
        "client_id=client_id&"
        "response_type=code&"
        "scope=email+openid+phone&"
        "redirect_uri=https://base_url/api/v1/accounts/auth/oidc/callback"
    )

    # Act
    login_url = auth_service.get_login_url()

    # Assert
    assert login_url == expected_login_url


@patch("requests.post")
@patch("accounts.services.auth_service.AuthService.decode_token")
def test_create_tokens(
    mock_decode_token: MagicMock,
    mock_post: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    code = "authorization_code"
    access_token = "access_token"  # noqa: S105
    id_token = "id_token"  # noqa: S105
    refresh_token = "refresh_token"  # noqa: S105
    expires_in = 3600
    cognito_id = "cognito_id"
    email = "user@example.com"
    mock_decode_token.return_value = {
        "sub": cognito_id,
        "email": email,
    }

    mock_post.return_value.json.return_value = {
        "id_token": id_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
    }
    mock_post.return_value.status_code = 200

    # Act
    tokens = auth_service.create_tokens(code)

    # Assert
    assert tokens == {
        "cognito_id": cognito_id,
        "email": email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
    }


@patch("requests.post")
def test_create_tokens_invalid_credentials(
    mock_post: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    code = "authorization_code"
    response = Response()
    response.status_code = 400
    response._content = b'{"error": "invalid_grant"}'
    mock_post.return_value = response

    # Act
    with pytest.raises(CustomException, match="Invalid credentials"):
        auth_service.create_tokens(code)

    # Assert
    mock_post.assert_called_once_with(
        auth_service._AuthService__create_token_url,
        data={
            "grant_type": "authorization_code",
            "client_id": auth_service._AuthService__cognito_client_id,
            "client_secret": auth_service._AuthService__cognito_client_secret,
            "redirect_uri": auth_service._AuthService__redirect_uri,
            "code": code,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=5,
    )


@patch("accounts.services.auth_service.cache")
@patch("accounts.services.auth_service.requests.get")
def test__get_cognito_jwks_cache_hit(
    mock_get: MagicMock,
    mock_cache: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    jwks = {"keys": [{"kid": "test"}]}
    mock_cache.get.return_value = jwks

    # Act
    result = auth_service._get_cognito_jwks()

    # Assert
    assert result == jwks
    mock_cache.get.assert_called_once_with("cognito_jwks")
    mock_get.assert_not_called()


@patch("accounts.services.auth_service.cache")
@patch("accounts.services.auth_service.requests.get")
def test__get_cognito_jwks_cache_miss(
    mock_get: MagicMock,
    mock_cache: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    jwks = {"keys": [{"kid": "test"}]}
    mock_cache.get.return_value = None
    mock_response = MagicMock()
    mock_response.json.return_value = jwks
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    result = auth_service._get_cognito_jwks()

    # Assert
    assert result == jwks
    mock_cache.set.assert_called_once_with("cognito_jwks", jwks, timeout=86400)
    mock_get.assert_called_once()


@patch("accounts.services.auth_service.jwt")
@patch("accounts.services.auth_service.cache")
def test_decode_token_valid(
    mock_cache: MagicMock,
    mock_jwt: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    token = "valid_token"  # noqa: S105
    jwks = {"keys": [{"kid": "test_kid"}]}
    mock_cache.get.return_value = jwks
    mock_jwt.get_unverified_header.return_value = {"kid": "test_kid"}
    mock_jwt.decode.return_value = {"sub": "user_id"}

    # Act
    payload = auth_service.decode_token(token)

    # Assert
    assert payload == {"sub": "user_id"}
    mock_jwt.get_unverified_header.assert_called_once_with(token)
    mock_jwt.decode.assert_called_once()


@patch("accounts.services.auth_service.jwt")
@patch("accounts.services.auth_service.cache")
def test_decode_token_valid_refresh_token(
    mock_cache: MagicMock,
    mock_jwt: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    token = "valid_token"  # noqa: S105
    access_token = "access_token"  # noqa: S105
    jwks = {"keys": [{"kid": "test_kid"}]}
    mock_cache.get.return_value = jwks
    mock_jwt.get_unverified_header.return_value = {"kid": "test_kid"}
    mock_jwt.decode.return_value = {"sub": "user_id"}

    # Act
    payload = auth_service.decode_token(token, access_token)

    # Assert
    assert payload == {"sub": "user_id"}
    mock_jwt.get_unverified_header.assert_called_once_with(token)
    mock_jwt.decode.assert_called_once()


@patch("accounts.services.auth_service.jwt")
@patch("accounts.services.auth_service.cache")
def test_decode_token_no_kid(
    mock_cache: MagicMock,
    mock_jwt: MagicMock,
    auth_service: AuthService,
) -> None:
    # Arrange
    token = "token"  # noqa: S105
    jwks = {"keys": []}
    mock_cache.get.return_value = jwks
    mock_jwt.get_unverified_header.return_value = {}

    # Act & Assert
    with pytest.raises(CustomException, match="Invalid token"):
        auth_service.decode_token(token)


@patch("accounts.services.auth_service.jwt")
@patch("accounts.services.auth_service.cache")
def test_decode_token_kid_not_found(
    mock_cache: MagicMock, mock_jwt: MagicMock, auth_service: AuthService
) -> None:
    # Arrange
    token = "token"  # noqa: S105
    jwks = {"keys": [{"kid": "other_kid"}]}
    mock_cache.get.return_value = jwks
    mock_jwt.get_unverified_header.return_value = {"kid": "test_kid"}

    # Act & Assert
    with pytest.raises(CustomException, match="Invalid token"):
        auth_service.decode_token(token)


@patch("accounts.services.auth_service.jwt")
@patch("accounts.services.auth_service.cache")
def test_decode_token_expired(
    mock_cache: MagicMock, mock_jwt: MagicMock, auth_service: AuthService
) -> None:
    # Arrange
    token = "token"  # noqa: S105
    jwks = {"keys": [{"kid": "test_kid"}]}
    mock_cache.get.return_value = jwks
    mock_jwt.get_unverified_header.return_value = {"kid": "test_kid"}
    mock_jwt.decode.side_effect = ExpiredSignatureError()

    # Act & Assert
    with pytest.raises(CustomException, match="Invalid token"):
        auth_service.decode_token(token)


@patch("accounts.services.auth_service.jwt")
@patch("accounts.services.auth_service.cache")
def test_decode_token_jwt_error(
    mock_cache: MagicMock, mock_jwt: MagicMock, auth_service: AuthService
) -> None:
    # Arrange
    token = "token"  # noqa: S105
    jwks = {"keys": [{"kid": "test_kid"}]}
    mock_cache.get.return_value = jwks
    mock_jwt.get_unverified_header.return_value = {"kid": "test_kid"}
    mock_jwt.decode.side_effect = JWTError()

    # Act & Assert
    with pytest.raises(CustomException, match="Invalid token"):
        auth_service.decode_token(token)


def test_refresh_tokens(auth_service: AuthService) -> None:
    # Arrange
    refresh_token = "refresh_token"  # noqa: S105
    access_token = "access_token"  # noqa: S105
    expires_in = "expires_in"
    get_tokens_from_refresh_token = (
        auth_service._AuthService__client.get_tokens_from_refresh_token
    )
    get_tokens_from_refresh_token.return_value = {
        "AuthenticationResult": {
            "AccessToken": access_token,
            "ExpiresIn": expires_in,
        }
    }

    # Act
    result = auth_service.refresh_tokens(refresh_token)

    # Assert
    assert result == {
        "access_token": access_token,
        "expires_in": expires_in,
    }
    get_tokens_from_refresh_token.assert_called_once_with(
        RefreshToken=refresh_token,
        ClientId=auth_service._AuthService__cognito_client_id,
        ClientSecret=auth_service._AuthService__cognito_client_secret,
    )


def test_refresh_tokens_missing_access_token(
    auth_service: AuthService,
) -> None:
    # Arrange
    refresh_token = "refresh_token"  # noqa: S105
    expires_in = "expires_in"
    get_tokens_from_refresh_token = (
        auth_service._AuthService__client.get_tokens_from_refresh_token
    )
    get_tokens_from_refresh_token.return_value = {
        "AuthenticationResult": {
            "ExpiresIn": expires_in,
        }
    }

    # Act
    with pytest.raises(CustomException, match="Internal Server Error"):
        auth_service.refresh_tokens(refresh_token)

    # Assert
    get_tokens_from_refresh_token.assert_called_once_with(
        RefreshToken=refresh_token,
        ClientId=auth_service._AuthService__cognito_client_id,
        ClientSecret=auth_service._AuthService__cognito_client_secret,
    )


def test_refresh_tokens_missing_expires_in(
    auth_service: AuthService,
) -> None:
    # Arrange
    refresh_token = "refresh_token"  # noqa: S105
    access_token = "access_token"  # noqa: S105
    get_tokens_from_refresh_token = (
        auth_service._AuthService__client.get_tokens_from_refresh_token
    )
    get_tokens_from_refresh_token.return_value = {
        "AuthenticationResult": {
            "AccessToken": access_token,
        }
    }

    # Act
    with pytest.raises(CustomException, match="Internal Server Error"):
        auth_service.refresh_tokens(refresh_token)

    # Assert
    get_tokens_from_refresh_token.assert_called_once_with(
        RefreshToken=refresh_token,
        ClientId=auth_service._AuthService__cognito_client_id,
        ClientSecret=auth_service._AuthService__cognito_client_secret,
    )


def test_refresh_tokens_missing_authentication_result(
    auth_service: AuthService,
) -> None:
    # Arrange
    refresh_token = "refresh_token"  # noqa: S105
    get_tokens_from_refresh_token = (
        auth_service._AuthService__client.get_tokens_from_refresh_token
    )
    get_tokens_from_refresh_token.return_value = {}

    # Act
    with pytest.raises(CustomException, match="Internal Server Error"):
        auth_service.refresh_tokens(refresh_token)

    # Assert
    get_tokens_from_refresh_token.assert_called_once_with(
        RefreshToken=refresh_token,
        ClientId=auth_service._AuthService__cognito_client_id,
        ClientSecret=auth_service._AuthService__cognito_client_secret,
    )
