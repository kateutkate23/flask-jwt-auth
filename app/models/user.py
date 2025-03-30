from __future__ import annotations
from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str
    role_number: int

    # заглушка для поиска по имени пользователя
    @staticmethod
    def find_by_username(username: str) -> User | None:
        if username == "testuser":
            return User(1, "testuser", "password", 1)
        return None
