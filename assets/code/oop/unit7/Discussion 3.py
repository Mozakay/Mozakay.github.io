import bcrypt
import re
import time
from collections import defaultdict
from typing import Optional


# ---------------------------------------------------------------------------
# 1) PASSWORD POLICY (rules for strong passwords)
# ---------------------------------------------------------------------------
MIN_PASSWORD_LENGTH = 12
PASSWORD_POLICY_RULES = [
    (lambda p: len(p) >= MIN_PASSWORD_LENGTH,
     f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."),
    (lambda p: re.search(r"[A-Z]", p) is not None,
     "Password must contain at least one uppercase letter."),
    (lambda p: re.search(r"[a-z]", p) is not None,
     "Password must contain at least one lowercase letter."),
    (lambda p: re.search(r"\d", p) is not None,
     "Password must contain at least one digit."),
    (lambda p: re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", p) is not None,
     "Password must contain at least one special character."),
]

WEAK_PASSWORDS = {
    "admin123", "password", "password123", "123456", "letmein",
    "qwerty", "abc123", "welcome", "monkey", "dragon",
}


def validate_password(password: str) -> tuple[bool, list[str]]:
    """
    Returns (is_valid, list_of_reasons).
    If the list is empty, the password is accepted.
    """
    violations: list[str] = []

    if password.lower() in WEAK_PASSWORDS:
        violations.append("Password is too common (found in a weak-password list).")

    for rule_fn, message in PASSWORD_POLICY_RULES:
        if not rule_fn(password):
            violations.append(message)

    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# 2) INPUT VALIDATION (allow-list for usernames)
# ---------------------------------------------------------------------------
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.\-]{3,64}$")


def sanitise_username(username: str) -> Optional[str]:
    """
    Only allow safe username characters (letters, numbers, underscore, dot, hyphen).
    If the username is not valid, return None.
    This helps block suspicious input patterns early.
    """
    if not isinstance(username, str):
        return None
    username = username.strip()
    if not USERNAME_PATTERN.match(username):
        return None
    return username


# ---------------------------------------------------------------------------
# 3) RATE LIMITING (slow down brute-force attempts)
# ---------------------------------------------------------------------------
MAX_ATTEMPTS    = 5          # max failures allowed in the time window
WINDOW_SECONDS  = 300        # 5 minutes
LOCKOUT_SECONDS = 900        # lock for 15 minutes after too many failures


class RateLimiter:
    def __init__(self) -> None:
        # identifier -> timestamps of failed attempts
        self._attempts: defaultdict[str, list[float]] = defaultdict(list)
        # identifier -> time until lockout ends
        self._lockouts: dict[str, float] = {}

    def is_locked(self, identifier: str) -> bool:
        expiry = self._lockouts.get(identifier)
        if expiry and time.time() < expiry:
            return True
        # If the lock time is over, remove it
        self._lockouts.pop(identifier, None)
        return False

    def record_failure(self, identifier: str) -> None:
        now = time.time()
        window_start = now - WINDOW_SECONDS

        # Keep only failures that happened inside the time window
        self._attempts[identifier] = [
            t for t in self._attempts[identifier] if t > window_start
        ]
        self._attempts[identifier].append(now)

        # If too many failures happen, lock the account for a while
        if len(self._attempts[identifier]) >= MAX_ATTEMPTS:
            self._lockouts[identifier] = now + LOCKOUT_SECONDS
            self._attempts[identifier].clear()

    def record_success(self, identifier: str) -> None:
        """Clear failures and lockout after a successful login."""
        self._attempts.pop(identifier, None)
        self._lockouts.pop(identifier, None)

    def remaining_lockout(self, identifier: str) -> int:
        """How many seconds are left in the lockout (0 if not locked)."""
        expiry = self._lockouts.get(identifier, 0)
        remaining = int(expiry - time.time())
        return max(remaining, 0)


# ---------------------------------------------------------------------------
# 4) USER MODEL (store only the hashed password)
# ---------------------------------------------------------------------------
class User:
    def __init__(self, username: str, hashed_password: bytes) -> None:
        self.username        = username
        # Store the bcrypt hash only (never store the real password)
        self.hashed_password = hashed_password


