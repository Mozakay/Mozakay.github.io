---
layout: post
title: Extending A Core Banking System With A Cybersecurity Layer
subtitle: Extending an existing core banking system through a dedicated cybersecurity layer, reporting, and verification
categories:
  - Software Development
tags: [unit12, software-architecture, object-oriented-design, cybersecurity, secure-banking, python, secure-design, layered-architecture, tdd]
---


## Overview

This post presents the design, extension, and verification of a secure banking platform developed from an existing core banking system. The original banking domain, implemented in `core_banking.py`, already supported deposits, withdrawals, balance enquiries, and deadlock-safe transfers. The capstone development focused on extending this existing system by adding a dedicated cybersecurity layer in `security_layer.py`, a secured orchestration layer in `secure_banking_services.py`, a reporting layer in `security_reporting.py`, and a full verification suite in `tests_security.py`.

The result is a layered secure banking platform in which the original core banking logic remains independent, while security controls are wrapped around it to provide authentication, authorisation, session control, fraud detection, rate limiting, audit logging, alerting, and reporting.

## Summary of the Work

The final version of the system follows a clearer layered architecture in which each file has a defined role. The earlier banking logic in `core_banking.py` remained responsible for the transactional domain only. Security responsibilities were not inserted directly into the core banking classes. Instead, they were introduced through surrounding layers that validate, authorise, monitor, and report on operations before and after execution.

This design improved separation of concerns, maintainability, extensibility, and testability. It also made the system easier to explain academically, because the capstone can be understood as the secure extension of an existing banking application rather than the creation of a banking system from the beginning.

## Layered Architecture

The final design uses a layered structure around the original banking domain:

- **Core banking domain** in `core_banking.py`
- **Cybersecurity layer** in `security_layer.py`
- **Façade and service orchestration layer** in `secure_banking_services.py`
- **Threat reporting and audit summarisation layer** in `security_reporting.py`
- **Verification layer** in `tests_security.py`

<div style="text-align:center; margin:40px 0;">
  <img src="{{ '/assets/images/oop/unit12/secure_banking_architecture_layer2_fixed.png' | relative_url }}"
       alt="Figure 1 - Layered architecture of the secure banking system"
       style="max-width:500px; width:100%; height:auto;">
</div>

**Figure 1.** Layered architecture of the secure banking system.

## Security Pipeline and Operational Sequence

The layers shown in Figure 1 are not independent. They are deliberately coordinated through the security pipeline before any protected banking operation is allowed to reach the core banking domain. In practical terms, the request lifecycle follows this sequence:

**Session → RBAC → Rate Limit → Fraud → Execute**

The significance of this sequencing is that the system asks a series of security questions before any deposit, withdrawal, or transfer is executed:

1. Is the user authenticated and is the current session still active?
2. Does the user hold the required permission for this specific action on this specific account?
3. Has the user exceeded the permitted request quota within the configured time window?
4. Does the transaction trigger any configured fraud rules?
5. If execution proceeds, does the operation succeed or fail, and how should that outcome be recorded?
6. Is the registry and audit structure consistent enough to support secure orchestration and reporting?

If any of these checks fail at the relevant stage, the request is halted immediately. In such cases, the system records the appropriate security outcome where applicable, raises the relevant exception, and prevents the request from reaching the underlying banking logic. This is the practical implementation of defence in depth through advanced object-oriented design.

The widget below shows the ordered security gates through which each protected request must pass before execution is allowed to reach the banking domain.

<div style="margin: 20px 0;">
  <h4 style="margin-bottom: 10px;">Interactive Security Pipeline</h4>
  <iframe
    src="{{ '/assets/interactive/pipeline_session_rbac_rate_fraud_execute.html' | relative_url }}"
    width="100%"
    height="600"
    style="border:1px solid #d9d9d9; border-radius:12px; background:#ffffff;">
  </iframe>
</div>

The widget below explains each cybersecurity control group, the protection it provides, and the specific threat category it addresses.

<div style="margin: 20px 0;">
  <h4 style="margin-bottom: 10px;">Interactive Cybersecurity Layer Overview</h4>
  <iframe
    src="{{ '/assets/interactive/cybersecurity_layer_what_why_en.html' | relative_url }}"
    width="100%"
    height="600"
    style="border:1px solid #d9d9d9; border-radius:12px; background:#ffffff;">
  </iframe>
</div>

## Service and Execution Design

The secure façade `SecureBankingService` provides a single entry point for protected operations such as deposit, withdraw, transfer, balance retrieval, logout, and report generation. However, it does not contain the core banking logic itself. Instead, it delegates the actual work to specialised services such as:

- `SecureAccountOperationService`
- `SecureTransferService`
- `AccountSecurityRegistry`
- `SecurityOperationPipeline`
- `ThreatReportGenerator`
- `SystemReportAssembler`

This means the design preserves the independence of the original banking domain while still ensuring that all protected operations must pass through the cybersecurity layer first.

## Advanced OOP Design Principles

The widget below highlights how advanced object-oriented principles support the architecture through abstraction, layered responsibility, and maintainable service coordination.

