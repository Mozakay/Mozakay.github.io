---
layout: post
title: Engineering Correctness in Concurrent Transactions
subtitle: A thread-safe bank account implementation with concurrency testing, deadlock prevention, and livelock analysis
categories:
  - Software Development
tags: [unit6, concurrency, thread-safety, race-condition, deadlock, livelock, python, testing]
---

## Overview

This post presents my Unit 6 work on concurrency and correctness in a banking system. The implementation was designed to preserve correct balances under concurrent transactions, prevent deadlock during transfers, and demonstrate how liveness issues such as livelock can still appear even when deadlock is avoided.

The system was developed in connected stages. First, it implemented a `BankAccount` with `deposit()`, `withdraw()`, and `get_balance()`. Second, it modelled concurrent workers operating on shared state. Third, it supported account-to-account transfers with deadlock avoidance through fixed lock ordering. Finally, it evaluated correctness using eight structured tests supported by screenshots and a summary table.

## Summary of the Work

Concurrency can make simple-looking code unreliable because final outcomes depend on thread interleavings rather than the written order of statements. For this reason, the design focused on disciplined synchronisation and requirement-linked testing. The implementation used locking around shared balance access, barriers to increase overlap between threads, deterministic setup where needed, and targeted tests for correctness, failure handling, race conditions, deadlock prevention, integration, and livelock.

Taken together, the results provide evidence for both safety and liveness. Safety here means balances remain correct and invariants are preserved. Liveness here means the system continues to make progress and avoids freezing under the tested scenarios.

## System Architecture and Component Responsibilities

At a system level, the design is divided into focused parts with clear responsibilities. `TransactionSimulator` coordinates concurrent worker threads and applies actions through the `Account` abstraction. `Operation` objects represent transaction behaviour, while `OperationFactory` creates those operations separately from execution. This structure improves clarity, extensibility, and maintainability.

<img src="/assets/images/oop/unit6/Figure%201%20-%20System%20Architecture.png" alt="Figure 1 - System Architecture" width="700">

**Figure 1.** System architecture.

<img src="/assets/images/oop/unit6/Figure%202%20-%20Operation%20and%20OperationFactory%20parts.png" alt="Figure 2 - Operation and OperationFactory parts" width="700">

**Figure 2.** Operation and OperationFactory parts.

<img src="/assets/images/oop/unit6/Figure%203%20-%20TransactionSimulator%20part.png" alt="Figure 3 - TransactionSimulator part" width="700">

**Figure 3.** TransactionSimulator part.

<img src="/assets/images/oop/unit6/Figure%204%20-%20Zoom-in%20view%20of%20TransactionSimulator%20Threads.png" alt="Figure 4 - Zoom-in view of TransactionSimulator Threads" width="700">

**Figure 4.** Zoom-in view of TransactionSimulator threads.

## Shared-State Synchronisation and Thread Safety

Thread safety is concentrated inside `BankAccount` because it owns the shared mutable balance. A lock protects `deposit()`, `withdraw()`, and `get_balance()`, so each read and write passes through the same synchronised boundary. This helps prevent lost updates and inconsistent reads during concurrent execution.

The contrast between the safe and unsafe versions makes this visible. The safe version uses locking to protect balance updates, while the unsafe version removes locking so that race conditions can be observed under load.

<img src="/assets/images/oop/unit6/Figure%205%20-%20Safe%20Bank%20Account%20(Locking).png" alt="Figure 5 - Safe Bank Account (Locking)" width="700">

**Figure 5.** Safe BankAccount with locking.

<img src="/assets/images/oop/unit6/Figure%207%20-%20Unsafe%20Bank%20Account.png" alt="Figure 7 - Unsafe Bank Account" width="700">

**Figure 7.** Unsafe BankAccount used to demonstrate race conditions.

## Transfer Semantics and Deadlock Avoidance

Transfers introduce an additional concurrency risk because two threads may each hold one account lock and wait for the other. The implementation avoids this by ordering locks consistently using `account_number` before balance updates take place. This removes circular wait and turns deadlock prevention into a deliberate design property rather than an accident of scheduling.

<img src="/assets/images/oop/unit6/Figure%206%20-%20Deadlock-Safe%20Transfer.png" alt="Figure 6 - Deadlock-Safe Transfer" width="700">

**Figure 6.** Deadlock-safe transfer through deterministic lock ordering.

## Verification Strategy and Test Evidence

The test suite was designed to provide clear evidence across different concurrency risks. It included deposits-only tests, unsafe race-condition tests, mixed deposit/withdraw scenarios, failed-withdrawal handling, transfer correctness, integration testing through the simulator, and livelock demonstration. The overall test run completed successfully, and the following figures show the recorded outputs.

<img src="/assets/images/oop/unit6/Figure%208%20-%20Test%20Suite%20Results.png" alt="Figure 8 - Test Suite Results" width="700">

**Figure 8.** Test suite results.

<img src="/assets/images/oop/unit6/Figure%209%20-%20Test%201%20and%202%20results.png" alt="Figure 9 - Test 1 and 2 results" width="700">

**Figure 9.** Test 1 and Test 2 results.

<img src="/assets/images/oop/unit6/Figure%2010%20-%20Test%203%20result.png" alt="Figure 10 - Test 3 result" width="700">

