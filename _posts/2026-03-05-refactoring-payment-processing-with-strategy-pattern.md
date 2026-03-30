---
layout: post
title: Refactoring Payment Processing with the Strategy Pattern
subtitle: Improving extensibility and maintainability by replacing conditional logic with interchangeable payment strategies
categories:
  - Software Development
tags: [unit5, strategy-pattern, behavioural-patterns, refactoring, python, object-oriented-design, payment-processing, maintainability]
---

## Overview

This post presents my Unit 5 Collaborative Discussion 2 work on behavioural design patterns. The task focused on a simple payment processing system that used conditional logic to handle different payment methods such as credit card, PayPal, and bank transfer. Although the original version worked, its design was not suitable for long-term extension because all payment behaviours were placed inside one method. The refactored version applied the Strategy Pattern to separate payment behaviour into interchangeable classes and improve the overall structure.

## Summary of the Work

The main aim of this work was to analyse the weaknesses in the original payment processor and redesign it using the Strategy Pattern. The original implementation relied on a growing if/elif chain, which increased coupling and made the code harder to maintain. The refactored design introduced an abstract PaymentStrategy interface and separate concrete classes for each payment type. The PaymentProcessor was then updated to work with a selected strategy instead of containing all payment rules directly. This improved extensibility, readability, and maintainability.

## Refactored Design

The refactored payment system is organised around the following main parts:
- `PaymentStrategy` as the common strategy interface
- `CreditCardPayment` for credit card transactions
- `PayPalPayment` for PayPal transactions
- `BankTransferPayment` for bank transfer transactions
- `PaymentProcessor` for coordinating payment execution through the selected strategy

This structure separates behaviour more clearly and makes the system easier to extend with new payment methods in the future.

## Before and After Refactoring

In the earlier design, the PaymentProcessor contained all payment decisions inside a single method. This meant that adding a new payment method required editing the same class and extending the conditional chain. As the number of payment methods increased, the code would become more difficult to read, test, and maintain.

After refactoring, each payment method was moved into its own strategy class. The PaymentProcessor no longer decides how each payment should work. Instead, it delegates the payment action to the chosen strategy object. This reduced conditional complexity and created a more flexible design. The change also supported the Open/Closed Principle because new payment methods can be added without modifying the existing processor logic.

## Code Development

The refactored code preserved the original behaviour of processing payments while improving the internal design. Each payment strategy now has a focused responsibility, which makes the code easier to understand and test. The PaymentProcessor was also designed to raise a clear error when no strategy is set, which improves reliability and prevents silent failure.

### Main Source Code

The source code includes the following key classes:
- `PaymentStrategy`
- `CreditCardPayment`
- `PayPalPayment`
- `BankTransferPayment`
- `PaymentProcessor`

## Application of the Strategy Pattern

### Problems in the Original Design

The original design used a long conditional chain to process different payment methods. This reduced readability and made future change more difficult. Anaya (2018) explains that long conditional logic often makes code harder to maintain. The design also violated the Open/Closed Principle because every new payment method required modification of the same method.

### Encapsulating Payment Behaviour

The Strategy Pattern improves this design by moving each payment algorithm into a separate class. Ayeva and Kasampalis (2018) describe strategies as a way to define interchangeable behaviours without rewriting the main workflow.

```python
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Processing credit card payment of ${amount}")
```

This code shows that each payment method follows the same interface while implementing its own behaviour independently.

### Decoupling the Processor from Concrete Payment Logic

The PaymentProcessor was refactored so that it depends on the PaymentStrategy abstraction rather than hard-coded payment branches.

```python
class PaymentProcessor:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process_payment(self, amount):
        if self.strategy is None:
            raise ValueError("No payment strategy set")
        self.strategy.pay(amount)
```

This refactoring improves flexibility because the processor can now work with any payment strategy that follows the common interface.

### Extensibility and Maintainability

Lott and Phillips (2025) note that object-oriented systems become easier to evolve when behaviour is separated into interchangeable parts. In this design, a new payment type can be added by creating another strategy class rather than changing the processor. This keeps the main workflow stable and reduces the risk of breaking existing behaviour.

### Defensive Error Handling

The processor raises a clear `ValueError` when no strategy has been assigned. This is important because it makes configuration problems visible early and improves reliability in the overall design (Keen, 2025).

## Python Source Code

This project includes the payment processing system and the related execution example.

### Source Code
- [Discussion 2.py](/assets/code/oop/unit5/Discussion%202.py)

## Code Execution

The refactored program was executed by first processing a credit card payment and then switching to PayPal payment through the same processor instance. The output confirmed that the selected strategy could be changed dynamically without modifying the processor itself.

<img src="/assets/images/oop/unit5/run%20code%20discussion%202.png" alt="Figure 1 - Code execution output" width="600">

**Figure 1.** Code execution showing successful payment processing with two different strategies.

## Reflection

This task showed that the Strategy Pattern is useful when a system contains several alternative behaviours that may grow over time. The original payment processor was functional, but it combined too much decision-making inside one method. Refactoring the code into separate strategies improved clarity and made the design easier to extend. More importantly, it showed that maintainability does not only depend on whether code runs correctly, but also on whether new behaviour can be added without disrupting the existing structure. This strengthened my understanding of behavioural design patterns and their practical value in object-oriented software development.