<div style="margin: 20px 0;">
  <h4 style="margin-bottom: 10px;">Advanced OOP Overview</h4>
  <iframe
    src="{{ '/assets/interactive/advanced_oop_en.html' | relative_url }}"
    width="100%"
    height="600"
    style="border:1px solid #d9d9d9; border-radius:12px; background:#ffffff;">
  </iframe>
</div>

## Pattern-Based Security Design in `security_layer.py`

This section explains two important design ideas in `security_layer.py`. The first is the fraud-detection design, where fraud rules are implemented as separate strategies. The second is the secured operation pipeline, where each request passes through an ordered sequence of security steps before it is allowed to reach the banking domain.

These two designs show how the security layer remains structured, extensible, and easier to maintain.

### Part 1 — Fraud Detection as a Strategy-Based Design

The fraud-detection subsystem is built around the abstract `FraudRule` base class. Each rule represents one independent fraud-checking condition, while `FraudDetectionEngine` evaluates all configured rules against the same `TransactionContext`. This means that new fraud rules can be added as new classes without changing the fraud engine itself.

#### Code extract 1 — Shared fraud context and abstract rule

```python
@dataclass(frozen=True, slots=True)
class TransactionContext:
    username: str
    account_number: int
    action: Permission
    current_balance: float
    amount: float
    recent_action_count: int
    hour_of_day: int

class FraudRule(ABC):
    @abstractmethod
    def evaluate(self, context: TransactionContext) -> bool:
        pass
    @abstractmethod
    def description(self) -> str:
        pass
```
This first part shows the shared fraud context and the abstract contract used by all fraud rules.

#### Code extract 2 — Concrete fraud rules
```python
class LargeAmountRule(FraudRule): ...
class RapidOutgoingTransactionRule(FraudRule): ...
class BalanceRatioRule(FraudRule): ...
class UnusualHourRule(FraudRule): ...

class FraudDetectionEngine(IFraudDetectionEngine):
    def __init__(self, rules: Iterable[FraudRule]) -> None:
        self._rules: List[FraudRule] = list(rules)

    def check(self, context: TransactionContext) -> List[str]:
        return [rule.description() for rule in self._rules if rule.evaluate(context)]
```
This part shows that each fraud rule follows the same interface, while the engine evaluates them through the shared FraudRule abstraction.

### Part 2 — Security Pipeline as an Ordered Control Flow

The second important design idea is the secured operation pipeline. Instead of allowing a banking request to go directly into execution, the system routes it through an ordered sequence of security steps. Each step performs one specific check, and the request must pass all of them before it can continue into the banking layer.

#### Code extract 3 — Security-step contract and main steps

```python
class ISecurityStep(ABC):
    @abstractmethod
    def supports(self, operation_type: OperationType) -> bool:
        pass
    @abstractmethod
    def execute(self, context: SecurityOperationContext) -> None:
        pass

class AuthenticatedSessionStep(ISecurityStep): ...
class AuthorizationStep(ISecurityStep): ...
class RateLimitStep(ISecurityStep): ...
class FraudCheckStep(ISecurityStep): ...
```
This part shows the abstract pipeline contract and the four main security checks used before monetary execution.

#### Code extract 4 — Pipeline execution and assembly
```python
class SecurityOperationPipeline(ISecurityOperationPipeline):
    def __init__(self, step_resolver: ISecurityStepResolver) -> None:
        self._step_resolver = step_resolver

    def _run(self, operation_type: OperationType, context: SecurityOperationContext) -> None:
        for step in self._step_resolver.resolve(operation_type):
            step.execute(context)

class SecurityOperationPipelineFactory:
    @staticmethod
    def from_legacy_dependencies(...):
        auth_step = AuthenticatedSessionStep(authenticator)
        authorization_step = AuthorizationStep(authorization_policy, resolved_event_factory)
        rate_limit_step = RateLimitStep(rate_limiter, resolved_event_factory)
        fraud_step = FraudCheckStep(fraud_engine, transaction_monitor, resolved_clock, resolved_event_factory)
        step_resolver = SecurityStepResolver(
            steps=(auth_step, authorization_step, rate_limit_step, fraud_step)
        )

        return SecurityOperationPipeline(step_resolver=step_resolver)
```
This part shows how the pipeline is executed in order and how the required steps are assembled before being used by the secured services.



### Architectural Value of These Two Designs

These two designs work together inside the secure banking system. The pipeline controls when a request may continue, while the fraud subsystem controls how suspicious transaction behaviour is evaluated. In practice, FraudCheckStep is one stage inside the wider pipeline, and it delegates fraud analysis to FraudDetectionEngine.

This is important because it shows that the system does not simply collect separate security features. Instead, it organises them through abstraction, composition, and ordered execution. That is what allows the security layer to protect the original banking domain in a structured and extensible way.

## Python Source Code

This project includes the original banking domain together with the security, orchestration, reporting, and testing modules.

### Core Banking Domain
- [core_banking.py](/assets/code/oop/unit12/core_banking.py)

### Cybersecurity Layer
- [security_layer.py](/assets/code/oop/unit12/security_layer.py)

