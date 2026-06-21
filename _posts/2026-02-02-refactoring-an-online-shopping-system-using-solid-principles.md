---
layout: post
title: Online Shopping System Refactoring with SOLID Principles
subtitle: Refactoring a simple online shopping system using object-oriented design, SOLID principles, and unit testing
categories: ["Advance OOP"]
tags: [unit2, solid, refactoring, object-oriented-design, python, unittest, shopping-system, payment-processing, discounts]
---

## Overview

This post presents the refactoring and testing of a simple online shopping system developed in Python. The original design placed multiple responsibilities inside the `Order` class, including cart management, total calculation, and payment processing. This made the code more tightly coupled and harder to extend. The refactored version improved the design by separating responsibilities, introducing abstractions, and applying SOLID principles. The system supports adding products to an order, calculating totals, applying discounts, and processing payments through a cleaner and more maintainable structure.

## Summary of the Work

The refactored version of the shopping system follows a clearer object-oriented structure. The `Order` class is responsible for managing items and calculating totals. Discount behaviour is handled through the `DiscountStrategy` abstraction and its implementations. Payment behaviour is handled separately through the `PaymentMethod` abstraction and the `PaymentProcessor` class. This structure improved maintainability, reduced coupling, and made the system easier to extend and test. The testing results showed that all 12 tests passed successfully across order handling, total calculation, discount processing, payment processing, extensibility, and boundary conditions.

## Refactored Design

The shopping system is organised around four main parts:
- **Product** for representing each item and its price
- **Order** for storing products and calculating totals
- **DiscountStrategy** for handling discount rules
- **PaymentMethod** and **PaymentProcessor** for payment processing

This structure separates the main behaviours of the system and makes the code easier to read, maintain, and extend.

## Before and After Refactoring

In the earlier design, the `Order` class handled too many responsibilities. It managed items, calculated totals, and also processed payment directly. This created tighter coupling and meant that adding a new payment method required modifying existing code. After refactoring, payment processing was moved into `PaymentProcessor`, while discount handling was separated into strategy classes. This made the design more flexible and easier to maintain.

Before refactoring, order logic and payment logic were combined in one area of the system. After refactoring, the design became more modular. `Order` focuses on item management and total calculation, `DiscountStrategy` handles discount behaviour, and `PaymentProcessor` works with the `PaymentMethod` abstraction to process payment. This improved separation of concerns and supported easier future extension.

## Code Development

The refactored code improved the structure of the shopping system without changing the main behaviour. Users can still add products, calculate totals, apply discounts, and complete payments. The main improvement is that these responsibilities are now separated across focused classes.

### Main Source Code

The source code includes the following key classes:
- `Product`
- `Order`
- `DiscountStrategy`
- `NoDiscount`
- `PercentageDiscount`
- `FixedAmountDiscount`
- `PaymentMethod`
- `CreditCardPayment`
- `PayPalPayment`
- `CryptoPayment`
- `PaymentProcessor`

## Application of SOLID Principles

The refactored design applies SOLID principles in a practical way.

### Single Responsibility Principle (SRP)

The original `Order` class handled cart management, total calculation, and payment processing. After refactoring, `Order` manages items and totals only, while `PaymentProcessor` handles payment separately. This makes each class easier to understand and maintain because each one has a clearer purpose.
The refactored design applies SRP by separating order management from payment processing. The Order class now manages items and totals only, while payment is handled by PaymentProcessor.
```python
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item: Product):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)
```
  This snippet shows that Order no longer handles payment logic directly.


### Open/Closed Principle (OCP)

The refactored shopping system applies the Open/Closed Principle by allowing new behaviours to be added without changing the main structure of the existing classes. This is shown through the use of `PaymentMethod` and `DiscountStrategy` as abstractions. New payment methods and discount rules can be added by creating new subclasses, while the core design remains unchanged.

```python
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass

class CryptoPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"Processing crypto payment of {amount:.2f}"
```
  This code shows that the system can be extended by adding new subclasses without modifying the existing payment or discount processing structure.

### Liskov Substitution Principle (LSP)