# ---------------------------------------------------------------------------
# 5) AUTHENTICATION SYSTEM
# ---------------------------------------------------------------------------

# Dummy hash: used when a username is not found, to keep timing similar
DUMMY_HASH = bcrypt.hashpw(b"dummy_password", bcrypt.gensalt(rounds=12))


class AuthenticationSystem:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._rate_limiter = RateLimiter()

    def add_user(self, username: str, password: str) -> tuple[bool, str]:
        """
        Create a new user.
        Returns (success, message).
        """
        clean_username = sanitise_username(username)
        if clean_username is None:
            return False, (
                "Invalid username. Use 3-64 characters: letters, digits, "
                "underscores, hyphens, or dots."
            )

        if clean_username in self._users:
            return False, "Username already exists."

        is_valid, violations = validate_password(password)
        if not is_valid:
            return False, "Weak password:\n  • " + "\n  • ".join(violations)

        # Hash the password before saving it
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
        self._users[clean_username] = User(clean_username, hashed)
        return True, f"User '{clean_username}' registered successfully."

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        """
        Check username and password.
        Returns (authenticated, message).
        """
        # Validate username first (reject suspicious formats early)
        clean_username = sanitise_username(username)
        if clean_username is None:
            return False, "Invalid username format."

        # Block repeated failed logins (rate limiting / lockout)
        if self._rate_limiter.is_locked(clean_username):
            secs = self._rate_limiter.remaining_lockout(clean_username)
            return False, (
                f"Account temporarily locked. Try again in {secs} seconds."
            )

        user = self._users.get(clean_username)
        if user is None:
            # Run a dummy bcrypt check to reduce timing differences
            bcrypt.checkpw(password.encode("utf-8"), DUMMY_HASH)
            self._rate_limiter.record_failure(clean_username)
            return False, "Invalid username or password."

        # Compare the password to the stored hash
        password_correct = bcrypt.checkpw(
            password.encode("utf-8"),
            user.hashed_password,
        )

        if not password_correct:
            self._rate_limiter.record_failure(clean_username)
            return False, "Invalid username or password."

        self._rate_limiter.record_success(clean_username)
        return True, f"Welcome, {clean_username}!"


# ---------------------------------------------------------------------------
# 6) QUICK DEMO (basic checks)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    auth = AuthenticationSystem()

    print("=" * 60)
    print("REGISTRATION")
    print("=" * 60)

    # Try weak passwords (should fail)
    for uname, pwd in [("admin", "admin123"), ("user1", "password")]:
        ok, msg = auth.add_user(uname, pwd)
        print(f"[{'OK' if ok else 'FAIL'}] add_user('{uname}', '{pwd}'): {msg}\n")

    # Add a valid user
    ok, msg = auth.add_user("alice", "Tr0ub4dor&3_secure!")
    print(f"[{'OK' if ok else 'FAIL'}] add_user('alice', '<strong pwd>'): {msg}\n")

    print("=" * 60)
    print("AUTHENTICATION")
    print("=" * 60)

    # Injection-style input (blocked by username validation)
    malicious = "alice' OR '1'='1"
    ok, msg = auth.authenticate(malicious, "anything")
    print(f"[{'OK' if ok else 'BLOCKED'}] Injection attempt: {msg}\n")

    # Wrong password
    ok, msg = auth.authenticate("alice", "wrongpassword")
    print(f"[{'OK' if ok else 'FAIL'}] Wrong password: {msg}\n")

    # Correct password
    ok, msg = auth.authenticate("alice", "Tr0ub4dor&3_secure!")
    print(f"[{'OK' if ok else 'FAIL'}] Correct credentials: {msg}\n")

    print("=" * 60)
    print("BRUTE-FORCE / RATE-LIMITING")
    print("=" * 60)

    ok, msg = auth.add_user("bob", "C0rrectHorse#Battery9!")
    print(f"Registered bob: {msg}\n")

    for i in range(1, 7):
        ok, msg = auth.authenticate("bob", f"wrong_attempt_{i}")
        status = "OK" if ok else ("LOCKED" if "temporarily locked" in msg.lower() else "FAIL")
    print(f"  Attempt {i}: [{status}] {msg}")