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
