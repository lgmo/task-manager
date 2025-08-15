import json
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from common.exceptions import CustomException


class CustomExceptionMiddleware:
    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return response

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception,
    ) -> HttpResponse:
        if isinstance(exception, CustomException):
            context = exception.get_response()

        else:
            context = CustomException(details=str(exception)).get_response()
        return HttpResponse(
            status=context.pop("status_code"),
            content_type="application/json",
            content=json.dumps(context),
        )
