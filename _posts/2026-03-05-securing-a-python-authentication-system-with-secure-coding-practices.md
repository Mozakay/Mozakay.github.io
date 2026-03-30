---
layout: post
title: Securing a Python Authentication System with Secure Coding Practices
subtitle: Refactoring an insecure authentication example by adding password hashing, input validation, strong password rules, and rate limiting
categories:
  - Software Development
tags: [unit7, secure-coding, authentication, python, bcrypt, input-validation, password-policy, rate-limiting]
---

## Overview

This post presents my Unit 7 Collaborative Discussion 3 work on secure coding practices in a Python authentication system. The original design contained several security weaknesses, including plaintext password storage, weak password acceptance, direct string-based authentication logic, lack of input validation, and no rate limiting. The refactored version improved the design by introducing password hashing with `bcrypt`, username sanitisation, stronger password policy checks, safer authentication behaviour, and basic rate-limiting with temporary account lockout.

## Summary of the Work

The purpose of this task was to examine an insecure authentication example and refactor it using secure coding practices. The refactored solution focused on five main improvements. First, plaintext passwords were replaced with hashed passwords. Second, usernames were validated through an allow-list pattern to reject unsafe input formats. Third, password validation rules were introduced to block weak or common passwords. Fourth, authentication logic was changed so that credentials were checked against stored hashes rather than through direct plain-text comparison. Fifth, a rate limiter was added to slow repeated failed logins and reduce brute-force risk. Together, these changes made the authentication system safer, more robust, and easier to maintain.

## Security Vulnerabilities Identified

The original code presented several important weaknesses:

- **Plaintext password storage** exposed user credentials directly if the system or data store were compromised.
- **Weak password acceptance** allowed predictable passwords such as `admin123` and `password`.
- **Direct string comparison in authentication** provided an unsafe foundation for authentication logic and increased future database-integration risk.
- **No input validation** meant suspicious or malformed usernames could be passed into the system.
- **No rate limiting** allowed unlimited login attempts, which increased exposure to brute-force attacks.

## Refactored Design

The refactored solution is organised around several focused components:

- `validate_password()` for checking password strength rules
- `sanitise_username()` for safe username validation
- `RateLimiter` for recording failures and applying temporary lockouts
- `User` for storing the username and hashed password only
- `AuthenticationSystem` for registration and authentication behaviour

This structure separates security concerns more clearly and makes the code easier to extend and reason about.

## Before and After Refactoring

In the earlier version, the system stored passwords directly in memory and compared them using simple string matching. This meant the design was functionally simple but insecure. It also did not attempt to validate usernames, reject weak passwords, or prevent repeated failed logins.

After refactoring, the system became more defensive. Passwords are now hashed before storage, usernames are checked against a safe pattern, weak passwords are rejected at registration, and failed login attempts can trigger a temporary lockout. The authentication flow also uses `bcrypt.checkpw()` rather than direct password comparison, which is more appropriate for secure credential handling.

## Code Development

The refactored code keeps the overall purpose of the original system but improves its internal design and security posture. Users can still be registered and authenticated, but the system now treats authentication as a security-sensitive process rather than a simple functional check. This improves both practical safety and code quality.

### Main Source Code

The source code includes the following main parts:

- `validate_password()`
- `sanitise_username()`
- `RateLimiter`
- `User`
- `AuthenticationSystem`

## Application of Secure Coding Practices

### Secure Password Storage

The refactored design no longer stores readable passwords. Instead, each password is hashed with `bcrypt` before being saved.

hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
self._users[clean_username] = User(clean_username, hashed)

This change reduces the risk of direct credential exposure and aligns the system with safer password-handling practice.

### Input Validation

The refactored solution validates usernames using an allow-list pattern. Only letters, digits, underscores, hyphens, and dots are accepted.

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.\-]{3,64}$")

def sanitise_username(username: str) -> Optional[str]:
    if not isinstance(username, str):
        return None
    username = username.strip()
    if not USERNAME_PATTERN.match(username):
        return None
    return username

This helps reject suspicious input early and makes the authentication process safer, especially if the design is extended later to interact with external systems or databases.

### Password Policy Enforcement

The new version checks passwords against strength rules, including minimum length, upper-case and lower-case letters, digits, special characters, and a weak-password list.

MIN_PASSWORD_LENGTH = 12

WEAK_PASSWORDS = {
    "admin123", "password", "password123", "123456"
}

This makes weak password selection less likely and strengthens the security of user accounts at the point of registration.

### Secure Authentication Logic

Authentication is now based on hash comparison rather than direct string comparison.

password_correct = bcrypt.checkpw(
    password.encode("utf-8"),
    user.hashed_password,
)

The refactored design also uses a dummy hash path when a username is not found. This helps reduce timing differences and makes behaviour more consistent when authentication fails.

### Rate Limiting Against Brute-Force Attacks

A `RateLimiter` class records failed login attempts inside a time window and applies a temporary lockout after repeated failures.

MAX_ATTEMPTS    = 5
WINDOW_SECONDS  = 300
LOCKOUT_SECONDS = 900

This reduces the risk of unlimited guessing attempts and improves the defensive behaviour of the system under attack conditions.

## Python Source Code

This project includes the secure authentication system and its demonstration code.

### Source Code

- [Discussion 3.py](/assets/code/oop/unit7/Discussion%203.py)

## Code Execution

The refactored program was executed to demonstrate the main security improvements. The outputs show weak-password rejection during registration, blocked unsafe input, correct authentication handling, and temporary lockout after repeated failures.

<img src="/assets/images/oop/unit7/run%20code%201%20discussion%203.png" alt="Figure 1 - Registration checks" width="600">

**Figure 1.** Registration output showing rejection of weak passwords and successful registration of a strong password.

<img src="/assets/images/oop/unit7/run%20code%202%20discussion%203.png" alt="Figure 2 - Authentication checks" width="600">

**Figure 2.** Authentication output showing blocked unsafe input, failed login with incorrect credentials, and successful login with the correct password.

<img src="/assets/images/oop/unit7/run%20code%203%20discussion%203.png" alt="Figure 3 - Rate limiting checks" width="600">

**Figure 3.** Output demonstrating repeated failed attempts and temporary lockout behaviour used to reduce brute-force risk.

## Reflection

This work showed that secure coding is not limited to adding isolated protections, but requires the whole authentication flow to be redesigned around safer defaults. The original code was simple to read, but it trusted user input too easily and protected credentials poorly. The refactored version improved the system by treating password handling, input checking, and failed-login behaviour as core parts of the design rather than optional extras. This task strengthened my understanding of how security weaknesses often arise from oversimplified logic and how object-oriented structure can support more secure and maintainable software.

The original design was vulnerable because it exposed several core authentication risks at once, including plain-text password storage, weak password acceptance, unsafe input handling, and unlimited login attempts. The refactored version reduced this risk by treating authentication as a security-critical boundary through password hashing, strict validation, stronger password rules, and rate limiting. This is important beyond this small task because weaknesses in authentication can compromise the security of an entire system, not just the login function itself.
