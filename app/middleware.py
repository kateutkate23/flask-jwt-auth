from functools import wraps
from typing import Callable

from flask import request, jsonify, current_app
import jwt


# проверка наличия токена
def token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return jsonify({"message": "token is missing"}), 401

        try:
            decoded_token = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = decoded_token["user_id"]
            request.role_number = decoded_token["role_number"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "token is expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated


# проверка роли
def role_required(role_number: int) -> Callable:
    def decorated(f: Callable) -> Callable:
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            if request.role_number != role_number:
                return jsonify({"message": "not enough rights for access"}), 403

            return f(*args, **kwargs)

        return decorated

    return decorated
