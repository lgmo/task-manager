import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from accounts.models import UserModel, UserSessionModel
from accounts.services.auth_service import auth_service
from common.exceptions import CustomException

logger = logging.getLogger(__name__)


class IsAuthenticated(BaseAuthentication):
    def authenticate(
        self,
        request: Request,
    ) -> tuple[UserModel, UserSessionModel] | None:
        token = request.COOKIES.get("session_id")

        if not token:
            raise AuthenticationFailed("Missing session id")

        try:
            session = UserSessionModel.objects.filter(id=token).first()

            if not session:
                raise AuthenticationFailed("Invalid session id")

            payload = auth_service.decode_token(session.access_token)
            user = UserModel.objects.filter(cognito_id=payload["sub"]).first()
            if not user:
                raise AuthenticationFailed("Invalid token")
            request.user = user
            return user, session
        except CustomException as e:
            raise AuthenticationFailed(e.message) from e
        except Exception as e:
            raise AuthenticationFailed("Invalid token") from e

    def authenticate_header(self, request: Request) -> str:
        return "CustomToken"
