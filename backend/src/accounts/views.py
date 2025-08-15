from datetime import UTC, datetime, timedelta

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import UserModel, UserSessionModel
from accounts.services.auth_service import auth_service
from common.authentications import IsAuthenticated


@extend_schema(
    tags=["Auth"],
)
class AuthView(viewsets.GenericViewSet):
    @extend_schema(
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "login_url": {
                        "type": "string",
                        "example": "https://idp.com/auth?response_type=code...",
                    }
                },
            },
        }
    )
    @action(detail=False, methods=["post"], url_path="login")
    def get_login_url(self, _: Request) -> Response:
        login_url = auth_service.get_login_url()
        return Response({"login_url": login_url}, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_302_FOUND: None},
    )
    @action(detail=False, methods=["get"], url_path="oidc/callback")
    def oidc_callback(self, request: Request) -> Response:
        auth_code = request.GET.get("code")

        if not auth_code:
            return Response(
                {"error": "Missing authorization code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        res = auth_service.create_tokens(auth_code)

        user = UserModel.objects.filter(cognito_id=res["cognito_id"]).first()
        if not user:
            user = UserModel.objects.create(
                email=res["email"],
                cognito_id=res["cognito_id"],
            )
        else:
            UserSessionModel.objects.filter(
                user=user,
                expires_at__lt=datetime.now(UTC),
            ).delete()

        session = UserSessionModel.objects.create(
            user=user,
            access_token=res["access_token"],
            refresh_token=res["refresh_token"],
            expires_at=datetime.now(UTC)
            + timedelta(seconds=res["expires_in"]),
        )

        response = Response(
            status=status.HTTP_302_FOUND,
            headers={
                "Location": settings.FRONTEND_HOME_URL,
            },
        )

        response.set_cookie(
            key="session_id",
            value=str(session.id),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            max_age=res["expires_in"],
        )

        return response

    @action(detail=False, methods=["post"], url_path="refresh-tokens")
    def refresh_tokens(self, request: Request) -> Response:
        session_id = request.COOKIES.get("session_id")

        if not session_id:
            return Response(
                {"error": "Missing session id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = UserSessionModel.objects.filter(id=session_id).first()

        if not session:
            return Response(
                {"error": "Invalid session id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens = auth_service.refresh_tokens(session.refresh_token)

        session.access_token = tokens["access_token"]
        session.expires_at = datetime.now(UTC) + timedelta(
            seconds=tokens["expires_in"],
        )
        session.save()

        UserSessionModel.objects.filter(
            user=session.user,
            expires_at__lt=datetime.now(UTC),
        ).delete()

        response = Response(status=status.HTTP_200_OK)

        response.set_cookie(
            key="session_id",
            value=str(session.id),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            max_age=tokens["expires_in"],
        )

        return response

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request: Request) -> Response:
        response = Response(
            {"logout_url": auth_service.get_logout_url()},
            status=status.HTTP_200_OK,
        )

        session_id = request.COOKIES.get("session_id")

        if session_id:
            UserSessionModel.objects.filter(id=session_id).delete()

        response.delete_cookie(
            "session_id",
            path="/",
        )
        return response


@extend_schema(
    tags=["Auth"],
)
class AuthCheckView(viewsets.GenericViewSet):
    authentication_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="auth/check")
    def check(self, _: Request) -> Response:
        return Response(status=status.HTTP_200_OK)
