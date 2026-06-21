---
layout: post
title: ShopEase System Design and Architecture
subtitle: Designing an e-commerce platform using layered architecture, modular design, UML, and design patterns
categories: ["Advance OOP"]
tags: [unit9, software-architecture, layered-architecture, uml, object-oriented-design, observer-pattern, dependency-injection, e-commerce]
---

## Overview

This post presents the system design for ShopEase, an e-commerce platform designed using layered architecture, modular design, object-oriented principles, and UML modelling. The aim of the design was to create a structured and maintainable architecture that separates user interaction, business logic, and data management. The design also addresses authentication, scalability, extensibility, dependency injection, and event-driven notifications.

## Summary of the Work

The ShopEase design was organised around clear architectural layers and functional modules. The system uses a presentation layer, a business logic layer, and a data access layer, with the database placed underneath. It also includes distinct modules for User Management, Authentication, Product Catalog, Cart, Order Processing, Payment, Notification, and Data Access. A UML class diagram was created to show the main domain objects and their relationships, while an Observer pattern diagram was used to explain how notifications are triggered when orders are placed. Together, these design decisions support maintainability, extensibility, and future growth.

## Layered Architecture Overview

The ShopEase system was designed using a layered architecture. The architecture is divided into the presentation layer, business logic layer, and data access layer, with the database placed beneath these layers. This structure provides a clear separation of responsibilities and helps organise the system in a manageable way.

The presentation layer contains controllers such as `UserController`, `ProductController`, `CartController`, and `OrderController`. These components receive user requests from client applications and pass them to the business logic layer. The business logic layer contains services such as `AuthenticationService`, `UserService`, `ProductCatalogService`, `CartService`, `OrderService`, `PaymentService`, and `NotificationService`. The data access layer contains repositories that isolate database operations from the rest of the system. This separation improves maintainability and reduces complexity.

<img src="/assets/images/oop/unit%209/Figure%201%20-%20architecture%20diagram.drawio.png" alt="Figure 1 - ShopEase layered architecture" width="500">

**Figure 1.** Layered architecture of the ShopEase system.

## Modular Design with Object-Oriented Principles

The system is also organised into distinct modules. These modules include User Management, Authentication, Product Catalog, Cart, Order Processing, Payment, Notification, and Data Access. Each module is responsible for a specific functional area of the system.

This modular structure improves clarity and makes the system easier to maintain. For example, user-related tasks are grouped inside User Management, product browsing is handled by Product Catalog, and the purchase workflow is coordinated by the Order Processing module. This approach reduces coupling and supports future enhancements.

<img src="/assets/images/oop/unit%209/Figure%202%20-Module%20Diagram.drawio.png" alt="Figure 2 - ShopEase module diagram" width="800">

**Figure 2.** Modular design of the ShopEase system.

## Core Functional Modules

The three core modules highlighted in the design are User Management, Product Catalog, and Order Processing.

The User Management module handles user-related operations such as account handling, profile management, and interaction with authentication services. The Product Catalog module supports browsing and retrieving product information. The Order Processing module coordinates checkout activities by interacting with the Cart, Payment, Notification, User Management, and Data Access modules. This reflects the real workflow of an e-commerce platform, where order placement depends on user identity, selected products, payment confirmation, and notification delivery.

## UML Class Diagram and Object-Oriented Design

The UML class diagram presents the main classes in the ShopEase system, including `User`, `Customer`, `Admin`, `Cart`, `CartItem`, `Order`, `OrderItem`, `Product`, and `Payment`, together with payment subclasses.

The diagram demonstrates key object-oriented principles. Encapsulation is shown through the grouping of attributes and methods inside each class. Inheritance is shown through the relationship between `User` and its subclasses `Customer` and `Admin`. Polymorphism is demonstrated in the payment hierarchy, where different payment subclasses provide alternative implementations of the same operation. This design improves flexibility, reusability, and maintainability.

<img src="/assets/images/oop/unit%209/Figure%203%20-%20UML%20Class%20Diagram.drawio.png" alt="Figure 3 - ShopEase UML class diagram" width="800">

**Figure 3.** UML class diagram showing the main classes and relationships in ShopEase.

## Security Practices: Authentication

Security is addressed through the Authentication module and the `AuthenticationService`. This ensures that authentication is treated as a dedicated concern rather than being mixed into unrelated business functions.

Authentication is important in an e-commerce system because the platform must protect user accounts, control access to features, and secure transactions. The design supports this by separating authentication logic from other services, which improves maintainability and provides a basis for stronger controls such as password hashing, role-based access control, and secure session handling.

## Scalability and Extensibility

The proposed architecture was designed with scalability and extensibility in mind. Scalability is supported by the layered structure and modular design. Because the system is divided into clear layers and modules, individual parts can be optimised or expanded without requiring major redesign of the whole platform.

Extensibility is also supported by object-oriented design. New payment methods can be introduced through the payment hierarchy, and new notification channels can be added through the notification pattern. This reduces the need to modify existing classes and supports future business growth.

## Dependency Injection

Dependency Injection is one of the important techniques supporting extensibility in this design. Although it is not shown as a separate diagram, the architecture implies that higher-level services should depend on abstractions rather than directly creating low-level components. For example, `OrderService` should use payment and notification services through injection rather than hard-coded internal creation.

This approach reduces tight coupling and makes the system easier to test, replace, and extend. If a new payment service is introduced, it can be integrated with limited impact on the rest of the design. The same principle applies to notification services and repository implementations.

## Observer Pattern for Notifications

The Observer pattern is used for the notification mechanism. In this design, `OrderService` acts as the subject, while `EmailNotification`, `SMSNotification`, and `PushNotification` act as concrete observers implementing the `NotificationObserver` interface.

When an order is placed, `OrderService` triggers `notifyObservers()`, which informs all registered observers. Each observer then handles the update in its own way. This allows the system to support multiple notification channels without embedding that logic directly in the order-processing workflow. This design improves extensibility because new notification types can be added by implementing the same observer interface without modifying the core service logic.

<img src="/assets/images/oop/unit%209/Figure%204%20-%20Observer%20Pattern%20Diagram.drawio.png" alt="Figure 4 - Observer pattern for notifications" width="800">

**Figure 4.** Observer pattern used for order notifications in ShopEase.

## Database Design and the Data Access Layer

The data access layer is represented through repository classes such as `UserRepository`, `ProductRepository`, `CartRepository`, `OrderRepository`, and `PaymentRepository`. The database contains core entities such as Users, Products, Orders, OrderItems, and Payments.

This structure separates persistence logic from business logic. Rather than allowing services to communicate directly with the database, repositories act as intermediaries that manage storage and retrieval. This improves maintainability and makes the system easier to adapt if the storage mechanism changes in the future.

## Overall Evaluation

Overall, the ShopEase design provides a clear and structured solution for an e-commerce platform. The layered architecture supports separation of responsibilities, the modular design improves organisation, and the class design demonstrates important object-oriented principles. Security is addressed through authentication, extensibility is supported through dependency injection and polymorphism, and the notification mechanism is strengthened through the Observer pattern. Together, the diagrams show that the system was designed to support maintainability, scalability, and future growth.

## Reflection

This design task showed how software architecture and object-oriented modelling work together in a realistic e-commerce scenario. The layered architecture helped separate responsibilities clearly, while the modular structure made the system easier to understand and manage. The UML class diagram improved communication of the class relationships, and the Observer pattern provided a clear solution for handling notifications in an extensible way. Overall, the design process highlighted the importance of structuring software carefully before implementation.
