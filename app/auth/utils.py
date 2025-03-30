import jwt
from datetime import datetime, timedelta, timezone

from flask import current_app

from app.models.user import User


def generate_tokens(user: User) -> tuple[str, str]:
    access = {
        "user_id": user.id,
        "role_number": user.role_number,
        "expires_at": (datetime.now(timezone.utc) + timedelta(
            minutes=current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"])).strftime("%m/%d/%Y %I:%M:%S"),
    }
    access_token = jwt.encode(access, current_app.config["SECRET_KEY"], algorithm="HS256")

    refresh = {
        "user_id": user.id,
        "expires_at": (datetime.now(timezone.utc) + timedelta(
            days=current_app.config["REFRESH_TOKEN_EXPIRE_DAYS"])).strftime("%m/%d/%Y %I:%M:%S"),
    }
    refresh_token = jwt.encode(refresh, current_app.config["SECRET_KEY"], algorithm="HS256")

    return access_token, refresh_token


def add_user_to_whitelist(user_id: int, token: str) -> None:
    current_app.redis.setex(
        f"whitelist-{token}",
        current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"] * 60,
        user_id
    )


def add_user_to_blacklist(token: str) -> None:
    current_app.redis.setex(
        f"blacklist-{token}",
        current_app.config["ACCESS_TOKEN_EXPIRE_MINUTES"] * 60,
        "blacklisted"
    )


def is_in_blacklist(token: str) -> bool:
    return current_app.redis.exists(f"blacklist-{token}")