The refactored shopping system applies the Liskov Substitution Principle because all payment subclasses follow the same contract defined by `PaymentMethod`. This means that `CreditCardPayment`, `PayPalPayment`, and `CryptoPayment` can all be used wherever a `PaymentMethod` is expected without breaking the system. This improves consistency and makes the behaviour of payment processing more reliable.

```python
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CryptoPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"Processing crypto payment of {amount:.2f}"
```
This code shows that `CryptoPayment` follows the same contract as other payment subclasses and can be used in place of any `PaymentMethod` implementation without affecting the behaviour of the system.

### Interface Segregation Principle (ISP)

The refactored shopping system applies the Interface Segregation Principle by keeping abstractions small and focused. The `PaymentMethod` abstraction contains only the `pay()` method, while the `DiscountStrategy` abstraction contains only the `apply_discount()` method. This avoids forcing classes to implement methods that they do not need and keeps the design simpler and more maintainable.

```python
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass
```
  This code shows that each abstraction has a single clear responsibility, so implementing classes only define the behaviour they actually need.
  
### Dependency Inversion Principle (DIP)

The refactored shopping system applies the Dependency Inversion Principle by making `PaymentProcessor` depend on the `PaymentMethod` abstraction rather than concrete payment classes. This means that the payment processing logic is no longer tied to a specific implementation such as `CreditCardPayment` or `PayPalPayment`. As a result, the design becomes more flexible and easier to extend.

```python
class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method
```
This code shows that `PaymentProcessor` works with the abstract `PaymentMethod` type rather than relying on a specific payment class.

## Python Source Code

This project includes the shopping system and the related unit test file.

### Source Code
- [Designing Real World Application.py](/assets/code/oop/unit2/Designing%20Real%20World%20Application.py)

## Testing

The refactored shopping system was tested using Python `unittest` to verify that the main functions worked correctly after refactoring. The tests covered adding items to an order, calculating totals for single and multiple products, applying percentage and fixed discounts, processing payments with different payment methods, adding a new payment method, adding a new discount strategy, applying no discount, preventing totals from falling below zero, and verifying that `CryptoPayment` can substitute `PaymentMethod`. The results showed that all 12 tests passed successfully.

<img src="/assets/images/oop/unit2/Run-tests.png" alt="Figure 1 - All tests passed" width="600">

**Figure 1.** Test execution showing that all 12 tests passed successfully.

<img src="/assets/images/oop/unit2/test%201%20and%202.png" alt="Figure 2 - Test 1 and 2" width="600">

**Figure 2.** Tests 1 and 2 verified item addition and single-item total calculation.

<img src="/assets/images/oop/unit2/test%203%20and%204.png" alt="Figure 3 - Test 3 and 4" width="600">

**Figure 3.** Tests 3 and 4 verified multiple-item total calculation and percentage discount handling.

<img src="/assets/images/oop/unit2/test%205%20and%206.png" alt="Figure 4 - Test 5 and 6" width="600">

**Figure 4.** Tests 5 and 6 verified fixed discount calculation and credit card payment.

<img src="/assets/images/oop/unit2/test%207%20and%208.png" alt="Figure 5 - Test 7 and 8" width="600">

**Figure 5.** Tests 7 and 8 verified PayPal payment after discount and the addition of a new payment method without modifying the processor.

<img src="/assets/images/oop/unit2/test%209%20and%2010.png" alt="Figure 6 - Test 9 and 10" width="600">

**Figure 6.** Tests 9 and 10 verified a new discount strategy and no-discount behaviour.

<img src="/assets/images/oop/unit2/test%2011%20and%2012.png" alt="Figure 7 - Test 11 and 12" width="600">

**Figure 7.** Tests 11 and 12 verified that totals do not fall below zero and that `CryptoPayment` can substitute `PaymentMethod`.

## Reflection

This work showed how refactoring can improve software design without changing the required behaviour of the system. Separating order management, discount logic, and payment processing created a clearer and more maintainable structure. The use of abstractions improved extensibility and reduced coupling. The testing results also confirmed that the refactored version behaved correctly across the main shopping system scenarios.
