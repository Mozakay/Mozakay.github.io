from __future__ import annotations

import hashlib
import hmac
import os
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Deque, Dict, Iterable, List, Mapping, NoReturn, Optional, Sequence, Tuple
from types import MappingProxyType


from core_banking import Account, _validate_amount as validate_amount

# ─────────────────────────────────────────────────────────────────────────────
# Module-level constants
# ─────────────────────────────────────────────────────────────────────────────

_SALT_BYTES = 32
_PBKDF2_ITERATIONS = 100_000
_MIN_PASSWORD_LENGTH = 8
_MIN_PASSWORD_DIGITS = 1
_DEFAULT_MAX_ATTEMPTS = 3
_DEFAULT_LOCKOUT_SEC = 30.0
_DEFAULT_SESSION_SEC = 300.0
_DEFAULT_MAX_AUTH_EVENTS = 5_000
_DEFAULT_MAX_SECURITY_EVENTS = 5_000
_DEFAULT_MAX_ALERTS = 1_000


# =============================================================================
# SECTION 1 — SECURITY EXCEPTIONS
# =============================================================================


class AuthenticationError(PermissionError):
    """Raised when authentication fails."""


class AccountLockedError(PermissionError):
    """Raised when a user account is temporarily locked."""


class AccountNotFoundError(KeyError):
    """Raised when a requested bank account number is not registered."""


class AuthorizationError(PermissionError):
    """Raised when an authenticated user lacks permission."""


class FraudAlertError(ValueError):
    """Raised when a transaction is flagged as suspicious."""



class RateLimitExceededError(PermissionError):
    """Raised when a user exceeds their allowed request frequency."""


# =============================================================================
# SECTION 2 — CLOCK, HASHING, VALIDATION, USER MODEL
# =============================================================================


def _normalize_username(username: str) -> str:
    if not isinstance(username, str):
        raise TypeError("username must be a string")
    normalized = username.strip().casefold()
    if not normalized:
        raise ValueError("username must be a non-empty string")
    return normalized

def _normalize_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _format_datetime(value: datetime) -> str:
    return _normalize_datetime(value, "value").isoformat()



class IPasswordPolicy(ABC):
    @abstractmethod
    def validate(self, password: str) -> None:
        pass

class BasicPasswordPolicy(IPasswordPolicy):
    def __init__(
        self,
        min_length: int = _MIN_PASSWORD_LENGTH,
        min_digits: int = _MIN_PASSWORD_DIGITS,
        allow_spaces: bool = False,
    ) -> None:
        if min_length < 1:
            raise ValueError("min_length must be >= 1")
        if min_digits < 0:
            raise ValueError("min_digits must be >= 0")
        if not isinstance(allow_spaces, bool):
            raise TypeError("allow_spaces must be a bool")
        self._min_length = int(min_length)
        self._min_digits = int(min_digits)
        self._allow_spaces = allow_spaces

    def validate(self, password: str) -> None:
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if not password:
            raise ValueError("password must be a non-empty string")
        if len(password) < self._min_length:
            raise ValueError(
                f"Password must be at least {self._min_length} characters long"
            )
        if not self._allow_spaces and any(c.isspace() for c in password):
            raise ValueError("Password must not contain spaces")
        digit_count = sum(1 for c in password if c.isdigit())
        if digit_count < self._min_digits:
            raise ValueError(
                f"Password must contain at least {self._min_digits} digit(s)"
            )


class IClock(ABC):
    @abstractmethod
    def monotonic(self) -> float:
        pass

    @abstractmethod
    def now(self) -> datetime:
        pass


class SystemClock(IClock):
    def monotonic(self) -> float:
        return time.monotonic()

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str, salt: bytes) -> bytes:
        pass

    def verify_password(self, password: str, salt: bytes, expected_hash: bytes) -> bool:
        candidate = self.hash_password(password, salt)
        return hmac.compare_digest(expected_hash, candidate)


class PBKDF2PasswordHasher(IPasswordHasher):
    def __init__(self, iterations: int = _PBKDF2_ITERATIONS) -> None:
        if iterations < 1:
            raise ValueError("iterations must be >= 1")
        self._iterations = int(iterations)

    def hash_password(self, password: str, salt: bytes) -> bytes:
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if not isinstance(salt, bytes):
            raise TypeError("salt must be bytes")
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            self._iterations,
        )


@dataclass(frozen=True, slots=True)
class User:
    username: str
    salt: bytes = field(repr=False)
    password_hash: bytes = field(repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "username", _normalize_username(self.username))
        if not isinstance(self.salt, bytes) or not self.salt:
            raise ValueError("salt must be non-empty bytes")
        if not isinstance(self.password_hash, bytes) or not self.password_hash:
            raise ValueError("password_hash must be non-empty bytes")

    @classmethod
    def create(
        cls,
        username: str,
        password: str,
        hasher: IPasswordHasher,
        password_policy: IPasswordPolicy,
    ) -> "User":
        normalized_username = _normalize_username(username)
        if not isinstance(hasher, IPasswordHasher):
            raise TypeError("hasher must implement IPasswordHasher")
        if not isinstance(password_policy, IPasswordPolicy):
            raise TypeError("password_policy must implement IPasswordPolicy")

        password_policy.validate(password)

        salt = os.urandom(_SALT_BYTES)
        return cls(
            username=normalized_username,
            salt=salt,
            password_hash=hasher.hash_password(password, salt),
        )

    def verify_password(self, password: str, hasher: IPasswordHasher) -> bool:
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if not isinstance(hasher, IPasswordHasher):
            raise TypeError("hasher must implement IPasswordHasher")
        return hasher.verify_password(password, self.salt, self.password_hash)

