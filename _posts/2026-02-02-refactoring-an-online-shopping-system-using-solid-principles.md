---
layout: post
title: Online Shopping System Refactoring with SOLID Principles
subtitle: Refactoring a simple online shopping system using object-oriented design, SOLID principles, and unit testing
categories:
  - Software Development
tags: [unit2, solid, refactoring, object-oriented-design, python, unittest, shopping-system, payment-processing, discounts]
---

## Overview

This post presents the refactoring and testing of a simple online shopping system developed in Python. The original design placed multiple responsibilities inside the `Order` class, including cart management, total calculation, and payment processing. This made the code more tightly coupled and harder to extend. The refactored version improved the design by separating responsibilities, introducing abstractions, and applying SOLID principles. The system supports adding products to an order, calculating totals, applying discounts, and processing payments through a cleaner and more maintainable structure.

## Summary of the Work

The refactored version of the system follows a clearer object-oriented structure. The `Order` class is responsible for managing items and calculating totals. Discount behaviour is handled through the `DiscountStrategy` abstraction and its implementations. Payment behaviour is handled separately through the `PaymentMethod` abstraction and the `PaymentProcessor` class. This structure improved maintainability, reduced coupling, and made the system easier to extend and test. The testing results showed that all 12 tests passed successfully across order handling, total calculation, discount processing, payment processing, extensibility, and boundary conditions.

## Refactored Design

The refactored shopping system is built around four main parts:
- **Product** for representing each item and its price
- **Order** for storing products and calculating totals
- **DiscountStrategy** for handling discount rules
- **PaymentMethod** and **PaymentProcessor** for payment processing

This structure separates the main behaviours of the system and makes the code easier to read, maintain, and extend.

## Before and After Refactoring

In the earlier design, the `Order` class handled too many responsibilities. It managed items, calculated totals, and also processed payment directly. This created tighter coupling and meant that adding a new payment method required modifying existing code. After refactoring, payment processing was moved into `PaymentProcessor`, while discount handling was separated into strategy classes. This made the design more flexible and easier to maintain.

## Code Development

The refactored code improved the structure of the shopping system without changing the main behaviour. Users can still add products, calculate totals, apply discounts, and complete payments. The main improvement is that these responsibilities are now separated across focused classes.

## Application of SOLID Principles

The refactored design applies SOLID principles in a practical way.

### Single Responsibility Principle (SRP)

The original `Order` class handled cart management, total calculation, and payment processing. After refactoring, `Order` manages items and totals only, while `PaymentProcessor` handles payment separately.

```python
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item: Product):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)

    def calculate_discounted_total(self, discount_strategy: DiscountStrategy) -> float:
        total = self.calculate_total()
        return discount_strategy.apply_discount(total)

```python
class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def process_payment(self, order: Order, discount_strategy: DiscountStrategy = None) -> str:
        if discount_strategy is None:
            discount_strategy = NoDiscount()

        final_total = order.calculate_discounted_total(discount_strategy)
        return self.payment_method.pay(final_total)

This separation improves clarity because the Order class no longer processes payments directly.

### Open/Closed Principle (OCP)

The system is open for extension but closed for modification. New payment methods and new discount strategies can be added without changing the main structure of the system.

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass

This design allows new subclasses such as ApplePayPayment or SeasonalDiscount to be introduced without modifying PaymentProcessor or Order.

Liskov Substitution Principle (LSP)

All payment subclasses follow the same contract defined by PaymentMethod. This means that CreditCardPayment, PayPalPayment, and CryptoPayment can all be used wherever a PaymentMethod is expected without breaking the system.

class CryptoPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"Processing crypto payment of {amount:.2f}"

This supports substitutability because the processor can work with any payment subclass through the same shared interface.

Interface Segregation Principle (ISP)

The abstractions remain small and focused. PaymentMethod contains only pay(), while DiscountStrategy contains only apply_discount().

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass

This avoids forcing classes to implement methods that they do not need.

Dependency Inversion Principle (DIP)

The refactored design reduces coupling by making PaymentProcessor depend on the PaymentMethod abstraction rather than concrete payment classes.

class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

This means that high-level payment logic works with abstractions rather than specific implementations such as CreditCardPayment or PayPalPayment.

Python Source Code

This project includes the shopping system and the related unit test file.

Source Code
Designing Real World Application.py
Testing and TDD Evidence

The system was tested using Python unittest to verify both functional behaviour and the refactored design. The tests covered adding items to an order, calculating totals for single and multiple products, applying percentage and fixed discounts, processing payments with different payment methods, adding a new payment method, adding a new discount strategy, applying no discount, preventing totals from falling below zero, and verifying that CryptoPayment can substitute PaymentMethod. The results showed that all 12 tests passed successfully.

<img src="/assets/images/oop/unit2/Run-tests.png" alt="Figure 1 - All tests passed" width="700">

Figure 1. Test execution showing that all 12 tests passed successfully.

<img src="/assets/images/oop/unit2/test%201%20and%202.png" alt="Figure 2 - Test 1 and 2" width="700">

Figure 2. Tests 1 and 2 verified item addition and single-item total calculation.

<img src="/assets/images/oop/unit2/test%203%20and%204.png" alt="Figure 3 - Test 3 and 4" width="700">

Figure 3. Tests 3 and 4 verified multiple-item total calculation and percentage discount handling.

<img src="/assets/images/oop/unit2/test%205%20and%206.png" alt="Figure 4 - Test 5 and 6" width="700">

Figure 4. Tests 5 and 6 verified fixed discount calculation and credit card payment.

<img src="/assets/images/oop/unit2/test%207%20and%208.png" alt="Figure 5 - Test 7 and 8" width="700">

Figure 5. Tests 7 and 8 verified PayPal payment after discount and the addition of a new payment method without modifying the processor.

<img src="/assets/images/oop/unit2/test%209%20and%2010.png" alt="Figure 6 - Test 9 and 10" width="700">

Figure 6. Tests 9 and 10 verified a new discount strategy and no-discount behaviour.

<img src="/assets/images/oop/unit2/test%2011%20and%2012.png" alt="Figure 7 - Test 11 and 12" width="700">

Figure 7. Tests 11 and 12 verified that totals do not fall below zero and that CryptoPayment can substitute PaymentMethod.

Reflection

This work showed how refactoring can improve software design without changing the required behaviour of the system. Separating order management, discount logic, and payment processing created a clearer and more maintainable structure. The use of abstractions improved extensibility and reduced coupling. The testing results also confirmed that the refactored version behaved correctly across the main shopping system scenarios.
