---
layout: post
title: Refactoring Pricing Logic with Code Smells and Strategy Pattern
subtitle: Improving readability and maintainability by replacing magic numbers and conditional logic with named constants and object-oriented refactoring
categories: ["Advance OOP"]
tags: [unit8, refactoring, code-smells, strategy-pattern, python, object-oriented-design, maintainability, clean-code]
---
 
## Overview
 
This post presents my Unit 8 Collaborative Discussion 4 work on refactoring and code smells. The task examined a simple pricing function that worked correctly but contained design issues that reduced readability and maintainability. In particular, the original version relied on magic numbers for discount values and used conditional logic directly inside the pricing process. The refactored version improved the design by introducing named constants and applying the Strategy Pattern to separate discount behaviour from the main calculation logic.
 
## Summary of the Work
 
The main aim of this work was to improve the internal structure of the original function without changing its overall behaviour. The refactoring focused on two key problems. First, discount values such as `0.9` and `0.8` were used directly in the code, which made their meaning less clear. Second, the use of `if`, `elif`, and `else` within the pricing process placed discount rules too close to the main calculation logic. The refactored solution replaced these values with named constants and moved discount behaviour into separate strategy classes. This made the code easier to read, easier to maintain, and more suitable for future extension.
 
## Code Smells Identified
 
Two main code smells were identified in the original design.
 
The first was the presence of magic numbers. Values such as `0.9` and `0.8` represented discount rates, but their meaning was not immediately obvious. This reduced code clarity and made future updates less convenient.
 
The second was the use of conditional logic in the pricing function. The pricing process was responsible not only for calculating totals, but also for selecting which discount rule should apply. This increased coupling and made the function harder to extend as new product types or discount rules were introduced.
 
## Refactored Design
 
The refactored solution is organised around a clearer object-oriented structure. The main parts are:
 
- `DiscountStrategy` as the abstract strategy interface
- `BookDiscount` for book pricing rules
- `ElectronicsDiscount` for electronics pricing rules
- `NoDiscount` for item types with no discount
- `get_discount_strategy()` for selecting the correct strategy
- `calculate_total_price()` for applying the chosen strategy and calculating the final total
 
This structure separates discount behaviour from the main calculation process and improves maintainability.
 
## Before and After Refactoring
 
In the earlier design, discount values and discount selection logic were embedded directly in the main pricing function. This made the function responsible for too many concerns at once. It calculated totals, contained discount rules, and handled product-type decisions.
 
After refactoring, discount behaviour was moved into separate strategy classes, while discount rates were expressed through named constants. The main function became simpler because it now focuses only on iterating through items, selecting a strategy, and adding the discounted price to the total. This improved separation of concerns and reduced complexity in the central pricing logic.
 
## Code Development
 
The refactored code preserved the original pricing behaviour while improving the overall design. Each product type is now associated with a focused class that applies its own pricing rule. This means that the system can be extended more easily in the future. For example, a new product type can be introduced by creating another strategy class rather than rewriting the main function.
 
### Main Source Code
 
The source code includes the following key parts:
 
- `DiscountStrategy`
- `BookDiscount`
- `ElectronicsDiscount`
- `NoDiscount`
- `get_discount_strategy()`
- `calculate_total_price()`
 
## Application of Refactoring Principles
 
### Improving Readability
 
The use of named constants improved readability by replacing unclear numeric values with meaningful identifiers. Instead of relying on raw values such as `0.9` and `0.8`, the refactored design uses `BOOK_DISCOUNT`, `ELECTRONICS_DISCOUNT`, and `NO_DISCOUNT`. This makes the code easier to understand and update.
 
```python
BOOK_DISCOUNT = 0.9
ELECTRONICS_DISCOUNT = 0.8
NO_DISCOUNT = 1.0
```
 
This change made the meaning of each discount rate more explicit and reduced ambiguity in the pricing logic.
 
### Reducing Conditional Complexity
 
The original design relied on conditional statements inside the pricing process. This made the function less flexible because every new discount rule would require additional logic in the same area of the code.
 
```python
def get_discount_strategy(item_type):
    if item_type == "book":
        return BookDiscount()
    elif item_type == "electronics":
        return ElectronicsDiscount()
    else:
        return NoDiscount()
```
 
This refactoring reduced the amount of decision-making inside the main pricing function and improved clarity in the overall design.
 
### Applying the Strategy Pattern
 
The Strategy Pattern was used to move discount behaviour into separate interchangeable classes. This allowed each discount rule to be represented as an independent object.
 
```python
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price):
        pass
 
class BookDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * BOOK_DISCOUNT
```
 
This design makes discount behaviour more modular and supports easier extension without rewriting the core calculation process.
 
### Improving Separation of Concerns
 
The refactored function now focuses only on processing items and applying the selected strategy.
 
```python
def calculate_total_price(items):
    total = 0
    for item in items:
        strategy = get_discount_strategy(item["type"])
        total += strategy.apply_discount(item["price"])
    return total
```
 
This shows a clearer separation between pricing flow and discount behaviour, which improves maintainability and supports cleaner future development.
 
## Python Source Code
 
This project includes the refactored pricing system in Python.
 
### Source Code
- [Discussion 4.py](/assets/code/oop/unit8/Discussion%204.py)
 
## Code Execution
 
The program was executed using an example input list containing a book, an electronics item, and a clothing item. The final output confirmed that the function applied the correct strategy for each item type and calculated the combined total successfully.
 
<img src="/assets/images/oop/unit8/run%20code%20discussin%204.png" alt="Figure 1 - Code execution output" width="600">
 
**Figure 1.** Code execution showing the pricing result after applying the refactored discount strategies.
 
## Reflection
 
This work showed that refactoring is not only about changing the appearance of code, but about improving its internal structure so that it becomes easier to understand, maintain, and extend. The original function was small and functional, but its design contained issues that would become more serious as the system grew. Replacing magic numbers with named constants improved clarity, while moving discount behaviour into separate strategy classes reduced complexity in the main function. This task strengthened my understanding of how object-oriented refactoring can support cleaner design and better long-term maintainability without changing external behaviour.
