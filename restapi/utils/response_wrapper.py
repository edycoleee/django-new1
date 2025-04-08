#/restapi/utils/response_wrapper.py
def success_response(message, data=None, status="success"):
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else {}
    }