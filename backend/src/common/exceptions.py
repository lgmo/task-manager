import logging
from typing import Any

from rest_framework import status

logger = logging.getLogger(__name__)


class CustomException(Exception):
    def __init__(
        self,
        message: str = "Internal Server Error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: str | None = None,
        **extra: dict[str, Any],
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = (
            details
            if status_code != status.HTTP_500_INTERNAL_SERVER_ERROR
            else None
        )
        self.extra = extra
        logger.error(
            f"Erro {status_code}: {message} - Details: {details}",
            exc_info=True,
        )

    def get_response(self) -> dict[str, Any]:
        context = {
            "status_code": self.status_code,
            "message": self.message,
            "details": self.details,
            **self.extra,
        }
        context = {k: v for k, v in context.items() if v is not None}
        return context
