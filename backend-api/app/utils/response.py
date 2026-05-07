def success_response(message: str, data=None, meta=None):
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta
    }


def error_response(message: str,errors=None):
    return {
        "success": False,
        "message": message,
        "error": errors,
        "data": None
    }