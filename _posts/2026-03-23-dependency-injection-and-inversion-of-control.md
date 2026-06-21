---
layout: post
title: Dependency Injection and Inversion of Control
subtitle: Refactoring a user registration system using dependency injection, inversion of control, and unit testing
categories: ["Advance OOP"]
tags: [unit11, dependency-injection, inversion-of-control, solid, python, unit-testing, refactoring]
---

## Overview

This post presents my Unit 11 work on Dependency Injection and Inversion of Control. The task focused on refactoring a tightly coupled design into a more flexible, maintainable, and testable object-oriented structure. The work shows how dependency injection can improve software design by separating dependency creation from class behaviour.

## What Are Dependency Injection and Inversion of Control?

Dependency Injection means passing a dependency into a class from outside instead of creating it inside the class. In this task, `UserManager` no longer creates `EmailService` directly. Instead, it receives a notifier through its constructor. This makes the code more flexible and easier to test.

Inversion of Control means that control over object creation and dependency management is moved outside the class. Instead of the class deciding which dependency to create, that decision is handled externally. Dependency Injection is one practical way to apply Inversion of Control.

In this refactoring, both ideas improved the design by reducing tight coupling and making the system easier to extend, maintain, and test.

## Summary of the Work

The original version of the code was tightly coupled because `UserManager` created `EmailService` directly inside its constructor. This meant the class depended on a concrete implementation and controlled its own dependency creation. As a result, the design was harder to extend, harder to test, and less maintainable.

After refactoring, the design introduced the `NotificationService` abstraction and passed the dependency into `UserManager` from outside. This changed the design from a rigid structure to one that is more aligned with SOLID principles. The refactored version also introduced `SMSService`, `MockNotificationService`, and a dependency injection container to improve object composition and testing.

## Why the Refactoring Improved the Design

The refactored code shows a clear improvement because it replaces tight coupling with a more flexible and testable structure. `UserManager` no longer depends directly on `EmailService`. Instead, it depends on the `NotificationService` abstraction. This reduces knowledge of implementation details and allows different notification methods to be used without changing the registration logic.

The design also became easier to understand because responsibilities were separated more clearly. `UserManager` now focuses on registration behaviour, while notification services handle message delivery. This made the code more maintainable and easier to extend.

## SOLID Principles Demonstrated

### Dependency Inversion Principle

The most important principle shown in this refactoring is the Dependency Inversion Principle. `UserManager`, as the high-level module, now depends on the `NotificationService` abstraction instead of depending directly on `EmailService`. This makes the code more modular and easier to change later.

### Single Responsibility Principle

Before refactoring, `UserManager` handled both registration and the creation of notifications. After refactoring, notification creation and delivery were separated into their own services. This means each class has a clearer role.

### Open/Closed Principle

The system is open for extension because new notification services can be added by implementing `NotificationService`, but the `UserManager` class does not need to be modified. The addition of `SMSService` demonstrates this clearly.

## Before Refactoring

In the original design, `UserManager` created `EmailService` directly inside the class. This made the design tightly coupled.

```python
class EmailService:
    def send_notification(self, user, message):
        print(f"Sending email to {user}: {message}")

class UserManager:
    def __init__(self):
        self.email_service = EmailService()

    def register_user(self, user):
        self.email_service.send_notification(user, "Welcome!")
```

## After Refactoring

After refactoring, `UserManager` received its dependency from outside through abstraction.

```python
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass

class EmailService(NotificationService):
    def send_notification(self, user, message):
        print(f"Sending email to {user}: {message}")

class UserManager:
    def __init__(self, notifier: NotificationService):
        self.notifier = notifier

    def register_user(self, user):
        self.notifier.send_notification(user, "Welcome!")
```

## Extension Through a New Service

A new service was added without changing the `UserManager` class.

```python
class SMSService(NotificationService):
    def send_notification(self, user, message):
        print(f"Sending SMS to {user}: {message}")
```

This shows that the design is more flexible and supports safe extension.

## Mocking and Testability

Dependency injection also improved testability. A mock notification service was created so that `UserManager` could be tested in isolation without sending a real email.

```python
class MockNotificationService(NotificationService):
    def __init__(self):
        self.messages = []

    def send_notification(self, user, message):
        self.messages.append((user, message))
```

This allowed the unit test to confirm that the correct welcome message was sent while keeping the test isolated from external systems.

## Dependency Injection Container

A dependency injection container was also introduced to automate object wiring.

```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    notifier = providers.Factory(EmailService)
    user_manager = providers.Factory(UserManager, notifier=notifier)
```

This further improved maintainability by separating object composition from object use.

## Python Source Code

The full Python file for this unit is available here:

- [Dependency Injection and Inversion of Control.py](/assets/code/oop/unit11/Dependency%20Injection%20and%20Inversion%20of%20Control.py)

## Testing and Evidence

The uploaded Python file includes:
- a unit test for `UserManager` using `MockNotificationService`
- an integration test for `EmailService`
- a test for `SMSService`
- a test for the dependency injection container

These tests showed that the refactored code was not only more flexible, but also easier to validate in isolation and in integration scenarios.

<img src="/assets/images/oop/unit11/Test%20result.png" alt="Test result for dependency injection and inversion of control" width="700">

**Figure 1.** Test results for the Dependency Injection and Inversion of Control implementation.

## Reflection

This unit showed clearly how dependency injection can improve object-oriented design. The refactored version was easier to extend, easier to test, and easier to maintain than the original tightly coupled version. Introducing the `NotificationService` abstraction reduced direct dependence on concrete classes, while the use of `MockNotificationService` supported isolated unit testing. The DI container also showed how dependency wiring can be handled more cleanly in larger systems.

Overall, the refactored code is more reusable, more maintainable, and better aligned with SOLID principles than the original design.
