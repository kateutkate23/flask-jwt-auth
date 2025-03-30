from flask import Blueprint, request, jsonify

from app.auth.utils import generate_tokens
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/ping', methods=['GET'])
def ping():
    return {"message": "server is running"}


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.find_by_username(username)
    if not user or user.password != password:
        return jsonify({"message": "invalid credentials"}), 401

    access_token, refresh_token = generate_tokens(user)
    return jsonify(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role_number": user.role_number
        }
    )
