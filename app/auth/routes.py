from flask import Blueprint, request, jsonify

from app.auth.utils import generate_tokens, add_user_to_whitelist, add_user_to_blacklist
from app.middleware import role_required, token_required
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


# тестовый route для проверки работы redis
@auth_bp.route("/ping", methods=["GET"])
def ping() -> dict:
    return {"message": "server is running"}


@auth_bp.route("/login", methods=["POST"])
def login():
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


# выбранный способ взаимодействия пользователей с контентом: REST API
#
# это стандартный подход для веб-приложений, использующий HTTP-методы
# он универсальный и широко используемый
#
# в сочетании с JWT-токенами обеспечивается безопасная передача данных о пользователе

# пример маршрута, доступный всем авторизованным пользователям
@auth_bp.route('/common', methods=['GET'])
@token_required
def common_endpoint():
    return jsonify({"message": "route available for every authorized user"})


# 2 примера маршрутов, доступных только пользователю с указанной ролью
@auth_bp.route("/first-role", methods=["GET"])
@role_required(1)
def first_role_example():
    return jsonify({"message": "route available for first role"})


@auth_bp.route("/second-role", methods=["GET"])
@role_required(2)
def second_role_example():
    return jsonify({"message": "route available for second role"})


@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    token = request.headers["Authorization"]
    add_user_to_blacklist(token)
    return jsonify({"message": "logout successful"})