**Figure 10.** Test 3 result.

<img src="/assets/images/oop/unit6/Figure%2011%20-%20Test%204%20result.png" alt="Figure 11 - Test 4 result" width="700">

**Figure 11.** Test 4 result.

<img src="/assets/images/oop/unit6/Figure%2012%20-%20Test%205%20and%206%20results.png" alt="Figure 12 - Test 5 and 6 results" width="700">

**Figure 12.** Test 5 and Test 6 results.

<img src="/assets/images/oop/unit6/Figure%2013%20-%20Test%207%20result.png" alt="Figure 13 - Test 7 result" width="700">

**Figure 13.** Test 7 result.

<img src="/assets/images/oop/unit6/Figure%2014%20-%20Test%208%20result.png" alt="Figure 14 - Test 8 result" width="700">

**Figure 14.** Test 8 result.

## Test Plan Summary

<div style="overflow-x:auto;">

<table>
  <thead>
    <tr>
      <th>Test Number</th>
      <th>Primary Goal</th>
      <th>Setup</th>
      <th>Concurrency Method</th>
      <th>Operations Executed</th>
      <th>Expected Outcome</th>
      <th>What It Proves</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Prove deposit is thread-safe under heavy load</td>
      <td>Start balance = 0.0<br>50 threads, each does 1000 deposits of 1.00</td>
      <td>Barrier to start at same time + lock inside <code>deposit()</code></td>
      <td>Deposits only</td>
      <td>Final balance = 50 × 1000 × 1.00 = 50000.00</td>
      <td>No lost updates; locking protects shared balance correctly</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Demonstrate race condition without locking</td>
      <td><code>UnsafeBankAccount</code>, 30 threads, 2000 deposits each, amount 1.00, retry up to 5 attempts</td>
      <td>Barrier start + no lock + forced interleaving using <code>sleep(0)</code></td>
      <td>Deposits only (unsafe)</td>
      <td>Actual balance differs from expected total</td>
      <td>Clear evidence that removing locks causes race condition</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Validate correct balance with a realistic small scenario</td>
      <td>Start balance = 5000.00<br>3 threads, each performs exactly 10 predefined operations</td>
      <td>Barrier + lock-protected methods</td>
      <td>Predefined list of deposits/withdrawals</td>
      <td>Final = start + total deposits − total withdrawals</td>
      <td>Correctness holds even when thread execution order varies</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Validate handling of failed withdrawals due to insufficient funds and logged pass/fail outcomes</td>
      <td>Start balance = 200.00<br>2 threads, 5 ops each</td>
      <td>Two threads + barrier + BankAccount lock + AccountLogger thread-safe log + join()</td>
      <td>Deposits + withdrawals (some may fail)</td>
      <td>Expected computed from only successful operations</td>
      <td>Insufficient funds does not break state; balance reflects only successful withdrawals</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Stress test for mixed deposits/withdrawals at scale</td>
      <td>Start = 100000.00, 30 threads, 200 ops, amounts 1–10, deterministic RNG seed</td>
      <td>Barrier start + lock-protected deposit/withdraw + join()</td>
      <td>Random mix of deposits/withdrawals</td>
      <td>Final = start + total deposits − total withdrawals</td>
      <td>Atomicity under high concurrency; balance remains consistent</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Prove transfers are deadlock-free under opposing concurrency</td>
      <td>Two accounts: A = 10000, B = 10000, 2 threads, opposing transfers</td>
      <td>Barrier + consistent lock ordering by <code>account_number</code> + <code>join(timeout=5)</code></td>
      <td>A to B and B to A</td>
      <td>Both threads finish within timeout; total A + B remains 20000.00</td>
      <td>Lock ordering prevents deadlock and total money is conserved</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Integration test of simulator + factory + logger</td>
      <td>Start balance = 10000.00, fixed operations, 3 threads, 50 ops each, seed 42</td>
      <td>Threads inside simulator + deterministic RNG choice</td>
      <td>Deterministic fixed deposit/withdraw operations</td>
      <td>Balance matches replayed expected result; logger records 150 entries</td>
      <td>End-to-end correctness + repeatability + logger coverage</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Demonstrate livelock: activity without progress, no deadlock</td>
      <td>Two locks, 2 threads, 500 attempts, progress counter</td>
      <td>Barriers keep retries aligned; non-blocking second-lock attempts with retry</td>
      <td>500 lock-acquire attempts per thread; neither thread ever holds both locks</td>
      <td>Progress count = 0</td>
      <td>Livelock concept: retries can prevent progress without deadlock</td>
    </tr>
  </tbody>
</table>

</div>

## Python Source Code

The complete Python implementation used for this unit is available below:

- [IndividualCoding.py](/assets/code/oop/unit6/IndividualCoding.py)


## Reflection

This work showed that concurrency correctness must be engineered deliberately rather than assumed from simple-looking code. The locked `BankAccount` preserved correct balances under contention, while the unsafe version revealed how easily race conditions appear when synchronisation is removed. The transfer logic also showed that deadlock avoidance can be designed through deterministic lock ordering. Finally, the livelock test demonstrated that active threads do not always guarantee useful progress. Together, the figures and summary table provide clear evidence that the implementation met its main concurrency requirements under the tested scenarios.
