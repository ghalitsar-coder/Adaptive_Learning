def build_response(success: bool, **kwargs):
    response = {
        "success": success
    }
    response.update(kwargs)
    return response
