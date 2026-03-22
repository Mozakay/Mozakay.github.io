from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass


# Represents a user in the system
@dataclass
class User:
    username: str
    password_hash: str
    role: str


# Abstract repository that defines how users should be stored and retrieved
class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass


# Simple in-memory repository using a dictionary instead of a real database
class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        # Stores users with the username as the key
        self._users: dict[str, User] = {}

    def add(self, user: User) -> None:
        # Add or update a user in the dictionary
        self._users[user.username] = user

    def get_by_username(self, username: str) -> User | None:
        # Return the user if found, otherwise return None
        return self._users.get(username)


# Service class that contains the business logic for registration and login
class UserService:
    def __init__(self, repository: UserRepository) -> None:
        # Accepts any repository that follows the UserRepository interface
        self.repository = repository

    def register_user(self, username: str, password: str, role: str) -> User:
        # Check that the username is not empty or only spaces
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")

        # Check that the password is not empty or only spaces
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")

        # Prevent duplicate usernames
        if self.repository.get_by_username(username) is not None:
            raise ValueError("Username already exists")

        # Hash the password before storing it
        password_hash = self._hash_password(password)

        # Create a new user object
        user = User(username=username, password_hash=password_hash, role=role)

        # Save the user in the repository
        self.repository.add(user)

        # Return the newly registered user
        return user

    def login(self, username: str, password: str) -> bool:
        # Reject login if username or password is missing
        if not username or not password:
            return False

        # Find the user by username
        user = self.repository.get_by_username(username)

        # Return False if the user does not exist
        if user is None:
            return False

        # Compare the stored password hash with the hash of the entered password
        return user.password_hash == self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> str:
        # Convert the password into a SHA-256 hash
        return hashlib.sha256(password.encode("utf-8")).hexdigest()