class IUserStore(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def contains(self, username: str) -> bool:
        pass


class InMemoryUserStore(IUserStore):
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._lock = threading.RLock()

    def add(self, user: User) -> None:
        if not isinstance(user, User):
            raise TypeError("user must be a User")
        username = _normalize_username(user.username)
        with self._lock:
            if username in self._users:
                raise ValueError(f"Username '{username}' is already registered")
            self._users[username] = user

    def get(self, username: str) -> Optional[User]:
        normalized = _normalize_username(username)
        with self._lock:
            return self._users.get(normalized)

    def contains(self, username: str) -> bool:
        normalized = _normalize_username(username)
        with self._lock:
            return normalized in self._users


# =============================================================================
# SECTION 3 — AUTHENTICATION
# =============================================================================
class AuthAction(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    LOCKOUT = "lockout"
    BLOCKED_LOGIN = "blocked_login"

class AuthStatus(Enum):
    PASS = "PASS"
    FAILED = "FAILED"
    LOCKED = "LOCKED"
    BLOCKED = "BLOCKED"

@dataclass(frozen=True, slots=True)
class AuthEvent:
    timestamp: datetime
    username: str
    action: AuthAction
    status: AuthStatus
    message: str
    affected_accounts: Tuple[int, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", _normalize_datetime(self.timestamp, "timestamp"))
        object.__setattr__(self, "username", _normalize_username(self.username))
        if not isinstance(self.action, AuthAction):
            raise TypeError("action must be an AuthAction")
        if not isinstance(self.status, AuthStatus):
            raise TypeError("status must be an AuthStatus")
        if not isinstance(self.message, str):
            raise TypeError("message must be a string")

        normalized_accounts: List[int] = []
        for account in self.affected_accounts:
            if not isinstance(account, int):
                raise TypeError("affected_accounts must contain int values")
            normalized_accounts.append(account)
        object.__setattr__(
            self,
            "affected_accounts",
            tuple(sorted(set(normalized_accounts))),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": _format_datetime(self.timestamp),
            "username": self.username,
            "action": self.action.value,
            "status": self.status.value,
            "message": self.message,
            "affected_accounts": list(self.affected_accounts),
        }


@dataclass(frozen=True, slots=True)
class AuthConfig:
    max_attempts: int = _DEFAULT_MAX_ATTEMPTS
    lockout_seconds: float = _DEFAULT_LOCKOUT_SEC
    session_timeout_seconds: float = _DEFAULT_SESSION_SEC

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.lockout_seconds <= 0:
            raise ValueError("lockout_seconds must be > 0")
        if self.session_timeout_seconds <= 0:
            raise ValueError("session_timeout_seconds must be > 0")


@dataclass(frozen=True, slots=True)
class LockoutResult:
    attempts: int
    now_locked: bool
    remaining_seconds: float

    def __post_init__(self) -> None:
        if not isinstance(self.attempts, int) or self.attempts < 0:
            raise ValueError("attempts must be a non-negative integer")
        if not isinstance(self.now_locked, bool):
            raise TypeError("now_locked must be a bool")
        if not isinstance(self.remaining_seconds, (int, float)) or self.remaining_seconds < 0:
            raise ValueError("remaining_seconds must be a non-negative number")


@dataclass(frozen=True, slots=True)
class SessionInfo:
    session_id: str
    username: str
    created_at: float
    last_activity_at: float

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, str) or not self.session_id:
            raise ValueError("session_id must be a non-empty string")
        object.__setattr__(self, "username", _normalize_username(self.username))
        object.__setattr__(self, "created_at", float(self.created_at))
        object.__setattr__(self, "last_activity_at", float(self.last_activity_at))


@dataclass(frozen=True, slots=True)
class AuthSession:
    session_id: str
    user: User

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, str) or not self.session_id:
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(self.user, User):
            raise TypeError("user must be a User")


class IUserRegistrar(ABC):
    @abstractmethod
    def register_user(self, username: str, password: str) -> User:
        pass


class IAuthenticator(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def logout(self, username: str) -> None:
        pass

    @abstractmethod
    def is_authenticated_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def touch_user(self, username: str) -> None:
        pass

    @abstractmethod
    def is_locked(self, username: str) -> bool:
        pass

    @abstractmethod
    def failed_attempts(self, username: str) -> int:
        pass


class ISessionAwareAuthenticator(IAuthenticator, ABC):
    @abstractmethod
    def authenticate_session(self, username: str, password: str) -> AuthSession:
        pass

    @abstractmethod
    def is_authenticated_session(self, auth_session: AuthSession) -> bool:
        pass

    @abstractmethod
    def touch_session(self, session_id: str) -> None:
        pass

    @abstractmethod
    def logout_session(self, session_id: str) -> None:
        pass


class IAuthAuditReader(ABC):
    @abstractmethod
    def get_auth_events(self) -> List[AuthEvent]:
        pass


class IAuthEventLogger(ABC):
    @abstractmethod
    def record(self, event: AuthEvent) -> None:
        pass


class IAuthEventJournal(IAuthEventLogger, IAuthAuditReader, ABC):
    pass


class IAuthEventRecorder(ABC):
    @abstractmethod
    def record(
        self,
        username: str,
        action: AuthAction,
        status: AuthStatus,
        message: str,
        affected_accounts: Tuple[int, ...] = (),
    ) -> None:
        pass


class IAuthService(IUserRegistrar, IAuthenticator, IAuthAuditReader, ABC):
    pass


class ISessionAwareAuthService(IAuthService, ISessionAwareAuthenticator, ABC):
    pass


class BoundedAuthEventLogger(IAuthEventJournal):
    def __init__(self, max_events: int = _DEFAULT_MAX_AUTH_EVENTS) -> None:
        if max_events < 1:
            raise ValueError("max_events must be >= 1")
        self._events: Deque[AuthEvent] = deque(maxlen=max_events)
        self._lock = threading.Lock()

    def record(self, event: AuthEvent) -> None:
        if not isinstance(event, AuthEvent):
            raise TypeError("event must be an AuthEvent")
        with self._lock:
            self._events.append(event)

    def get_auth_events(self) -> List[AuthEvent]:
        with self._lock:
            return list(self._events)


class ISessionManager(ABC):
    @abstractmethod
    def start_session(self, username: str) -> str:
        pass

    @abstractmethod
    def end_session(self, session_id: str) -> None:
        pass

    @abstractmethod
    def is_active(self, session_id: str) -> bool:
        pass

    @abstractmethod
    def touch(self, session_id: str) -> None:
        pass

    @abstractmethod
    def active_sessions_for_user(self, username: str) -> Tuple[str, ...]:
        pass

    @abstractmethod
    def session_owner(self, session_id: str) -> Optional[str]:
        pass


class SessionManager(ISessionManager):
    def __init__(self, session_timeout_seconds: float, clock: Optional[IClock] = None) -> None:
        if session_timeout_seconds <= 0:
            raise ValueError("session_timeout_seconds must be > 0")
        self._session_timeout = float(session_timeout_seconds)
        self._clock = clock or SystemClock()
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")
        self._sessions: Dict[str, SessionInfo] = {}
        self._user_sessions: Dict[str, set[str]] = {}
        self._lock = threading.RLock()

    def _is_expired(self, session: SessionInfo, now: float) -> bool:
        return (now - session.last_activity_at) > self._session_timeout

    def _remove_session_unlocked(self, session_id: str) -> None:
        session = self._sessions.pop(session_id, None)
        if session is None:
            return
        user_sessions = self._user_sessions.get(session.username)
        if user_sessions is not None:
            user_sessions.discard(session_id)
            if not user_sessions:
                self._user_sessions.pop(session.username, None)

    def start_session(self, username: str) -> str:
        normalized = _normalize_username(username)
        now = self._clock.monotonic()
        session_id = str(uuid.uuid4())
        session = SessionInfo(
            session_id=session_id,
            username=normalized,
            created_at=now,
            last_activity_at=now,
        )
        with self._lock:
            self._sessions[session_id] = session
            self._user_sessions.setdefault(normalized, set()).add(session_id)
        return session_id

    def end_session(self, session_id: str) -> None:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be a string")
        with self._lock:
            self._remove_session_unlocked(session_id)

    def is_active(self, session_id: str) -> bool:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be a string")
        now = self._clock.monotonic()
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return False
            if self._is_expired(session, now):
                self._remove_session_unlocked(session_id)
                return False
            return True

    def touch(self, session_id: str) -> None:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be a string")
        now = self._clock.monotonic()
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None or self._is_expired(session, now):
                self._remove_session_unlocked(session_id)
                return
            self._sessions[session_id] = SessionInfo(
                session_id=session.session_id,
                username=session.username,
                created_at=session.created_at,
                last_activity_at=now,
            )

    def active_sessions_for_user(self, username: str) -> Tuple[str, ...]:
        normalized = _normalize_username(username)
        now = self._clock.monotonic()
        with self._lock:
            session_ids = list(self._user_sessions.get(normalized, set()))
            active: List[str] = []
            for session_id in session_ids:
                session = self._sessions.get(session_id)
                if session is None or self._is_expired(session, now):
                    self._remove_session_unlocked(session_id)
                    continue
                active.append(session_id)
            return tuple(sorted(active))

    def session_owner(self, session_id: str) -> Optional[str]:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be a string")
        now = self._clock.monotonic()
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            if self._is_expired(session, now):
                self._remove_session_unlocked(session_id)
                return None
            return session.username
        

class ICredentialService(ABC):
    @abstractmethod
    def create_user(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def verify(self, user: User, password: str) -> bool:
        pass


class CredentialService(ICredentialService):
    def __init__(
        self,
        hasher: IPasswordHasher,
        password_policy: IPasswordPolicy,
    ) -> None:
        if not isinstance(hasher, IPasswordHasher):
            raise TypeError("hasher must implement IPasswordHasher")
        if not isinstance(password_policy, IPasswordPolicy):
            raise TypeError("password_policy must implement IPasswordPolicy")

        self._hasher = hasher
        self._password_policy = password_policy

    def create_user(self, username: str, password: str) -> User:
        return User.create(
            username=username,
            password=password,
            hasher=self._hasher,
            password_policy=self._password_policy,
        )

    def verify(self, user: User, password: str) -> bool:
        if not isinstance(user, User):
            raise TypeError("user must be a User")
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        return user.verify_password(password, self._hasher)


class IAuthSessionCoordinator(ABC):
    @abstractmethod
    def login_user(self, username: str) -> str:
        pass

    @abstractmethod
    def logout_user(self, username: str) -> None:
        pass

    @abstractmethod
    def logout_session(self, session_id: str) -> None:
        pass

    @abstractmethod
    def has_active_session(self, username: str) -> bool:
        pass

    @abstractmethod
    def is_session_active(self, session_id: str) -> bool:
        pass

    @abstractmethod
    def touch_user(self, username: str) -> None:
        pass

    @abstractmethod
    def touch_session(self, session_id: str) -> None:
        pass

    @abstractmethod
    def session_owner(self, session_id: str) -> Optional[str]:
        pass


class AuthSessionCoordinator(IAuthSessionCoordinator):
    def __init__(self, session_manager: ISessionManager) -> None:
        if not isinstance(session_manager, ISessionManager):
            raise TypeError("session_manager must implement ISessionManager")
        self._session_manager = session_manager

    def login_user(self, username: str) -> str:
        return self._session_manager.start_session(_normalize_username(username))

    def logout_user(self, username: str) -> None:
        normalized = _normalize_username(username)
        for session_id in self._session_manager.active_sessions_for_user(normalized):
            self._session_manager.end_session(session_id)

    def logout_session(self, session_id: str) -> None:
        self._session_manager.end_session(session_id)

    def has_active_session(self, username: str) -> bool:
        normalized = _normalize_username(username)
        return len(self._session_manager.active_sessions_for_user(normalized)) > 0

    def is_session_active(self, session_id: str) -> bool:
        return self._session_manager.is_active(session_id)

    def touch_user(self, username: str) -> None:
        normalized = _normalize_username(username)
        for session_id in self._session_manager.active_sessions_for_user(normalized):
            self._session_manager.touch(session_id)

    def touch_session(self, session_id: str) -> None:
        self._session_manager.touch(session_id)

    def session_owner(self, session_id: str) -> Optional[str]:
        return self._session_manager.session_owner(session_id)


class IAuthorizedAccountReader(ABC):
    @abstractmethod
    def account_numbers_for_user(self, username: str) -> Tuple[int, ...]:
        pass


class AuthEventRecorder(IAuthEventRecorder):
    def __init__(self, event_logger: IAuthEventLogger, clock: IClock) -> None:
        if not isinstance(event_logger, IAuthEventLogger):
            raise TypeError("event_logger must implement IAuthEventLogger")
        if not isinstance(clock, IClock):
            raise TypeError("clock must implement IClock")
        self._event_logger = event_logger
        self._clock = clock

    def record(
        self,
        username: str,
        action: AuthAction,
        status: AuthStatus,
        message: str,
        affected_accounts: Tuple[int, ...] = (),
    ) -> None:
        self._event_logger.record(
            AuthEvent(
                timestamp=self._clock.now(),
                username=_normalize_username(username),
                action=action,
                status=status,
                message=message,
                affected_accounts=affected_accounts,
            )
        )


class ILoginAttemptPolicy(ABC):
    @property
    @abstractmethod
    def max_attempts(self) -> int:
        pass

    @abstractmethod
    def record_failure(self, username: str) -> LockoutResult:
        pass

    @abstractmethod
    def reset(self, username: str) -> None:
        pass

    @abstractmethod
    def is_locked(self, username: str) -> bool:
        pass

    @abstractmethod
    def failed_attempts(self, username: str) -> int:
        pass

    @abstractmethod
    def remaining_lock_seconds(self, username: str) -> float:
        pass


class LoginAttemptPolicy(ILoginAttemptPolicy):
    def __init__(
        self,
        max_attempts: int,
        lockout_seconds: float,
        clock: Optional[IClock] = None,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if lockout_seconds <= 0:
            raise ValueError("lockout_seconds must be > 0")
        self._max_attempts = int(max_attempts)
        self._lockout_seconds = float(lockout_seconds)
        self._attempts: Dict[str, int] = {}
        self._locked_until: Dict[str, float] = {}
        self._clock = clock or SystemClock()
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")
        self._lock = threading.RLock()

    @property
    def max_attempts(self) -> int:
        return self._max_attempts

    def _clear_if_expired(self, username: str) -> None:
        locked_until = self._locked_until.get(username)
        if locked_until is not None and self._clock.monotonic() >= locked_until:
            self._locked_until.pop(username, None)
            self._attempts.pop(username, None)

    def record_failure(self, username: str) -> LockoutResult:
        normalized = _normalize_username(username)
        with self._lock:
            self._clear_if_expired(normalized)
            attempts = self._attempts.get(normalized, 0) + 1
            self._attempts[normalized] = attempts

            now_locked = attempts >= self._max_attempts
            remaining = 0.0

            if now_locked:
                self._locked_until[normalized] = (
                    self._clock.monotonic() + self._lockout_seconds
                )
                remaining = self._lockout_seconds

            return LockoutResult(
                attempts=attempts,
                now_locked=now_locked,
                remaining_seconds=remaining,
            )

    def reset(self, username: str) -> None:
        normalized = _normalize_username(username)
        with self._lock:
            self._attempts.pop(normalized, None)
            self._locked_until.pop(normalized, None)

    def is_locked(self, username: str) -> bool:
        normalized = _normalize_username(username)
        with self._lock:
            self._clear_if_expired(normalized)
            locked_until = self._locked_until.get(normalized)
            return locked_until is not None and self._clock.monotonic() < locked_until

    def failed_attempts(self, username: str) -> int:
        normalized = _normalize_username(username)
        with self._lock:
            self._clear_if_expired(normalized)
            return self._attempts.get(normalized, 0)

    def remaining_lock_seconds(self, username: str) -> float:
        normalized = _normalize_username(username)
        with self._lock:
            self._clear_if_expired(normalized)
            locked_until = self._locked_until.get(normalized)
            if locked_until is None:
                return 0.0
            return max(0.0, locked_until - self._clock.monotonic())




class IAuthRegistrationService(ABC):
    @abstractmethod
    def register_user(self, username: str, password: str) -> User:
        pass


class IAuthLoginService(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def authenticate_session(self, username: str, password: str) -> AuthSession:
        pass

class ILoginEligibilityService(ABC):
    @abstractmethod
    def prepare_login(self, username: str) -> User:
        pass

    @abstractmethod
    def ensure_not_locked(self, username: str) -> None:
        pass

class ILoginOutcomeService(ABC):
    @abstractmethod
    def handle_success(self, user: User) -> AuthSession:
        pass

    @abstractmethod
    def handle_failure(self, username: str) -> NoReturn:
        pass

class IAuthSessionService(ABC):
    @abstractmethod
    def logout(self, username: str) -> None:
        pass

    @abstractmethod
    def logout_session(self, session_id: str) -> None:
        pass

    @abstractmethod
    def is_authenticated_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def is_authenticated_session(self, auth_session: AuthSession) -> bool:
        pass

    @abstractmethod
    def touch_user(self, username: str) -> None:
        pass

    @abstractmethod
    def touch_session(self, session_id: str) -> None:
        pass

    @abstractmethod
    def is_locked(self, username: str) -> bool:
        pass

    @abstractmethod
    def failed_attempts(self, username: str) -> int:
        pass


class AuthRegistrationService(IAuthRegistrationService):
    def __init__(
        self,
        user_store: IUserStore,
        credential_service: ICredentialService,
    ) -> None:
        if not isinstance(user_store, IUserStore):
            raise TypeError("user_store must implement IUserStore")
        if not isinstance(credential_service, ICredentialService):
            raise TypeError("credential_service must implement ICredentialService")

        self._users = user_store
        self._credential_service = credential_service

    def register_user(self, username: str, password: str) -> User:
        user = self._credential_service.create_user(username, password)
        self._users.add(user)
        return user


class AuthLoginService(IAuthLoginService):
    def __init__(
        self,
        eligibility_service: ILoginEligibilityService,
        credential_service: ICredentialService,
        outcome_service: ILoginOutcomeService,
    ) -> None:
        if not isinstance(eligibility_service, ILoginEligibilityService):
            raise TypeError("eligibility_service must implement ILoginEligibilityService")
        if not isinstance(credential_service, ICredentialService):
            raise TypeError("credential_service must implement ICredentialService")
        if not isinstance(outcome_service, ILoginOutcomeService):
            raise TypeError("outcome_service must implement ILoginOutcomeService")

        self._eligibility_service = eligibility_service
        self._credential_service = credential_service
        self._outcome_service = outcome_service

    def authenticate(self, username: str, password: str) -> User:
        return self.authenticate_session(username, password).user

    def authenticate_session(self, username: str, password: str) -> AuthSession:
        normalized_username = _normalize_username(username)
        if not isinstance(password, str):
            raise TypeError("password must be a string")

        user = self._eligibility_service.prepare_login(normalized_username)
        is_valid = self._credential_service.verify(user, password)

        self._eligibility_service.ensure_not_locked(normalized_username)

        if is_valid:
            return self._outcome_service.handle_success(user)

        self._outcome_service.handle_failure(normalized_username)


class LoginEligibilityService(ILoginEligibilityService):
    def __init__(
        self,
        user_store: IUserStore,
        login_attempt_policy: ILoginAttemptPolicy,
        auth_event_recorder: IAuthEventRecorder,
    ) -> None:
        if not isinstance(user_store, IUserStore):
            raise TypeError("user_store must implement IUserStore")
        if not isinstance(login_attempt_policy, ILoginAttemptPolicy):
            raise TypeError("login_attempt_policy must implement ILoginAttemptPolicy")
        if not isinstance(auth_event_recorder, IAuthEventRecorder):
            raise TypeError("auth_event_recorder must implement IAuthEventRecorder")

        self._users = user_store
        self._login_attempt_policy = login_attempt_policy
        self._auth_events = auth_event_recorder

    def prepare_login(self, username: str) -> User:
        normalized_username = _normalize_username(username)
        user = self._users.get(normalized_username)
        if user is None:
            self._auth_events.record(
                username=normalized_username,
                action=AuthAction.LOGIN,
                status=AuthStatus.FAILED,
                message="Invalid credentials",
            )
            raise AuthenticationError("Invalid credentials")

        self.ensure_not_locked(normalized_username)
        return user

    def ensure_not_locked(self, username: str) -> None:
        normalized_username = _normalize_username(username)
        if self._login_attempt_policy.is_locked(normalized_username):
            remaining = round(
                self._login_attempt_policy.remaining_lock_seconds(normalized_username),
                1,
            )
            self._auth_events.record(
                username=normalized_username,
                action=AuthAction.BLOCKED_LOGIN,
                status=AuthStatus.BLOCKED,
                message="Login attempt rejected because account is locked",
            )
            raise AccountLockedError(
                f"Account for '{normalized_username}' is locked for "
                f"{remaining} more second(s)"
            )


class LoginOutcomeService(ILoginOutcomeService):
    def __init__(
        self,
        login_attempt_policy: ILoginAttemptPolicy,
        session_coordinator: IAuthSessionCoordinator,
        auth_event_recorder: IAuthEventRecorder,
        authorized_account_reader: Optional[IAuthorizedAccountReader] = None,
    ) -> None:
        if not isinstance(login_attempt_policy, ILoginAttemptPolicy):
            raise TypeError("login_attempt_policy must implement ILoginAttemptPolicy")
        if not isinstance(session_coordinator, IAuthSessionCoordinator):
            raise TypeError("session_coordinator must implement IAuthSessionCoordinator")
        if not isinstance(auth_event_recorder, IAuthEventRecorder):
            raise TypeError("auth_event_recorder must implement IAuthEventRecorder")
        if authorized_account_reader is not None and not isinstance(
            authorized_account_reader,
            IAuthorizedAccountReader,
        ):
            raise TypeError(
                "authorized_account_reader must implement IAuthorizedAccountReader"
            )

        self._login_attempt_policy = login_attempt_policy
        self._session_coordinator = session_coordinator
        self._auth_events = auth_event_recorder
        self._authorized_account_reader = authorized_account_reader

    def handle_success(self, user: User) -> AuthSession:
        if not isinstance(user, User):
            raise TypeError("user must be a User")

        self._login_attempt_policy.reset(user.username)
        session_id = self._session_coordinator.login_user(user.username)
        self._auth_events.record(
            username=user.username,
            action=AuthAction.LOGIN,
            status=AuthStatus.PASS,
            message="Authentication successful",
        )
        return AuthSession(session_id=session_id, user=user)

    def handle_failure(self, username: str) -> NoReturn:
        normalized_username = _normalize_username(username)
        result = self._login_attempt_policy.record_failure(normalized_username)

        if result.now_locked:
            self._session_coordinator.logout_user(normalized_username)
            affected_accounts: Tuple[int, ...] = ()
            if self._authorized_account_reader is not None:
                affected_accounts = self._authorized_account_reader.account_numbers_for_user(
                    normalized_username
                )

            if result.attempts == self._login_attempt_policy.max_attempts:
                self._auth_events.record(
                    username=normalized_username,
                    action=AuthAction.LOCKOUT,
                    status=AuthStatus.LOCKED,
                    message=(
                        f"Account locked after "
                        f"{self._login_attempt_policy.max_attempts} failed attempt(s)"
                    ),
                    affected_accounts=affected_accounts,
                )

            raise AccountLockedError(
                f"Account for '{normalized_username}' locked after "
                f"{self._login_attempt_policy.max_attempts} failed attempt(s)"
            )

        self._auth_events.record(
            username=normalized_username,
            action=AuthAction.LOGIN,
            status=AuthStatus.FAILED,
            message=(
                f"Invalid credentials. Attempt "
                f"{result.attempts}/{self._login_attempt_policy.max_attempts}"
            ),
        )
        raise AuthenticationError("Invalid credentials")

class AuthSessionService(IAuthSessionService):
    def __init__(
        self,
        user_store: IUserStore,
        session_coordinator: IAuthSessionCoordinator,
        login_attempt_policy: ILoginAttemptPolicy,
        auth_event_recorder: IAuthEventRecorder,
    ) -> None:
        if not isinstance(user_store, IUserStore):
            raise TypeError("user_store must implement IUserStore")
        if not isinstance(session_coordinator, IAuthSessionCoordinator):
            raise TypeError("session_coordinator must implement IAuthSessionCoordinator")
        if not isinstance(login_attempt_policy, ILoginAttemptPolicy):
            raise TypeError("login_attempt_policy must implement ILoginAttemptPolicy")
        if not isinstance(auth_event_recorder, IAuthEventRecorder):
            raise TypeError("auth_event_recorder must implement IAuthEventRecorder")

        self._users = user_store
        self._session_coordinator = session_coordinator
        self._login_attempt_policy = login_attempt_policy
        self._auth_events = auth_event_recorder

    def logout(self, username: str) -> None:
        normalized = _normalize_username(username)
        if not self._users.contains(normalized):
            return
        self._session_coordinator.logout_user(normalized)
        self._auth_events.record(
            username=normalized,
            action=AuthAction.LOGOUT,
            status=AuthStatus.PASS,
            message="Session terminated",
        )

    def logout_session(self, session_id: str) -> None:
        if not isinstance(session_id, str) or not session_id:
            raise TypeError("session_id must be a non-empty string")
        owner = self._session_coordinator.session_owner(session_id)
        self._session_coordinator.logout_session(session_id)
        if owner is not None and self._users.contains(owner):
            self._auth_events.record(
                username=owner,
                action=AuthAction.LOGOUT,
                status=AuthStatus.PASS,
                message="Session terminated",
            )

    def is_authenticated_user(self, user: User) -> bool:
        if not isinstance(user, User):
            return False
        stored_user = self._users.get(user.username)
        if stored_user != user:
            return False
        return self._session_coordinator.has_active_session(user.username)

    def is_authenticated_session(self, auth_session: AuthSession) -> bool:
        if not isinstance(auth_session, AuthSession):
            return False
        stored_user = self._users.get(auth_session.user.username)
        if stored_user != auth_session.user:
            return False
        owner = self._session_coordinator.session_owner(auth_session.session_id)
        if owner != auth_session.user.username:
            return False
        return self._session_coordinator.is_session_active(auth_session.session_id)

    def touch_user(self, username: str) -> None:
        self._session_coordinator.touch_user(username)

    def touch_session(self, session_id: str) -> None:
        if not isinstance(session_id, str) or not session_id:
            raise TypeError("session_id must be a non-empty string")
        self._session_coordinator.touch_session(session_id)

    def is_locked(self, username: str) -> bool:
        return self._login_attempt_policy.is_locked(_normalize_username(username))

    def failed_attempts(self, username: str) -> int:
        return self._login_attempt_policy.failed_attempts(_normalize_username(username))


class AuthService(ISessionAwareAuthService):
    def __init__(
        self,
        registration_service: IAuthRegistrationService,
        login_service: IAuthLoginService,
        session_service: IAuthSessionService,
        auth_event_journal: IAuthEventJournal,
    ) -> None:
        if not isinstance(registration_service, IAuthRegistrationService):
            raise TypeError("registration_service must implement IAuthRegistrationService")
        if not isinstance(login_service, IAuthLoginService):
            raise TypeError("login_service must implement IAuthLoginService")
        if not isinstance(session_service, IAuthSessionService):
            raise TypeError("session_service must implement IAuthSessionService")
        if not isinstance(auth_event_journal, IAuthEventJournal):
            raise TypeError("auth_event_journal must implement IAuthEventJournal")

        self._registration_service = registration_service
        self._login_service = login_service
        self._session_service = session_service
        self._auth_event_journal = auth_event_journal

    def register_user(self, username: str, password: str) -> User:
        return self._registration_service.register_user(username, password)

    def authenticate(self, username: str, password: str) -> User:
        return self._login_service.authenticate(username, password)

    def authenticate_session(self, username: str, password: str) -> AuthSession:
        return self._login_service.authenticate_session(username, password)

    def logout(self, username: str) -> None:
        self._session_service.logout(username)

    def logout_session(self, session_id: str) -> None:
        self._session_service.logout_session(session_id)

    def get_auth_events(self) -> List[AuthEvent]:
        return self._auth_event_journal.get_auth_events()

    def is_authenticated_user(self, user: User) -> bool:
        return self._session_service.is_authenticated_user(user)

    def is_authenticated_session(self, auth_session: AuthSession) -> bool:
        return self._session_service.is_authenticated_session(auth_session)

    def touch_user(self, username: str) -> None:
        self._session_service.touch_user(username)

    def touch_session(self, session_id: str) -> None:
        self._session_service.touch_session(session_id)

    def is_locked(self, username: str) -> bool:
        return self._session_service.is_locked(username)

    def failed_attempts(self, username: str) -> int:
        return self._session_service.failed_attempts(username)


class AuthServiceFactory:
    @staticmethod
    def from_legacy_dependencies(
        user_store: IUserStore,
        login_attempt_policy: ILoginAttemptPolicy,
        credential_service: ICredentialService,
        session_coordinator: IAuthSessionCoordinator,
        auth_event_journal: IAuthEventJournal,
        clock: IClock,
        authorized_account_reader: Optional[IAuthorizedAccountReader] = None,
    ) -> AuthService:
        if not isinstance(user_store, IUserStore):
            raise TypeError("user_store must implement IUserStore")
        if not isinstance(login_attempt_policy, ILoginAttemptPolicy):
            raise TypeError("login_attempt_policy must implement ILoginAttemptPolicy")
        if not isinstance(credential_service, ICredentialService):
            raise TypeError("credential_service must implement ICredentialService")
        if not isinstance(clock, IClock):
            raise TypeError("clock must implement IClock")
        if not isinstance(session_coordinator, IAuthSessionCoordinator):
            raise TypeError("session_coordinator must implement IAuthSessionCoordinator")
        if not isinstance(auth_event_journal, IAuthEventJournal):
            raise TypeError("auth_event_journal must implement IAuthEventJournal")
        if authorized_account_reader is not None and not isinstance(
            authorized_account_reader,
            IAuthorizedAccountReader,
        ):
            raise TypeError(
                "authorized_account_reader must implement IAuthorizedAccountReader"
            )

        auth_event_recorder = AuthEventRecorder(
            event_logger=auth_event_journal,
            clock=clock,
        )

        registration_service = AuthRegistrationService(
            user_store=user_store,
            credential_service=credential_service,
        )
        eligibility_service = LoginEligibilityService(
            user_store=user_store,
            login_attempt_policy=login_attempt_policy,
            auth_event_recorder=auth_event_recorder,
        )
        outcome_service = LoginOutcomeService(
            login_attempt_policy=login_attempt_policy,
            session_coordinator=session_coordinator,
            auth_event_recorder=auth_event_recorder,
            authorized_account_reader=authorized_account_reader,
        )
        login_service = AuthLoginService(
            eligibility_service=eligibility_service,
            credential_service=credential_service,
            outcome_service=outcome_service,
        )
        session_service = AuthSessionService(
            user_store=user_store,
            session_coordinator=session_coordinator,
            login_attempt_policy=login_attempt_policy,
            auth_event_recorder=auth_event_recorder,
        )
        return AuthService(
            registration_service=registration_service,
            login_service=login_service,
            session_service=session_service,
            auth_event_journal=auth_event_journal,
        )
    

# =============================================================================
# SECTION 4 — AUTHORIZATION
# =============================================================================


@dataclass(frozen=True, slots=True)
class Permission:
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Permission name must be a non-empty string")
        object.__setattr__(self, "name", self.name.strip().casefold())


@dataclass(frozen=True, slots=True)
class RoleId:
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("RoleId name must be a non-empty string")
        object.__setattr__(self, "name", self.name.strip().casefold())


ROLE_OWNER = RoleId("owner")
ROLE_AUDITOR = RoleId("auditor")
ROLE_ADMIN = RoleId("admin")

PERM_VIEW_BALANCE = Permission("view_balance")
PERM_DEPOSIT = Permission("deposit")
PERM_WITHDRAW = Permission("withdraw")
PERM_TRANSFER = Permission("transfer")
PERM_VIEW_LOGS = Permission("view_logs")


_PERMISSION_TABLE: Mapping[RoleId, frozenset[Permission]] = MappingProxyType(
    {
        ROLE_OWNER: frozenset(
            {
                PERM_VIEW_BALANCE,
                PERM_DEPOSIT,
                PERM_WITHDRAW,
                PERM_TRANSFER,
                PERM_VIEW_LOGS,
            }
        ),
        ROLE_AUDITOR: frozenset(
            {
                PERM_VIEW_BALANCE,
                PERM_VIEW_LOGS,
            }
        ),
        ROLE_ADMIN: frozenset(
            {
                PERM_VIEW_BALANCE,
                PERM_DEPOSIT,
                PERM_WITHDRAW,
                PERM_TRANSFER,
                PERM_VIEW_LOGS,
            }
        ),
    }
)

_OUTGOING_PERMISSIONS: frozenset[Permission] = frozenset(
    {PERM_WITHDRAW, PERM_TRANSFER}
)


class IAccessRepository(ABC):
    @abstractmethod
    def grant_access(self, username: str, account_number: int, role: RoleId) -> None:
        pass

    @abstractmethod
    def revoke_access(self, username: str, account_number: int) -> None:
        pass

    @abstractmethod
    def get_role(self, username: str, account_number: int) -> Optional[RoleId]:
        pass

    @abstractmethod
    def account_numbers_for_user(self, username: str) -> Tuple[int, ...]:
        pass


class InMemoryAccessRepository(IAccessRepository):
    def __init__(self) -> None:
        self._roles: Dict[str, Dict[int, RoleId]] = {}
        self._lock = threading.RLock()

    def grant_access(self, username: str, account_number: int, role: RoleId) -> None:
        normalized = _normalize_username(username)
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        if not isinstance(role, RoleId):
            raise TypeError("role must be a RoleId")
        with self._lock:
            self._roles.setdefault(normalized, {})[account_number] = role

    def revoke_access(self, username: str, account_number: int) -> None:
        normalized = _normalize_username(username)
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        with self._lock:
            if normalized in self._roles:
                self._roles[normalized].pop(account_number, None)
                if not self._roles[normalized]:
                    self._roles.pop(normalized, None)

    def get_role(self, username: str, account_number: int) -> Optional[RoleId]:
        normalized = _normalize_username(username)
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        with self._lock:
            return self._roles.get(normalized, {}).get(account_number)

    def account_numbers_for_user(self, username: str) -> Tuple[int, ...]:
        normalized = _normalize_username(username)
        with self._lock:
            return tuple(sorted(self._roles.get(normalized, {}).keys()))


class IRolePermissionProvider(ABC):
    @abstractmethod
    def allowed_permissions(self, role: RoleId) -> frozenset[Permission]:
        pass


class TableRolePermissionProvider(IRolePermissionProvider):
    def __init__(
        self,
        permission_table: Optional[Mapping[RoleId, frozenset[Permission]]] = None,
    ) -> None:
        table = _PERMISSION_TABLE if permission_table is None else permission_table

        validated_table: Dict[RoleId, frozenset[Permission]] = {}
        for role, actions in table.items():
            if not isinstance(role, RoleId):
                raise TypeError("permission_table keys must be RoleId values")
            normalized_actions = frozenset(actions)
            for action in normalized_actions:
                if not isinstance(action, Permission):
                    raise TypeError(
                        "permission_table values must contain Permission objects"
                    )
            validated_table[role] = normalized_actions

        self._permission_table = MappingProxyType(validated_table)

    def allowed_permissions(self, role: RoleId) -> frozenset[Permission]:
        if not isinstance(role, RoleId):
            raise TypeError("role must be a RoleId")
        return self._permission_table.get(role, frozenset())


class IPermissionPolicy(ABC):
    @abstractmethod
    def is_allowed(self, role: RoleId, permission: Permission) -> bool:
        pass


class PermissionPolicy(IPermissionPolicy):
    def __init__(
        self,
        provider: Optional[IRolePermissionProvider] = None,
    ) -> None:
        resolved_provider = TableRolePermissionProvider() if provider is None else provider
        if not isinstance(resolved_provider, IRolePermissionProvider):
            raise TypeError("provider must implement IRolePermissionProvider")
        self._provider = resolved_provider

    def is_allowed(self, role: RoleId, permission: Permission) -> bool:
        if not isinstance(role, RoleId):
            raise TypeError("role must be a RoleId")
        if not isinstance(permission, Permission):
            raise TypeError("permission must be a Permission")
        return permission in self._provider.allowed_permissions(role)


class IAuthorizationPolicy(IAuthorizedAccountReader, ABC):
    @abstractmethod
    def grant_access(self, username: str, account_number: int, role: RoleId) -> None:
        pass

    @abstractmethod
    def revoke_access(self, username: str, account_number: int) -> None:
        pass

    @abstractmethod
    def get_role(self, username: str, account_number: int) -> Optional[RoleId]:
        pass

    @abstractmethod
    def check_permission(self, user: User, permission: Permission, account_number: int) -> bool:
        pass


class AuthorizationPolicy(IAuthorizationPolicy):
    def __init__(
        self,
        access_repository: Optional[IAccessRepository] = None,
        permission_policy: Optional[IPermissionPolicy] = None,
    ) -> None:
        self._repository = access_repository or InMemoryAccessRepository()
        self._permission_policy = permission_policy or PermissionPolicy()

        if not isinstance(self._repository, IAccessRepository):
            raise TypeError("access_repository must implement IAccessRepository")
        if not isinstance(self._permission_policy, IPermissionPolicy):
            raise TypeError("permission_policy must implement IPermissionPolicy")

    def grant_access(self, username: str, account_number: int, role: RoleId) -> None:
        self._repository.grant_access(username, account_number, role)

    def revoke_access(self, username: str, account_number: int) -> None:
        self._repository.revoke_access(username, account_number)

    def get_role(self, username: str, account_number: int) -> Optional[RoleId]:
        return self._repository.get_role(username, account_number)

    def account_numbers_for_user(self, username: str) -> Tuple[int, ...]:
        return self._repository.account_numbers_for_user(username)

    def check_permission(self, user: User, permission: Permission, account_number: int) -> bool:
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")
        if not isinstance(permission, Permission):
            raise TypeError("permission must be a Permission")
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")

        role = self.get_role(user.username, account_number)
        if role is None:
            raise AuthorizationError(
                f"User '{user.username}' has no access to account {account_number}"
            )
        if not self._permission_policy.is_allowed(role, permission):
            raise AuthorizationError(
                f"User '{user.username}' (role '{role.name}') may not perform "
                f"'{permission.name}' on account {account_number}"
            )
        return True


# =============================================================================
# SECTION 5 — SECURITY EVENTS, AUDIT LOGGING, ALERTING
# =============================================================================


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class EventStatus(Enum):
    PASS = "PASS"
    FAILED = "FAILED"
    DENIED = "DENIED"
    BLOCKED = "BLOCKED"
    FLAGGED = "FLAGGED"
    LOCKED = "LOCKED"


class SecurityAction(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    FRAUD_DETECTED = "fraud_detected"
    ACCESS_DENIED = "access_denied"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    GET_BALANCE = "get_balance"
    AUTH_LOGIN = "auth_login"
    AUTH_LOGOUT = "auth_logout"
    AUTH_LOCKOUT = "auth_lockout"
    AUTH_BLOCKED_LOGIN = "auth_blocked_login"


_AUTH_ACTION_TO_SECURITY_ACTION: Mapping[AuthAction, SecurityAction] = MappingProxyType(
    {
        AuthAction.LOGIN: SecurityAction.AUTH_LOGIN,
        AuthAction.LOGOUT: SecurityAction.AUTH_LOGOUT,
        AuthAction.LOCKOUT: SecurityAction.AUTH_LOCKOUT,
        AuthAction.BLOCKED_LOGIN: SecurityAction.AUTH_BLOCKED_LOGIN,
    }
)

_AUTH_STATUS_TO_EVENT_STATUS: Mapping[AuthStatus, EventStatus] = MappingProxyType(
    {
        AuthStatus.PASS: EventStatus.PASS,
        AuthStatus.FAILED: EventStatus.FAILED,
        AuthStatus.LOCKED: EventStatus.LOCKED,
        AuthStatus.BLOCKED: EventStatus.BLOCKED,
    }
)

_AUTH_STATUS_TO_SEVERITY: Mapping[AuthStatus, Severity] = MappingProxyType(
    {
        AuthStatus.PASS: Severity.INFO,
        AuthStatus.FAILED: Severity.WARNING,
        AuthStatus.BLOCKED: Severity.WARNING,
        AuthStatus.LOCKED: Severity.CRITICAL,
    }
)


class EventAmountKind(Enum):
    NONE = "none"
    TRANSACTION = "transaction"
    BALANCE = "balance"


@dataclass(frozen=True, slots=True)
class EventAmount:
    kind: EventAmountKind
    value: Optional[float] = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, EventAmountKind):
            raise TypeError("kind must be an EventAmountKind")

        if self.kind == EventAmountKind.NONE:
            if self.value is not None:
                raise ValueError("NONE amount kind must not have a value")

        elif self.kind == EventAmountKind.TRANSACTION:
            if self.value is None:
                raise ValueError("TRANSACTION amount kind requires a value")
            object.__setattr__(self, "value", validate_amount(self.value))

        elif self.kind == EventAmountKind.BALANCE:
            if self.value is None:
                raise ValueError("BALANCE amount kind requires a value")
            numeric = round(float(self.value), 2)
            if numeric < 0:
                raise ValueError("BALANCE amount must be non-negative")
            object.__setattr__(self, "value", numeric)

    @classmethod
    def none(cls) -> "EventAmount":
        return cls(EventAmountKind.NONE)

    @classmethod
    def transaction(cls, value: float) -> "EventAmount":
        return cls(EventAmountKind.TRANSACTION, value)

    @classmethod
    def balance(cls, value: float) -> "EventAmount":
        return cls(EventAmountKind.BALANCE, value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind.value,
            "value": self.value,
        }

    def __str__(self) -> str:
        if self.kind == EventAmountKind.NONE:
            return "none"
        assert self.value is not None
        return f"{self.kind.value}:{self.value:.2f}"


def _safe_transaction_event_amount(value: Any) -> EventAmount:
    try:
        return EventAmount.transaction(value)
    except Exception:
        return EventAmount.none()


@dataclass(frozen=True, slots=True)
class SecurityEvent:
    timestamp: datetime
    username: str
    account_number: Optional[int]
    action: SecurityAction
    amount: EventAmount
    status: EventStatus
    message: str = ""
    severity: Severity = Severity.INFO

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", _normalize_datetime(self.timestamp, "timestamp"))
        object.__setattr__(self, "username", _normalize_username(self.username))
        if self.account_number is not None and not isinstance(self.account_number, int):
            raise TypeError("account_number must be an int or None")
        if not isinstance(self.action, SecurityAction):
            raise TypeError("action must be a SecurityAction")
        if not isinstance(self.amount, EventAmount):
            raise TypeError("amount must be an EventAmount")
        if not isinstance(self.status, EventStatus):
            raise TypeError("status must be an EventStatus")
        if not isinstance(self.message, str):
            raise TypeError("message must be a string")
        if not isinstance(self.severity, Severity):
            raise TypeError("severity must be a Severity")

    @classmethod
    def create(
        cls,
        clock: IClock,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        amount: EventAmount,
        status: EventStatus,
        message: str = "",
        severity: Severity = Severity.INFO,
    ) -> "SecurityEvent":
        if not isinstance(clock, IClock):
            raise TypeError("clock must implement IClock")
        return cls(
            timestamp=clock.now(),
            username=username,
            account_number=account_number,
            action=action,
            amount=amount,
            status=status,
            message=message,
            severity=severity,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": _format_datetime(self.timestamp),
            "username": self.username,
            "account_number": self.account_number,
            "action": self.action.value,
            "amount": self.amount.to_dict(),
            "status": self.status.value,
            "message": self.message,
            "severity": self.severity.value,
        }

    def __repr__(self) -> str:
        return (
            f"[{self.severity.value}] {_format_datetime(self.timestamp)} | "
            f"User={self.username} | Account={self.account_number} | "
            f"Action={self.action.value} | Amount={self.amount} | "
            f"Status={self.status.value} | {self.message}"
        )

class ISecurityEventFactory(ABC):
    @abstractmethod
    def transaction_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        amount: float,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        pass

    @abstractmethod
    def safe_transaction_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        amount: Any,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        pass

    @abstractmethod
    def balance_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        balance: float,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        pass

    @abstractmethod
    def no_amount_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        pass

class SecurityEventFactory(ISecurityEventFactory):
    def __init__(self, clock: IClock) -> None:
        if not isinstance(clock, IClock):
            raise TypeError("clock must implement IClock")
        self._clock = clock

    def transaction_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        amount: float,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        return SecurityEvent.create(
            clock=self._clock,
            username=username,
            account_number=account_number,
            action=action,
            amount=EventAmount.transaction(amount),
            status=status,
            message=message,
            severity=severity,
        )

    def safe_transaction_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        amount: Any,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        return SecurityEvent.create(
            clock=self._clock,
            username=username,
            account_number=account_number,
            action=action,
            amount=_safe_transaction_event_amount(amount),
            status=status,
            message=message,
            severity=severity,
        )

    def balance_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        balance: float,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        return SecurityEvent.create(
            clock=self._clock,
            username=username,
            account_number=account_number,
            action=action,
            amount=EventAmount.balance(balance),
            status=status,
            message=message,
            severity=severity,
        )

    def no_amount_event(
        self,
        username: str,
        account_number: Optional[int],
        action: SecurityAction,
        status: EventStatus,
        message: str,
        severity: Severity,
    ) -> SecurityEvent:
        return SecurityEvent.create(
            clock=self._clock,
            username=username,
            account_number=account_number,
            action=action,
            amount=EventAmount.none(),
            status=status,
            message=message,
            severity=severity,
        )


@dataclass(frozen=True, slots=True)
class ObserverNotificationFailure:
    observer_name: str
    event_action: SecurityAction
    message: str
    timestamp: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.observer_name, str) or not self.observer_name:
            raise ValueError("observer_name must be a non-empty string")
        if not isinstance(self.event_action, SecurityAction):
            raise TypeError("event_action must be a SecurityAction")
        if not isinstance(self.message, str):
            raise TypeError("message must be a string")
        object.__setattr__(self, "timestamp", _normalize_datetime(self.timestamp, "timestamp"))


class IObserverFailureReader(ABC):
    @abstractmethod
    def all(self) -> List[ObserverNotificationFailure]:
        pass


class IObserverFailureSink(IObserverFailureReader, ABC):
    @abstractmethod
    def record(self, failure: ObserverNotificationFailure) -> None:
        pass


class InMemoryObserverFailureSink(IObserverFailureSink):
    def __init__(self) -> None:
        self._failures: List[ObserverNotificationFailure] = []
        self._lock = threading.RLock()

    def record(self, failure: ObserverNotificationFailure) -> None:
        if not isinstance(failure, ObserverNotificationFailure):
            raise TypeError("failure must be an ObserverNotificationFailure")
        with self._lock:
            self._failures.append(failure)

    def all(self) -> List[ObserverNotificationFailure]:
        with self._lock:
            return list(self._failures)


class SecurityObserver(ABC):
    @abstractmethod
    def on_critical_event(self, event: SecurityEvent) -> None:
        pass


class IAlertMonitor(SecurityObserver, ABC):
    @abstractmethod
    def get_alerts(self) -> List[SecurityEvent]:
        pass

    @abstractmethod
    def alert_count(self) -> int:
        pass


class AlertObserver(IAlertMonitor):
    def __init__(self, max_alerts: int = _DEFAULT_MAX_ALERTS) -> None:
        if max_alerts < 1:
            raise ValueError("max_alerts must be >= 1")
        self._alerts: Deque[SecurityEvent] = deque(maxlen=max_alerts)
        self._lock = threading.Lock()

    def on_critical_event(self, event: SecurityEvent) -> None:
        if not isinstance(event, SecurityEvent):
            raise TypeError("event must be a SecurityEvent")
        with self._lock:
            self._alerts.append(event)

    def get_alerts(self) -> List[SecurityEvent]:
        with self._lock:
            return list(self._alerts)

    def alert_count(self) -> int:
        with self._lock:
            return len(self._alerts)


class ISecurityEventSource(ABC):
    @abstractmethod
    def get_events(self) -> List[SecurityEvent]:
        pass


class ISecurityEventStore(ABC):
    @abstractmethod
    def add(self, event: SecurityEvent) -> None:
        pass

    @abstractmethod
    def all(self) -> List[SecurityEvent]:
        pass


class BoundedSecurityEventStore(ISecurityEventStore):
    def __init__(self, max_events: int = _DEFAULT_MAX_SECURITY_EVENTS) -> None:
        if max_events < 1:
            raise ValueError("max_events must be >= 1")
        self._events: Deque[SecurityEvent] = deque(maxlen=max_events)
        self._lock = threading.RLock()

    def add(self, event: SecurityEvent) -> None:
        if not isinstance(event, SecurityEvent):
            raise TypeError("event must be a SecurityEvent")
        with self._lock:
            self._events.append(event)

    def all(self) -> List[SecurityEvent]:
        with self._lock:
            return list(self._events)


class ICriticalEventPublisher(ABC):
    @abstractmethod
    def add_observer(self, observer: SecurityObserver) -> None:
        pass

    @abstractmethod
    def publish(self, event: SecurityEvent) -> None:
        pass


class CriticalEventPublisher(ICriticalEventPublisher):
    def __init__(
        self,
        failure_sink: Optional[IObserverFailureSink] = None,
        clock: Optional[IClock] = None,
    ) -> None:
        self._observers: List[SecurityObserver] = []
        self._lock = threading.RLock()
        resolved_failure_sink = InMemoryObserverFailureSink() if failure_sink is None else failure_sink
        resolved_clock = SystemClock() if clock is None else clock

        self._failure_sink = resolved_failure_sink
        self._clock = resolved_clock

        if not isinstance(self._failure_sink, IObserverFailureSink):
            raise TypeError("failure_sink must implement IObserverFailureSink")
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")

    def add_observer(self, observer: SecurityObserver) -> None:
        if not isinstance(observer, SecurityObserver):
            raise TypeError("observer must be a SecurityObserver")
        with self._lock:
            self._observers.append(observer)

    def publish(self, event: SecurityEvent) -> None:
        if not isinstance(event, SecurityEvent):
            raise TypeError("event must be a SecurityEvent")
        with self._lock:
            observers = list(self._observers)

        for observer in observers:
            try:
                observer.on_critical_event(event)
            except Exception as exc:
                self._failure_sink.record(
                    ObserverNotificationFailure(
                        observer_name=observer.__class__.__name__,
                        event_action=event.action,
                        message=str(exc),
                        timestamp=self._clock.now(),
                    )
                )


class SecurityEventQueryService:
    def __init__(self, event_source: ISecurityEventSource) -> None:
        if not isinstance(event_source, ISecurityEventSource):
            raise TypeError("event_source must implement ISecurityEventSource")
        self._event_source = event_source

    def by_severity(self, severity: Severity) -> List[SecurityEvent]:
        if not isinstance(severity, Severity):
            raise TypeError("severity must be a Severity")
        return [e for e in self._event_source.get_events() if e.severity == severity]

    def by_username(self, username: str) -> List[SecurityEvent]:
        normalized = _normalize_username(username)
        return [e for e in self._event_source.get_events() if e.username == normalized]

    def by_account(self, account_number: int) -> List[SecurityEvent]:
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        return [e for e in self._event_source.get_events() if e.account_number == account_number]

    def count_by_severity(self) -> Dict[Severity, int]:
        counts = {level: 0 for level in Severity}
        for event in self._event_source.get_events():
            counts[event.severity] += 1
        return counts




class ISecurityEventRecorder(ABC):
    @abstractmethod
    def record(self, event: SecurityEvent) -> None:
        pass

    @abstractmethod
    def add_observer(self, observer: SecurityObserver) -> None:
        pass

    @abstractmethod
    def get_events(self) -> List[SecurityEvent]:
        pass


class SecurityEventRecorder(ISecurityEventRecorder, ISecurityEventSource):
    def __init__(
        self,
        event_store: ISecurityEventStore,
        publisher: ICriticalEventPublisher,
        enabled: bool = True,
    ) -> None:
        if not isinstance(event_store, ISecurityEventStore):
            raise TypeError("event_store must implement ISecurityEventStore")
        if not isinstance(publisher, ICriticalEventPublisher):
            raise TypeError("publisher must implement ICriticalEventPublisher")
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be a bool")

        self._event_store = event_store
        self._publisher = publisher
        self._enabled = enabled

    def record(self, event: SecurityEvent) -> None:
        if not isinstance(event, SecurityEvent):
            raise TypeError("event must be a SecurityEvent")
        if not self._enabled:
            return
        self._event_store.add(event)
        if event.severity == Severity.CRITICAL:
            self._publisher.publish(event)

    def add_observer(self, observer: SecurityObserver) -> None:
        self._publisher.add_observer(observer)

    def get_events(self) -> List[SecurityEvent]:
        return self._event_store.all()


class IAccountAuditLogger(ISecurityEventSource, ABC):
    @property
    @abstractmethod
    def account_number(self) -> int:
        pass

    @abstractmethod
    def record(self, event: SecurityEvent) -> None:
        pass

    @abstractmethod
    def add_observer(self, observer: SecurityObserver) -> None:
        pass

    @abstractmethod
    def deposit(self, amount: float, username: str = "system") -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float, username: str = "system") -> None:
        pass



class IAuditLoggerFactory(ABC):
    @abstractmethod
    def create(self, account: Account, enabled: bool = True) -> IAccountAuditLogger:
        pass


class IAuditDiagnosticsReader(ABC):
    @abstractmethod
    def observer_failures(self) -> List[ObserverNotificationFailure]:
        pass


class IDiagnosticAuditLoggerFactory(IAuditLoggerFactory, IAuditDiagnosticsReader, ABC):
    pass



# =============================================================================
# SECTION 6 — FRAUD DETECTION (STRATEGY PATTERN)
# =============================================================================


@dataclass(frozen=True, slots=True)
class TransactionContext:
    username: str
    account_number: int
    action: Permission
    current_balance: float
    amount: float
    recent_action_count: int
    hour_of_day: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "username", _normalize_username(self.username))
        if not isinstance(self.account_number, int):
            raise TypeError("account_number must be an int")
        if not isinstance(self.action, Permission):
            raise TypeError("action must be a Permission")

        current_balance = round(float(self.current_balance), 2)
        if current_balance < 0:
            raise ValueError("current_balance must be non-negative")
        object.__setattr__(self, "current_balance", current_balance)

        object.__setattr__(self, "amount", validate_amount(self.amount))

        if not isinstance(self.recent_action_count, int) or self.recent_action_count < 0:
            raise ValueError("recent_action_count must be a non-negative int")
        if not isinstance(self.hour_of_day, int) or not (0 <= self.hour_of_day <= 23):
            raise ValueError("hour_of_day must be an integer between 0 and 23")


class FraudRule(ABC):
    @abstractmethod
    def evaluate(self, context: TransactionContext) -> bool:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class LargeAmountRule(FraudRule):
    def __init__(
        self,
        threshold: float = 5_000.0,
        applicable_actions: Optional[Iterable[Permission]] = None,
    ) -> None:
        self._threshold = validate_amount(threshold)
        actions = _OUTGOING_PERMISSIONS if applicable_actions is None else frozenset(applicable_actions)
        for action in actions:
            if not isinstance(action, Permission):
                raise TypeError("applicable_actions must contain Permission values")
        self._applicable_actions = frozenset(actions)

    def evaluate(self, context: TransactionContext) -> bool:
        if context.action not in self._applicable_actions:
            return False
        return context.amount > self._threshold

    def description(self) -> str:
        return f"Amount exceeds {self._threshold:.2f}"


class RapidOutgoingTransactionRule(FraudRule):
    def __init__(self, max_recent_actions: int = 5) -> None:
        if max_recent_actions < 1:
            raise ValueError("max_recent_actions must be >= 1")
        self._max_recent = int(max_recent_actions)

    def evaluate(self, context: TransactionContext) -> bool:
        if context.action not in _OUTGOING_PERMISSIONS:
            return False
        return context.recent_action_count >= self._max_recent

    def description(self) -> str:
        return f"Rapid outgoing transaction frequency >= {self._max_recent}"


class BalanceRatioRule(FraudRule):
    def __init__(
        self,
        max_ratio: float = 0.8,
        applicable_actions: Optional[Iterable[Permission]] = None,
    ) -> None:
        if not (0 < max_ratio <= 1):
            raise ValueError("max_ratio must be between 0 and 1")
        self._max_ratio = float(max_ratio)
        actions = _OUTGOING_PERMISSIONS if applicable_actions is None else frozenset(applicable_actions)
        for action in actions:
            if not isinstance(action, Permission):
                raise TypeError("applicable_actions must contain Permission values")
        self._applicable_actions = frozenset(actions)

    def evaluate(self, context: TransactionContext) -> bool:
        if context.action not in self._applicable_actions:
            return False
        if context.current_balance <= 0:
            return False
        return (context.amount / context.current_balance) > self._max_ratio

    def description(self) -> str:
        return f"Amount exceeds {self._max_ratio * 100:.0f}% of current balance"


class UnusualHourRule(FraudRule):
    def __init__(
        self,
        allowed_start_hour: int = 7,
        allowed_end_hour: int = 22,
        applicable_actions: Optional[Iterable[Permission]] = None,
    ) -> None:
        start = int(allowed_start_hour)
        end = int(allowed_end_hour)
        if not (0 <= start <= 23) or not (0 <= end <= 24) or start >= end:
            raise ValueError("allowed hours must define a valid half-open interval")
        self._start = start
        self._end = end

        if applicable_actions is None:
            self._applicable_actions: Optional[frozenset[Permission]] = None
        else:
            actions = frozenset(applicable_actions)
            for action in actions:
                if not isinstance(action, Permission):
                    raise TypeError("applicable_actions must contain Permission values")
            self._applicable_actions = actions

    def evaluate(self, context: TransactionContext) -> bool:
        if self._applicable_actions is not None and context.action not in self._applicable_actions:
            return False
        return not (self._start <= context.hour_of_day < self._end)

    def description(self) -> str:
        return f"Transaction outside allowed hours {self._start:02d}:00–{self._end:02d}:00"


class IFraudDetectionEngine(ABC):
    @abstractmethod
    def check(self, context: TransactionContext) -> List[str]:
        pass

    @abstractmethod
    def add_rule(self, rule: FraudRule) -> None:
        pass


class FraudDetectionEngine(IFraudDetectionEngine):
    def __init__(self, rules: Iterable[FraudRule]) -> None:
        materialised_rules = list(rules)
        if not materialised_rules:
            raise ValueError("rules must be a non-empty iterable of FraudRule objects")
        for rule in materialised_rules:
            if not isinstance(rule, FraudRule):
                raise TypeError(
                    f"All rules must be FraudRule instances; got {type(rule)}"
                )
        self._rules: List[FraudRule] = materialised_rules
        self._lock = threading.RLock()

    def add_rule(self, rule: FraudRule) -> None:
        if not isinstance(rule, FraudRule):
            raise TypeError("rule must be a FraudRule")
        with self._lock:
            self._rules.append(rule)

    def check(self, context: TransactionContext) -> List[str]:
        if not isinstance(context, TransactionContext):
            raise TypeError("context must be a TransactionContext")
        with self._lock:
            rules_snapshot = list(self._rules)
        return [rule.description() for rule in rules_snapshot if rule.evaluate(context)]


# =============================================================================
# SECTION 7 — RATE LIMITING (FACTORY METHOD PATTERN)
# =============================================================================


class LimiterType(Enum):
    TOKEN_BUCKET = "token_bucket"
    STRICT_WINDOW = "strict_window"


@dataclass(frozen=True, slots=True)
class TokenBucketConfig:
    capacity: int = 10
    refill_rate: float = 2.0

    def __post_init__(self) -> None:
        if self.capacity < 1:
            raise ValueError("capacity must be >= 1")
        if self.refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")


@dataclass(frozen=True, slots=True)
class StrictWindowConfig:
    max_requests: int = 5
    window_seconds: float = 60.0

    def __post_init__(self) -> None:
        if self.max_requests < 1:
            raise ValueError("max_requests must be >= 1")
        if self.window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")


RateLimiterOptions = TokenBucketConfig | StrictWindowConfig | None


# Rate limiting is intentionally user-scoped rather than session-scoped.
# Logging out one session resets the user's limiter state across all sessions.
class RateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, username: str, action: Optional[Permission] = None) -> bool:
        pass

    @abstractmethod
    def reset(self, username: str) -> None:
        pass


class TokenBucketRateLimiter(RateLimiter):
    def __init__(
        self,
        capacity: int = 10,
        refill_rate: float = 2.0,
        clock: Optional[IClock] = None,
    ) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        self._capacity = int(capacity)
        self._refill_rate = float(refill_rate)
        self._tokens: Dict[Tuple[str, Optional[Permission]], float] = {}
        self._last_refill: Dict[Tuple[str, Optional[Permission]], float] = {}
        self._clock = clock or SystemClock()
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")
        self._lock = threading.RLock()

    @staticmethod
    def _build_key(
        username: str,
        action: Optional[Permission],
    ) -> Tuple[str, Optional[Permission]]:
        normalized = _normalize_username(username)
        if action is not None and not isinstance(action, Permission):
            raise TypeError("action must be a Permission or None")
        return (normalized, action)

    def _refill(self, key: Tuple[str, Optional[Permission]]) -> None:
        now = self._clock.monotonic()
        if key not in self._tokens:
            self._tokens[key] = float(self._capacity)
            self._last_refill[key] = now
            return
        elapsed = now - self._last_refill[key]
        self._tokens[key] = min(
            float(self._capacity),
            self._tokens[key] + elapsed * self._refill_rate,
        )
        self._last_refill[key] = now

    def is_allowed(self, username: str, action: Optional[Permission] = None) -> bool:
        key = self._build_key(username, action)
        with self._lock:
            self._refill(key)
            if self._tokens[key] >= 1.0:
                self._tokens[key] -= 1.0
                return True
            return False

    def reset(self, username: str) -> None:
        normalized = _normalize_username(username)
        with self._lock:
            keys_to_remove = [key for key in self._tokens if key[0] == normalized]
            for key in keys_to_remove:
                self._tokens.pop(key, None)
                self._last_refill.pop(key, None)


class StrictWindowRateLimiter(RateLimiter):
    def __init__(
        self,
        max_requests: int = 5,
        window_seconds: float = 60.0,
        clock: Optional[IClock] = None,
    ) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self._max_requests = int(max_requests)
        self._window = float(window_seconds)
        self._request_times: Dict[Tuple[str, Optional[Permission]], List[float]] = {}
        resolved_clock = SystemClock() if clock is None else clock
        self._clock = resolved_clock
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")
        self._lock = threading.RLock()

    @staticmethod
    def _build_key(
        username: str,
        action: Optional[Permission],
    ) -> Tuple[str, Optional[Permission]]:
        normalized = _normalize_username(username)
        if action is not None and not isinstance(action, Permission):
            raise TypeError("action must be a Permission or None")
        return (normalized, action)

    def is_allowed(self, username: str, action: Optional[Permission] = None) -> bool:
        now = self._clock.monotonic()
        cutoff = now - self._window
        key = self._build_key(username, action)
        with self._lock:
            timestamps = [ts for ts in self._request_times.get(key, []) if ts >= cutoff]
            if len(timestamps) >= self._max_requests:
                self._request_times[key] = timestamps
                return False
            timestamps.append(now)
            self._request_times[key] = timestamps
            return True

    def reset(self, username: str) -> None:
        normalized = _normalize_username(username)
        with self._lock:
            keys_to_remove = [key for key in self._request_times if key[0] == normalized]
            for key in keys_to_remove:
                self._request_times.pop(key, None)


class RateLimiterCreator(ABC):
    @abstractmethod
    def create_limiter(self, options: RateLimiterOptions = None) -> RateLimiter:
        pass


class TokenBucketCreator(RateLimiterCreator):
    def __init__(self, clock: Optional[IClock] = None) -> None:
        resolved_clock = SystemClock() if clock is None else clock
        self._clock = resolved_clock
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")

    def create_limiter(self, options: RateLimiterOptions = None) -> RateLimiter:
        if options is None:
            options = TokenBucketConfig()
        if not isinstance(options, TokenBucketConfig):
            raise TypeError("TokenBucketCreator requires TokenBucketConfig")
        return TokenBucketRateLimiter(
            capacity=options.capacity,
            refill_rate=options.refill_rate,
            clock=self._clock,
        )


class StrictWindowCreator(RateLimiterCreator):
    def __init__(self, clock: Optional[IClock] = None) -> None:
        resolved_clock = SystemClock() if clock is None else clock
        self._clock = resolved_clock
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")

    def create_limiter(self, options: RateLimiterOptions = None) -> RateLimiter:
        if options is None:
            options = StrictWindowConfig()
        if not isinstance(options, StrictWindowConfig):
            raise TypeError("StrictWindowCreator requires StrictWindowConfig")
        return StrictWindowRateLimiter(
            max_requests=options.max_requests,
            window_seconds=options.window_seconds,
            clock=self._clock,
        )


class IRateLimiterFactory(ABC):
    @abstractmethod
    def create(
        self,
        limiter_type: LimiterType,
        rate_limiter_options: RateLimiterOptions = None,
    ) -> RateLimiter:
        pass

    @abstractmethod
    def register_creator(
        self,
        limiter_type: LimiterType,
        creator: RateLimiterCreator,
    ) -> None:
        pass


class RateLimiterFactory(IRateLimiterFactory):
    def __init__(
        self,
        creators: Optional[Mapping[LimiterType, RateLimiterCreator]] = None,
    ) -> None:
        resolved_creators = (
            {
                LimiterType.TOKEN_BUCKET: TokenBucketCreator(),
                LimiterType.STRICT_WINDOW: StrictWindowCreator(),
            }
            if creators is None
            else creators
        )

        validated: Dict[LimiterType, RateLimiterCreator] = {}
        for key, value in resolved_creators.items():
            if not isinstance(key, LimiterType):
                raise TypeError("creator map keys must be LimiterType")
            if not isinstance(value, RateLimiterCreator):
                raise TypeError("creator map values must be RateLimiterCreator")
            validated[key] = value

        self._creator_map = validated
        self._lock = threading.RLock()

    def register_creator(
        self,
        limiter_type: LimiterType,
        creator: RateLimiterCreator,
    ) -> None:
        if not isinstance(limiter_type, LimiterType):
            raise TypeError("limiter_type must be a LimiterType enum")
        if not isinstance(creator, RateLimiterCreator):
            raise TypeError("creator must be a RateLimiterCreator")
        with self._lock:
            self._creator_map[limiter_type] = creator

    def create(
        self,
        limiter_type: LimiterType,
        rate_limiter_options: RateLimiterOptions = None,
    ) -> RateLimiter:
        if not isinstance(limiter_type, LimiterType):
            raise TypeError("limiter_type must be a LimiterType enum")
        with self._lock:
            creator = self._creator_map.get(limiter_type)
        if creator is None:
            raise ValueError(f"No creator registered for {limiter_type}")
        return creator.create_limiter(rate_limiter_options)

# =============================================================================
# SECTION 9 — TRANSACTION MONITORING
# =============================================================================


@dataclass(frozen=True, slots=True)
class TransactionRecord:
    timestamp: float
    action: Permission
    username: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", float(self.timestamp))
        if not isinstance(self.action, Permission):
            raise TypeError("action must be a Permission")
        object.__setattr__(self, "username", _normalize_username(self.username))


class ITransactionMonitor(ABC):
    @abstractmethod
    def record(self, account_number: int, action: Permission, username: str) -> None:
        pass

    @abstractmethod
    def recent_count(
        self,
        account_number: int,
        action: Optional[Permission] = None,
        username: Optional[str] = None,
        window_seconds: float = 10.0,
    ) -> int:
        pass


class TransactionMonitor(ITransactionMonitor):
    def __init__(self, retention_seconds: float = 60.0, clock: Optional[IClock] = None) -> None:
        if retention_seconds <= 0:
            raise ValueError("retention_seconds must be > 0")
        self._retention_seconds = float(retention_seconds)
        resolved_clock = SystemClock() if clock is None else clock
        self._clock = resolved_clock
        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")
        self._records: Dict[int, List[TransactionRecord]] = {}
        self._lock = threading.RLock()

    def _prune(self, account_number: int, now: float) -> None:
        records = self._records.get(account_number)
        if records is None:
            return

        cutoff = now - self._retention_seconds
        fresh_records = [
            record for record in records if record.timestamp >= cutoff
        ]

        if fresh_records:
            self._records[account_number] = fresh_records
        else:
            self._records.pop(account_number, None)

    def record(self, account_number: int, action: Permission, username: str) -> None:
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        if not isinstance(action, Permission):
            raise TypeError("action must be a Permission")
        normalized_username = _normalize_username(username)

        now = self._clock.monotonic()
        with self._lock:
            self._prune(account_number, now)
            records = self._records.setdefault(account_number, [])
            records.append(
                TransactionRecord(
                    timestamp=now,
                    action=action,
                    username=normalized_username,
                )
            )

    def recent_count(
        self,
        account_number: int,
        action: Optional[Permission] = None,
        username: Optional[str] = None,
        window_seconds: float = 10.0,
    ) -> int:
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        if action is not None and not isinstance(action, Permission):
            raise TypeError("action must be a Permission or None")
        if username is not None:
            username = _normalize_username(username)
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")

        now = self._clock.monotonic()
        cutoff = now - window_seconds
        with self._lock:
            self._prune(account_number, now)
            records = self._records.get(account_number, [])

            if action is None and username is None:
                return sum(1 for record in records if record.timestamp >= cutoff)

            return sum(
                1
                for record in records
                if record.timestamp >= cutoff
                and (action is None or record.action == action)
                and (username is None or record.username == username)
            )


# =============================================================================
# SECTION 10 — OPERATION SECURITY PIPELINE
# =============================================================================
class OperationType(Enum):
    READ = "read"
    MONETARY = "monetary"


@dataclass(frozen=True, slots=True)
class SecurityOperationContext:
    auth_session: AuthSession
    account_number: int
    action: Permission
    logger: IAccountAuditLogger
    account: Optional[Account] = None
    amount: Optional[float] = None

    def __post_init__(self) -> None:
        if not isinstance(self.auth_session, AuthSession):
            raise TypeError("auth_session must be an AuthSession")
        if not isinstance(self.account_number, int):
            raise TypeError("account_number must be an int")
        if not isinstance(self.action, Permission):
            raise TypeError("action must be a Permission")
        if not isinstance(self.logger, IAccountAuditLogger):
            raise TypeError("logger must implement IAccountAuditLogger")
        if self.account is not None and not isinstance(self.account, Account):
            raise TypeError("account must implement Account")
        if self.amount is not None:
            object.__setattr__(self, "amount", validate_amount(self.amount))

        if (self.account is None) != (self.amount is None):
            raise ValueError("account and amount must either both be provided or both be omitted")


class ISecurityStep(ABC):
    @abstractmethod
    def supports(self, operation_type: OperationType) -> bool:
        pass

    @abstractmethod
    def execute(self, context: SecurityOperationContext) -> None:
        pass


class AuthenticatedSessionStep(ISecurityStep):
    def __init__(self, authenticator: ISessionAwareAuthenticator) -> None:
        if not isinstance(authenticator, ISessionAwareAuthenticator):
            raise TypeError("authenticator must implement ISessionAwareAuthenticator")
        self._authenticator = authenticator

    def supports(self, operation_type: OperationType) -> bool:
        return operation_type in (OperationType.READ, OperationType.MONETARY)

    def execute(self, context: SecurityOperationContext) -> None:
        if not self._authenticator.is_authenticated_session(context.auth_session):
            raise AuthenticationError(
                f"Session '{context.auth_session.session_id}' for user "
                f"'{context.auth_session.user.username}' is not authenticated. "
                "Please log in before performing operations."
            )
        self._authenticator.touch_session(context.auth_session.session_id)


class AuthorizationStep(ISecurityStep):
    def __init__(
        self,
        authorization_policy: IAuthorizationPolicy,
        event_factory: ISecurityEventFactory,
    ) -> None:
        if not isinstance(authorization_policy, IAuthorizationPolicy):
            raise TypeError("authorization_policy must implement IAuthorizationPolicy")
        if not isinstance(event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")
        self._authorization_policy = authorization_policy
        self._event_factory = event_factory

    def supports(self, operation_type: OperationType) -> bool:
        return operation_type in (OperationType.READ, OperationType.MONETARY)

    def execute(self, context: SecurityOperationContext) -> None:
        try:
            self._authorization_policy.check_permission(
                context.auth_session.user,
                context.action,
                context.account_number,
            )
        except AuthorizationError:
            context.logger.record(
                self._event_factory.no_amount_event(
                    username=context.auth_session.user.username,
                    account_number=context.account_number,
                    action=SecurityAction.ACCESS_DENIED,
                    status=EventStatus.DENIED,
                    message=(
                        f"User '{context.auth_session.user.username}' denied "
                        f"'{context.action.name}' on account {context.account_number}"
                    ),
                    severity=Severity.WARNING,
                )
            )
            raise


class RateLimitStep(ISecurityStep):
    def __init__(self, rate_limiter: RateLimiter, event_factory: ISecurityEventFactory) -> None:
        if not isinstance(rate_limiter, RateLimiter):
            raise TypeError("rate_limiter must implement RateLimiter")
        if not isinstance(event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")
        self._rate_limiter = rate_limiter
        self._event_factory = event_factory

    def supports(self, operation_type: OperationType) -> bool:
        return operation_type == OperationType.MONETARY

    def execute(self, context: SecurityOperationContext) -> None:
        if not self._rate_limiter.is_allowed(context.auth_session.user.username, context.action):
            context.logger.record(
                self._event_factory.no_amount_event(
                    username=context.auth_session.user.username,
                    account_number=context.account_number,
                    action=SecurityAction.RATE_LIMIT_EXCEEDED,
                    status=EventStatus.BLOCKED,
                    message="Request rate limit exceeded",
                    severity=Severity.WARNING,
                )
            )
            raise RateLimitExceededError(
                f"Rate limit exceeded for user '{context.auth_session.user.username}'"
            )


class FraudCheckStep(ISecurityStep):
    def __init__(
        self,
        fraud_engine: IFraudDetectionEngine,
        transaction_monitor: ITransactionMonitor,
        clock: IClock,
        event_factory: ISecurityEventFactory,
    ) -> None:
        if not isinstance(fraud_engine, IFraudDetectionEngine):
            raise TypeError("fraud_engine must implement IFraudDetectionEngine")
        if not isinstance(transaction_monitor, ITransactionMonitor):
            raise TypeError("transaction_monitor must implement ITransactionMonitor")
        if not isinstance(clock, IClock):
            raise TypeError("clock must implement IClock")
        if not isinstance(event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")

        self._fraud_engine = fraud_engine
        self._transaction_monitor = transaction_monitor
        self._clock = clock
        self._event_factory = event_factory

    def supports(self, operation_type: OperationType) -> bool:
        return operation_type == OperationType.MONETARY

    def execute(self, context: SecurityOperationContext) -> None:
        if context.account is None or context.amount is None:
            return

        tx_context = TransactionContext(
            username=context.auth_session.user.username,
            account_number=context.account_number,
            action=context.action,
            current_balance=context.account.get_balance(),
            amount=context.amount,
            recent_action_count=self._transaction_monitor.recent_count(
                context.account_number,
                action=context.action,
                username=context.auth_session.user.username,
            ),
            hour_of_day=self._clock.now().hour,
        )

        triggered = self._fraud_engine.check(tx_context)
        if triggered:
            context.logger.record(
                self._event_factory.transaction_event(
                    username=context.auth_session.user.username,
                    account_number=context.account_number,
                    action=SecurityAction.FRAUD_DETECTED,
                    amount=context.amount,
                    status=EventStatus.FLAGGED,
                    message="Triggered rules: " + ", ".join(triggered),
                    severity=Severity.CRITICAL,
                )
            )
            raise FraudAlertError(f"Transaction flagged: {', '.join(triggered)}")


class ISecurityOperationPipeline(ABC):
    @abstractmethod
    def secure_read(
        self,
        auth_session: AuthSession,
        account_number: int,
        action: Permission,
        logger: IAccountAuditLogger,
    ) -> None:
        pass

    @abstractmethod
    def secure_monetary_action(
        self,
        auth_session: AuthSession,
        account_number: int,
        action: Permission,
        amount: float,
        account: Account,
        logger: IAccountAuditLogger,
    ) -> None:
        pass

class ISecurityStepResolver(ABC):
    @abstractmethod
    def resolve(self, operation_type: OperationType) -> Sequence[ISecurityStep]:
        pass


class SecurityStepResolver(ISecurityStepResolver):
    def __init__(self, steps: Iterable[ISecurityStep]) -> None:
        resolved_steps = tuple(steps)
        if not resolved_steps:
            raise ValueError("steps must not be empty")
        for step in resolved_steps:
            if not isinstance(step, ISecurityStep):
                raise TypeError("all steps must implement ISecurityStep")
        self._steps = resolved_steps

    def resolve(self, operation_type: OperationType) -> Sequence[ISecurityStep]:
        if not isinstance(operation_type, OperationType):
            raise TypeError("operation_type must be an OperationType")
        return tuple(step for step in self._steps if step.supports(operation_type))

class SecurityOperationPipeline(ISecurityOperationPipeline):
    def __init__(self, step_resolver: ISecurityStepResolver) -> None:
        if not isinstance(step_resolver, ISecurityStepResolver):
            raise TypeError("step_resolver must implement ISecurityStepResolver")
        self._step_resolver = step_resolver

    def _run(
        self,
        operation_type: OperationType,
        context: SecurityOperationContext,
    ) -> None:
        for step in self._step_resolver.resolve(operation_type):
            step.execute(context)

    def secure_read(
        self,
        auth_session: AuthSession,
        account_number: int,
        action: Permission,
        logger: IAccountAuditLogger,
    ) -> None:
        context = SecurityOperationContext(
            auth_session=auth_session,
            account_number=account_number,
            action=action,
            logger=logger,
        )
        self._run(OperationType.READ, context)

    def secure_monetary_action(
        self,
        auth_session: AuthSession,
        account_number: int,
        action: Permission,
        amount: float,
        account: Account,
        logger: IAccountAuditLogger,
    ) -> None:
        context = SecurityOperationContext(
            auth_session=auth_session,
            account_number=account_number,
            action=action,
            amount=amount,
            account=account,
            logger=logger,
        )
        self._run(OperationType.MONETARY, context)


class SecurityOperationPipelineFactory:
    @staticmethod
    def from_legacy_dependencies(
        authenticator: ISessionAwareAuthenticator,
        authorization_policy: IAuthorizationPolicy,
        fraud_engine: IFraudDetectionEngine,
        rate_limiter: RateLimiter,
        transaction_monitor: ITransactionMonitor,
        clock: Optional[IClock] = None,
        event_factory: Optional[ISecurityEventFactory] = None,
    ) -> SecurityOperationPipeline:
        if not isinstance(authenticator, ISessionAwareAuthenticator):
            raise TypeError("authenticator must implement ISessionAwareAuthenticator")
        if not isinstance(authorization_policy, IAuthorizationPolicy):
            raise TypeError("authorization_policy must implement IAuthorizationPolicy")
        if not isinstance(fraud_engine, IFraudDetectionEngine):
            raise TypeError("fraud_engine must implement IFraudDetectionEngine")
        if not isinstance(rate_limiter, RateLimiter):
            raise TypeError("rate_limiter must implement RateLimiter")
        if not isinstance(transaction_monitor, ITransactionMonitor):
            raise TypeError("transaction_monitor must implement ITransactionMonitor")

        resolved_clock = SystemClock() if clock is None else clock
        if not isinstance(resolved_clock, IClock):
            raise TypeError("clock must implement IClock")

        resolved_event_factory = (
            SecurityEventFactory(resolved_clock)
            if event_factory is None
            else event_factory
        )
        if not isinstance(resolved_event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")

        auth_step = AuthenticatedSessionStep(authenticator)
        authorization_step = AuthorizationStep(
            authorization_policy,
            resolved_event_factory,
        )
        rate_limit_step = RateLimitStep(rate_limiter, resolved_event_factory)
        fraud_step = FraudCheckStep(
            fraud_engine,
            transaction_monitor,
            resolved_clock,
            resolved_event_factory,
        )

        step_resolver = SecurityStepResolver(
            steps=(
                auth_step,
                authorization_step,
                rate_limit_step,
                fraud_step,
            )
        )

        return SecurityOperationPipeline(step_resolver=step_resolver)

