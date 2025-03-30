from flask import Blueprint, request, jsonify

from app.auth.utils import generate_tokens, add_user_to_whitelist
from app.middleware import role_required
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


# тестовый route для проверки работы redis
@auth_bp.route("/ping", methods=["GET"])
def ping() -> dict:
    return {"message": "server is running"}


@auth_bp.route("/login", methods=["POST"])
def login() -> jsonify():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)
    if not user or user.password != password:
        return jsonify({"message": "invalid credentials"}), 401

    access_token, refresh_token = generate_tokens(user)
    # добавление пользователя в белый список при успешной авторизации
    add_user_to_whitelist(user.id, access_token)
    return jsonify(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role_number": user.role_number
        }
    )


@auth_bp.route("/first-role", methods=["GET"])
@role_required(1)
def first_role_example() -> jsonify():
    return jsonify({"message": "route available for first role"})


@auth_bp.route("/second-role", methods=["GET"])
@role_required(2)
def second_role_example() -> jsonify():
    return jsonify({"message": "route available for second role"})
