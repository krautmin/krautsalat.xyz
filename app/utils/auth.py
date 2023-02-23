from functools import wraps
from quart import current_app, make_response, jsonify, request


def api_key_required(f):
    @wraps(f)
    async def decorator(*args, **kwargs):
        token = None
        # ensure the api key is passed with the headers
        if "x-api-key" in request.headers:
            token = request.headers["x-api-key"]
        if not token:  # throw error if no token provided
            return await make_response(
                jsonify({"message": "A valid token is missing!"}), 401
            )
        elif token != current_app.config["API_KEY"]:
            return await make_response(jsonify({"message": "Invalid token!!"}), 401)
        return await f(*args, **kwargs)

    return decorator
