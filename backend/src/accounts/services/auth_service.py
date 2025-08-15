import base64
import hashlib
import hmac
from typing import TYPE_CHECKING, Any

import boto3
import requests
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.cache import cache
from jose import JWTError, jwt
from rest_framework import status

if TYPE_CHECKING:
    from types_boto3_cognito_idp import CognitoIdentityProviderClient

from common.exceptions import CustomException


class AuthService:
    def __init__(self) -> None:
        self.__aws_default_region = settings.AWS_DEFAULT_REGION

        self.__client: CognitoIdentityProviderClient = boto3.client(  # pyright: ignore
            "cognito-idp",
        )
        self.__cognito_client_id: str = settings.COGNITO_CLIENT_ID
        self.__cognito_client_secret: str = settings.COGNITO_CLIENT_SECRET
        self.__cognito_domain: str = settings.COGNITO_DOMAIN

        self.__redirect_uri = (
            f"{settings.BASE_URL}/api/v1/accounts/auth/oidc/callback"
        )
        self.__create_token_url = self._generate_token_action_url("token")
        self.__cognito_jwks_base_url = (
            f"https://cognito-idp.{self.__aws_default_region}.amazonaws.com/"
            f"{settings.COGNITO_USER_POOL_ID}"
        )

    def _get_cognito_jwks(self) -> dict[str, list[dict[str, str]]]:
        jwks = cache.get("cognito_jwks")

        if not jwks:
            response = requests.get(
                f"{self.__cognito_jwks_base_url}/.well-known/jwks.json",
                timeout=5,
            )
            response.raise_for_status()
            jwks = response.json()

            cache.set("cognito_jwks", jwks, timeout=86400)

        return jwks

    def _get_secret_hash(self, username: str) -> str:
        message = bytes(f"{username}{self.__cognito_client_id}", "utf-8")
        key = bytes(self.__cognito_client_secret, "utf-8")
        return base64.b64encode(
            hmac.new(
                key,
                message,
                digestmod=hashlib.sha256,
            ).digest()
        ).decode()

    def _generate_token_action_url(self, action: str) -> str:
        url = (
            f"https://{self.__cognito_domain}.auth."
            f"{self.__aws_default_region}.amazoncognito.com/oauth2/{action}"
        )
        return url

    def get_login_url(self) -> str:
        return (
            f"https://{self.__cognito_domain}.auth."
            f"{self.__aws_default_region}.amazoncognito.com/login?"
            f"client_id={self.__cognito_client_id}&"
            f"response_type=code&"
            f"scope=email+openid+phone&"
            f"redirect_uri={self.__redirect_uri}"
        )

    def get_logout_url(self) -> str:
        return (
            f"https://{self.__cognito_domain}.auth."
            f"{self.__aws_default_region}.amazoncognito.com/logout?"
            f"client_id={self.__cognito_client_id}&"
            f"response_type=code&"
            f"scope=email+openid+phone&"
            f"redirect_uri={self.__redirect_uri}"
        )

    def decode_token(
        self, token: str, access_token: str | None = None
    ) -> dict[str, Any]:
        if not access_token:
            access_token = token
        try:
            jwks = self._get_cognito_jwks()

            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            if not kid:
                raise CustomException(
                    message="Invalid token",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

            key = next(
                (k for k in jwks["keys"] if k.get("kid") == kid),
                None,
            )
            if not key:
                raise CustomException(
                    message="Invalid token",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=settings.COGNITO_CLIENT_ID,
                issuer=self.__cognito_jwks_base_url,
                access_token=access_token,
            )
            return payload

        except JWTError as e:
            raise CustomException(
                message="Invalid token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            ) from e

    def create_tokens(self, code: str) -> dict[str, Any]:
        try:
            data = {
                "grant_type": "authorization_code",
                "client_id": self.__cognito_client_id,
                "client_secret": self.__cognito_client_secret,
                "redirect_uri": self.__redirect_uri,
                "code": code,
            }
            res = requests.post(
                self.__create_token_url,
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                timeout=5,
            )
            res.raise_for_status()
            res = res.json()

            id_token_payload = self.decode_token(
                res["id_token"],
                res["access_token"],
            )
            return {
                "cognito_id": id_token_payload["sub"],
                "email": id_token_payload["email"],
                "access_token": res["access_token"],
                "refresh_token": res["refresh_token"],
                "expires_in": res["expires_in"],
            }
        except requests.HTTPError as e:
            if e.response.json().get("error") == "invalid_grant":
                raise CustomException(
                    message="Invalid credentials",
                    status_code=status.HTTP_400_BAD_REQUEST,
                ) from e
            raise e

    def refresh_tokens(self, refresh_token: str) -> dict[str, Any]:
        try:
            res = self.__client.get_tokens_from_refresh_token(
                RefreshToken=refresh_token,
                ClientId=self.__cognito_client_id,
                ClientSecret=self.__cognito_client_secret,
            )

            if "AuthenticationResult" not in res:
                raise CustomException(details="Missing authentication result")

            res = res["AuthenticationResult"]

            if "AccessToken" not in res:
                raise CustomException(details="Missing access token")

            if "ExpiresIn" not in res:
                raise CustomException(details="Missing expires in")

            return {
                "access_token": res["AccessToken"],
                "expires_in": res["ExpiresIn"],
            }
        except ClientError as e:
            raise CustomException(
                message="Invalid credentials",
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e


auth_service = AuthService()
