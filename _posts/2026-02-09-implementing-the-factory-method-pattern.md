---
layout: post
title: Implementing the Factory Method Pattern
subtitle: Designing a car manufacturing system using the Factory Method Pattern in Python
categories:
  - Software Development
tags: [unit3, factory-method, design-patterns, object-oriented-design, python, creational-patterns]
---

## Overview

This post presents the design and implementation of a car manufacturing system using the Factory Method Pattern in Python. The task required a solution that could create different car types, such as Sedan, SUV, and Hatchback, without hardcoding their concrete classes in the main program. The final design uses abstract classes, concrete products, and concrete factories to separate object creation from object use. This makes the system easier to extend and maintain.

## Summary of the Work

A car company may need to build several models, such as Sedan, SUV, Hatchback, and Electric Car. The main program should not be tied to these specific classes. A better approach is to use the Factory Method Pattern. This pattern keeps object creation separate from object use, so the client code works with abstract types while factories handle the actual creation of objects.

The design begins with an abstract `Car` type. It defines one required behaviour, `drive()`, which ensures that all concrete car classes follow the same contract. Concrete car classes such as `Sedan`, `SUV`, `Hatchback`, and `ElectricCar` each implement this method in their own way. This keeps the variation inside the product classes rather than in the client logic.

An abstract `CarFactory` class is then created with the factory method `create_car()`. Each concrete factory overrides this method and returns a specific car type. For example, `SedanFactory` returns a `Sedan`, while `SUVFactory` returns an `SUV`. This design allows the client code to remain independent from concrete product classes.

## Factory Method Design

The system is organised around four main elements:
- **Abstract product** represented by `Car`
- **Concrete products** represented by `Sedan`, `SUV`, `Hatchback`, and `ElectricCar`
- **Abstract creator** represented by `CarFactory`
- **Concrete creators** represented by `SedanFactory`, `SUVFactory`, `HatchbackFactory`, and `ElectricFactory`

This structure ensures that object creation is delegated to specialised factory classes rather than being hardcoded in the main program.

## How the Pattern Works

The Factory Method Pattern separates object creation from the main program. Instead of directly instantiating objects such as `Sedan()` or `SUV()`, the client code works with a factory abstraction. A factory object is passed into the client function, which then calls `create_car()` to obtain a car object and `drive()` to use it.

This means the client does not need to know the exact class being created. It depends only on the abstract `Car` and `CarFactory` types. This reduces coupling and makes the design easier to extend.

## Demonstration

The client function `client_code(factory)` accepts any subclass of `CarFactory`. When `SedanFactory()` is passed, the system creates a `Sedan`. When `SUVFactory()` is passed, it creates an `SUV`. The same logic works for `HatchbackFactory()` and `ElectricFactory()`.

This demonstrates the key benefit of the Factory Method Pattern. The client code remains unchanged while different product objects are created depending on the factory provided.

## Why This Pattern Was Suitable

The Factory Method Pattern was suitable for this task because the system needed to create several car types without specifying their exact classes in the main program. If the client code directly created each product, the system would become more tightly coupled and harder to maintain.

The addition of `ElectricCar` shows why this pattern is useful. A new car model was added by creating a new product class and a matching factory class. The existing client code did not need to change. This supports extensibility and follows the Open–Closed Principle, where stable parts of the system remain unchanged while new behaviour is added through extension.

## Demonstrating the Factory Method Pattern

The Factory Method Pattern is shown clearly in the structure of the car manufacturing system. The design separates the product interface, concrete products, factory interface, concrete factories, and client code.

### 1. Abstract Product: `Car`

The pattern begins with the abstract `Car` class. This class defines the common interface for all car types through the `drive()` method. Any concrete car must implement this behaviour.

```python
class Car(ABC):
    @abstractmethod
    def drive(self):
        pass
```
This ensures that all car objects follow the same contract.

### 2. Concrete Products: Sedan, SUV, Hatchback, and ElectricCar

The concrete product classes inherit from Car and provide their own implementation of drive(). Each class represents a specific type of car.
```python
class Sedan(Car):
    def drive(self):
        return "Driving a Sedan"

class SUV(Car):
    def drive(self):
        return "Driving an SUV"

class Hatchback(Car):
    def drive(self):
        return "Driving a Hatchback"

class ElectricCar(Car):
    def drive(self):
        return "Driving an Electric Car"
```
This shows that different products can be created while still following the same abstract interface.

### 3. Abstract Creator: CarFactory

The abstract CarFactory class defines the factory method create_car(). This is the key part of the Factory Method Pattern because object creation is delegated to factory subclasses.
```python
class CarFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass
```
This allows the client code to depend on the factory abstraction rather than specific factory classes.

### 4. Concrete Creators: SedanFactory, SUVFactory, HatchbackFactory, and ElectricFactory

Each concrete factory overrides create_car() and returns a specific car object. This is how the pattern creates different products without changing the client code.
```python
class SedanFactory(CarFactory):
    def create_car(self):
        return Sedan()

class SUVFactory(CarFactory):
    def create_car(self):
        return SUV()

class HatchbackFactory(CarFactory):
    def create_car(self):
        return Hatchback()

class ElectricFactory(CarFactory):
    def create_car(self):
        return ElectricCar()
```
This part demonstrates that each factory is responsible for creating one concrete product.

### 5. Client Code

The client code works only with the CarFactory abstraction. It does not directly create Sedan, SUV, or any other concrete car class.
```python
def client_code(factory: CarFactory):
    car = factory.create_car()
    print(car.drive())
```
This shows the main benefit of the Factory Method Pattern: the client uses the product without knowing its exact class.

### 6. Demonstration of Flexibility

The same client function can work with different factories. Only the factory object changes, while the client logic stays the same.
```python
if __name__ == "__main__":
    client_code(SedanFactory())
    client_code(SUVFactory())
    client_code(HatchbackFactory())
    client_code(ElectricFactory())
```
This demonstrates that the system is flexible and easy to extend. Adding ElectricCar required a new product class and a matching factory, but the client code did not need to change.

## Python Source Code

This project includes the Python implementation of the Factory Method Pattern.

### Source Code
- [Implementing the Factory Method Pattern.py](/assets/code/oop/unit3/Implementing%20the%20Factory%20Method%20Pattern.py)

## Implementation Evidence

The following figure shows the submitted implementation of the Factory Method Pattern for the car manufacturing system.

<img src="/assets/images/oop/unit3/Test.png" alt="Figure 1 - Factory Method Pattern implementation" width="700">

**Figure 1.** Submitted Python implementation of the Factory Method Pattern for creating different car types through factory classes.

## Reflection

This task showed how the Factory Method Pattern can simplify object creation in an object-oriented system. Instead of linking the client code to specific car classes, the design uses abstract products and abstract factories. This keeps the main program cleaner and makes the system easier to extend.

The addition of `ElectricCar` showed the practical value of the pattern. A new type was introduced by adding a new product class and a matching factory, while the client code stayed unchanged. This confirmed that the design supports lower coupling, easier maintenance, and future expansion.
