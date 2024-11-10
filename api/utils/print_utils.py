import json

def out(data={}, message=None, is_success=True):
    return {
        "success": is_success,
        "message": message,
        "data": json.dumps(data)
    }