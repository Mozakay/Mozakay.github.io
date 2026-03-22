---
layout: post
title: Secure E-Learning Platform Design and TDD
subtitle: Designing, refactoring, and testing a user management module for a secure e-learning platform
categories: Software Development
tags: [unit10, software-architecture, object-oriented-design, tdd, e-learning-platform, python, secure-design]
---

## Overview

This post presents the design, refactoring, and testing of the User Management module developed as part of a secure e-learning platform. The module was designed to support valid user registration, reject invalid input, allow correct login, block incorrect login, and protect passwords through hashing. The work also shows how the internal structure was improved through refactoring while preserving the same external behaviour.

## Summary of the Work

The final version of the module follows a clearer layered structure made up of a Domain layer, a Repository layer, and a Service layer. The earlier version stored user data directly inside `UserService`, which made the design more tightly coupled and harder to maintain. After refactoring, storage responsibilities were moved into `UserRepository` and `InMemoryUserRepository`, which improved separation of concerns, maintainability, and testability. The testing evidence confirmed that the refactored version still behaved correctly, with 10 tests passing successfully across registration, validation, login, password hashing, and repository behaviour.

## Final Layered Architecture

The final design uses three main layers:
- **Domain layer** for the `User` class
- **Repository layer** for `UserRepository` and `InMemoryUserRepository`
- **Service layer** for `UserService`, registration, login, and password hashing

<img src="/assets/images/oop/unit10/Figure%201%20-%20user%20management%20module%20layered%20architecture.png" alt="Figure 1 - User management module layered architecture" width="900">

**Figure 1.** Final layered architecture of the User Management module.

## Before and After Refactoring

The earlier design placed storage directly inside `UserService`. This meant that validation, business logic, storage, and password handling were all managed by the same class. After refactoring, storage was moved into a separate repository structure. This made the design cleaner and easier to extend.

<img src="/assets/images/oop/unit10/Figure%202%20-%20Before%20Refactor%20-%20UserService%20with%20Internal%20Storage.png" alt="Figure 2 - Before refactor UserService with internal storage" width="900">

**Figure 2.** Before refactoring, `UserService` stored users internally.

<img src="/assets/images/oop/unit10/Figure%203%20-%20After%20Refactor%20-%20UserService%20Using%20Repository.png" alt="Figure 3 - After refactor UserService using repository" width="900">

**Figure 3.** After refactoring, `UserService` depends on a repository.

<img src="/assets/images/oop/unit10/Figure%204%20-%20After%20Refactor%20-%20Abstract%20UserRepository.png" alt="Figure 4 - After refactor abstract UserRepository" width="900">

**Figure 4.** Abstract `UserRepository`.

<img src="/assets/images/oop/unit10/Figure%205%20-%20After%20Refactor%20-%20InMemoryUserRepository%20Implementation.png" alt="Figure 5 - After refactor InMemoryUserRepository implementation" width="900">

**Figure 5.** `InMemoryUserRepository` implementation.

<img src="/assets/images/oop/unit10/Figure%2010%20-%20After%20Refactor%20%E2%80%93%20Repository%20Based%20Storage%20Design.png" alt="Figure 10 - Repository based storage design" width="900">

**Figure 10.** Refactored storage design based on the repository pattern.

<img src="/assets/images/oop/unit10/Figure%2011%20-%20Before%20Refactor%20-%20Direct%20Storage%20Inside%20UserService.png" alt="Figure 11 - Direct storage inside UserService" width="900">

**Figure 11.** Direct storage inside `UserService` before refactoring.

## Code Development

The code was improved without changing the main behaviour of the module. Registration still validated input, prevented duplicates, created a `User` object, and hashed the password. Login still checked input, found the user, and compared the stored password hash with the entered password hash. The key improvement was that data access moved from direct internal storage to the repository layer.

### `register_user()` Before and After

<img src="/assets/images/oop/unit10/Figure%206%20-%20Before%20Refactor%20-%20register%20user%20Method.png" alt="Figure 6 - Before refactor register user method" width="900">

**Figure 6.** Earlier version of `register_user()`.

<img src="/assets/images/oop/unit10/Figure%207%20-%20After%20Refactor%20-%20register%20user%20Method.png" alt="Figure 7 - After refactor register user method" width="900">

**Figure 7.** Improved version of `register_user()`.

### `login()` Before and After

<img src="/assets/images/oop/unit10/Figure%208%20-%20Before%20Refactor%20-%20login%20Method.png" alt="Figure 8 - Before refactor login method" width="900">

**Figure 8.** Earlier version of `login()`.

<img src="/assets/images/oop/unit10/Figure%209%20-%20After%20Refactor%20-%20login%20Method.png" alt="Figure 9 - After refactor login method" width="900">

**Figure 9.** Improved version of `login()`.

## My Python Code

Paste your actual Python code below in sections.

### User Class

```python
# Paste your User class here
