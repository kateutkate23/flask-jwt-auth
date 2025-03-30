import jwt
from datetime import datetime, timedelta, timezone

from flask import current_app


def generate_tokens(user):
    access = {
        "user_id": user.id,
        "role_number": user.role_number,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"])
    }
    access_token = jwt.encode(access, current_app.config["SECRET_KEY"], algorithm="HS256")

    refresh = {
        "user_id": user.id,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=current_app.config["REFRESH_TOKEN_EXPIRE_DAYS"])
    }
    refresh_token = jwt.encode(refresh, current_app.config["SECRET_KEY"], algorithm="HS256")

    return access_token, refresh_token


def add_user_to_whitelist(user_id, token):
    current_app.redis.setex(
        f"whitelist-{token}",
        current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"] * 60,
        user_id
    )
