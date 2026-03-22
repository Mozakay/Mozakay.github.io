from __future__ import annotations

import hashlib


class User:
    def __init__(self, username: str, password_hash: str, role: str) -> None:
        self.username = username
        self.password_hash = password_hash
        self.role = role


class UserService:
    def __init__(self) -> None:
        # Store all users directly inside the service
        self.users: dict[str, User] = {}

    def register_user(self, username: str, password: str, role: str) -> User:
        # Basic input validation
        if username == "" or username is None:
            raise ValueError("Username cannot be empty")

        if password == "" or password is None:
            raise ValueError("Password cannot be empty")

        # Check duplicate username
        if username in self.users:
            raise ValueError("Username already exists")

        # Hash password
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Create and store user
        user = User(username, password_hash, role)
        self.users[username] = user

        return user

    def login(self, username: str, password: str) -> bool:
        if username == "" or username is None:
            return False

        if password == "" or password is None:
            return False

        if username not in self.users:
            return False

        user = self.users[username]
        entered_password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        if user.password_hash == entered_password_hash:
            return True
        else:
            return False