### Service Orchestration Layer
- [secure_banking_services.py](/assets/code/oop/unit12/secure_banking_services.py)

### Reporting Layer
- [security_reporting.py](/assets/code/oop/unit12/security_reporting.py)

### Verification Suite
- [tests_security.py](/assets/code/oop/unit12/tests_security.py)

## Operation Lifecycle Example

One of the strongest aspects of the project is that individual operations can be explained as protected execution journeys rather than simple method calls. For example, a withdrawal request begins at the façade layer, passes through session validation, authorisation, rate limiting, and fraud detection, and only reaches the underlying banking method if all gates succeed. If a fraud rule is triggered, the request is blocked, a security event is written, a critical alert is published, and the account balance remains unchanged.

This makes the system easier to reason about both technically and academically, because each transaction can be analysed as a controlled lifecycle with clear checkpoints, failure paths, and audit evidence.

The widget below demonstrates the lifecycle of a protected operation from request entry through the security pipeline to either successful execution or blocked termination.

<div style="margin: 20px 0;">
  <h4 style="margin-bottom: 10px;">Interactive Operation Lifecycle</h4>
  <iframe
    src="{{ '/assets/interactive/deposit_flow_live_simulator.html' | relative_url }}"
    width="100%"
    height="600"
    style="border:1px solid #d9d9d9; border-radius:12px; background:#ffffff;">
  </iframe>
</div>

## Testing and Verification Evidence

The platform was verified using Python `unittest` to confirm that the new security and reporting layers behave correctly around the original banking system. The tests cover authentication, account lockout, session expiry, role-based access control, fraud detection, rate limiting, audit logging, reporting, registry integrity, and final object-graph assembly.

The interactive map below shows how the security-layer design, SOLID principles, and grouped test evidence align across the implemented system.

<div style="margin: 20px 0;">
  <h4 style="margin-bottom: 10px;">Security Layer and SOLID Mapping</h4>
  <iframe
    src="{{ '/assets/interactive/tests_solid_security_layer_mapping.html' | relative_url }}"
    width="100%"
    height="600"
    style="border:1px solid #d9d9d9; border-radius:12px; background:#ffffff;">
  </iframe>
</div>

The grouped test evidence shows that the system behaves correctly across both normal and blocked execution paths.

<img src="/assets/images/oop/unit12/Figure%2012.%20test%201%20to%203.png" alt="Figure 12 - Tests 1 to 3" width="700">

**Figure 12.** Tests 1 to 3 verified successful login, failed login, and account lockout behaviour.

<img src="/assets/images/oop/unit12/Figure%2013.%20test%204%20to%206.png" alt="Figure 13 - Tests 4 to 6" width="700">

**Figure 13.** Tests 4 to 6 verified locked-account rejection, session expiry, and auditor withdrawal denial.

<img src="/assets/images/oop/unit12/Figure%2014.%20test%207%20to%209.png" alt="Figure 14 - Tests 7 to 9" width="700">

**Figure 14.** Tests 7 to 9 verified auditor deposit denial, owner transfer success, and fraud blocking for large transactions.

<img src="/assets/images/oop/unit12/Figure%2015.%20test%2010%20to%2012.png" alt="Figure 15 - Tests 10 to 12" width="700">

**Figure 15.** Tests 10 to 12 verified fraud alert observation, unusual-hour fraud detection, and balance-ratio transfer blocking.

<img src="/assets/images/oop/unit12/Figure%2016.%20test%2013%20and%2015.png" alt="Figure 16 - Tests 13 and 15" width="700">

**Figure 16.** Selected audit and rate-limiting tests verified denial logging and rate-limit warning events.

<img src="/assets/images/oop/unit12/Figure%2017.%20test%2016%20and%2018.png" alt="Figure 17 - Tests 16 and 18" width="700">

**Figure 17.** Reporting tests verified `ThreatReportBuilder` and `ThreatReportGenerator`.

<img src="/assets/images/oop/unit12/Figure%2018.%20test%2019%20to%2021.png" alt="Figure 18 - Tests 19 to 21" width="700">

**Figure 18.** Registry-integrity, token-bucket refill, and final composition-root tests.

<img src="/assets/images/oop/unit12/Figure%2019.%20test%2022.png" alt="Figure 19 - Test 22" width="700">

**Figure 19.** Demonstration of the secured lifecycle of a high-risk withdrawal request at 3 AM, showing how the request is blocked at the fraud stage before reaching the core banking execution layer.

## Reflection

This work showed how an existing banking transaction application can be developed into a secure banking platform without rewriting the original domain model. By preserving `core_banking.py` as the independent transactional foundation and surrounding it with specialised layers for security, orchestration, reporting, and verification, the design achieved a clearer separation of concerns and a more extensible structure.

The project also demonstrated how advanced object-oriented principles can support secure software design in practice. Abstractions, factories, decorators, strategy-based fraud rules, observer-based alerting, and layered service orchestration were not used as isolated academic patterns, but as practical mechanisms to ensure that operations are protected before execution and traceable afterwards. The testing results confirmed that the final system behaves correctly across secure, blocked, and fully integrated scenarios.
