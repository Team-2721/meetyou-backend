from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["ok"] = False
        response.data["status_code"] = response.status_code
        return response
    else:
        data = {
            "ok": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": exc.args[0],
        }
        return data
