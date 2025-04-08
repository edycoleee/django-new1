#/restapi/utils/exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from restapi.utils.response_wrapper import success_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = response.data.get('detail') if 'detail' in response.data else "Something went wrong"
        return Response(success_response(
            message=message,
            data={},
            status="error"
        ), status=response.status_code)

    # Untuk unhandled exception
    return Response(success_response(
        message=str(exc),
        data={},
        status="error"
    ), status=500)
