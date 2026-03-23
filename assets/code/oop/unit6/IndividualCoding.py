import threading
import random
import unittest
import time
from typing import List, Tuple
from abc import ABC, abstractmethod

class InsufficientFundsError(ValueError):
    """Raised when an account has insufficient funds for a withdrawal/transfer."""

# Validates that an amount is a positive number before any deposit or withdrawal is processed.
# Raises TypeError if the value is not a number, and ValueError if it is zero or negative.
def _validate_amount(amount: float) -> float:
    if not isinstance(amount, (int, float)):
        raise TypeError("amount must be a number")
    amount = float(amount)
    if amount <= 0:
        raise ValueError("amount must be > 0")
    return amount

# This prevents floating-point precision errors that can occur
# when adding or subtracting floats 
def _round_money(x: float) -> float:
    return round(float(x), 2)

# Abstraction for accounts to allow for future extensions without changing the interface.
# Any class that inherits Account MUST implement all four methods. This supports the SOLID principle of Dependency Inversion,
# other classes (like TransactionSimulator) depend on this abstraction rather than on BankAccount directly.
class Account(ABC):
    # Every account must have a unique account number.
    @property
    @abstractmethod
    def account_number(self) -> int:
        pass

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass

# Operation abstraction (TransactionSimulator can run any operation without modifying its part).
# The simulator calls apply() without needing to know whether it is depositing, withdrawing, or doing something else.
# New transaction types can be added by creating a new subclass without changing TransactionSimulator at all (Open/Closed Principle).
class Operation(ABC):
    @abstractmethod
    def apply(self, account: Account, rng: random.Random) -> None:
        pass
class DepositOperation(Operation):
    def __init__(self, deposit_range: Tuple[float, float]):
        self.deposit_range = deposit_range

    def apply(self, account: Account, rng: random.Random) -> None:
        account.deposit(rng.uniform(*self.deposit_range))
class WithdrawOperation(Operation):
    def __init__(self, withdraw_range: Tuple[float, float]):
        self.withdraw_range = withdraw_range

    def apply(self, account: Account, rng: random.Random) -> None:
        try:
            account.withdraw(rng.uniform(*self.withdraw_range))
        except InsufficientFundsError:
            pass
# Added an OperationFactory (Factory Method)
# So TransactionSimulator can create operations via a factory (clear Creational pattern).
# This makes it easy to swap/change operations later without editing the simulator.
class OperationFactory(ABC):
    @abstractmethod
    def create_operations(
        self,
        deposit_range: Tuple[float, float],
        withdraw_range: Tuple[float, float],
    ) -> List[Operation]:
        pass
# If fixed operations are provided (self._operations), it returns those instead of creating new ones. 
# This allows for more flexible testing (e.g. deterministic operations) without modifying the TransactionSimulator.
class BasicOperationFactory(OperationFactory):
    def __init__(self, operations: List[Operation] = None):
        self._operations = operations or []
    def create_operations(
        self,
        deposit_range: Tuple[float, float],
        withdraw_range: Tuple[float, float],
    ) -> List[Operation]:
        # Open for extension without modifying factory.
        if self._operations:
            return self._operations
        return [DepositOperation(deposit_range), WithdrawOperation(withdraw_range)]

# 1) Bank Account Class:
# Create a BankAccount class with the following attributes: Account_number (unique identifier for the account)& Balance (current balance of the account).
class BankAccount(Account):
    def __init__(self, account_number: int, balance: float = 0.0):
        self._account_number = int(account_number)          # Account_number
        self._balance = _round_money(balance)              # Balance

        # 2) Thread Safety:
        # Ensure that all methods in the BankAccount class are thread-safe. Use synchronisation mechanisms such as locks to prevent race conditions.
        self._lock = threading.Lock()

    @property
    def account_number(self) -> int:
        return self._account_number
    
    # Balance adjustment methods without locking (to be used internally)
    def _deposit_unlocked(self, amount: float) -> None:
        self._balance = _round_money(self._balance + amount)
        
    def _withdraw_unlocked(self, amount: float) -> None:
        # If sufficient funds are available
        if self._balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds: balance={self._balance}, requested={amount}"
            )
        self._balance = _round_money(self._balance - amount)
    # To run a deposit safely
    def deposit(self, amount: float) -> None:
        amount = _validate_amount(amount)       #Validate the input amount (must be a positive number).
        with self._lock:                        #Acquire the account lock to prevent race conditions.
            self._deposit_unlocked(amount)      #Update the balance inside the critical section and that is safe.
    # To run a withdrawal safely.
    def withdraw(self, amount: float) -> None:
        amount = _validate_amount(amount)
        with self._lock:
            self._withdraw_unlocked(amount)
    # To return the current balance safely.
    def get_balance(self) -> float:
        with self._lock:
            return self._balance


    # 4) Deadlock Prevention:Ensure that implementation avoids deadlocks. 
    # For example, if two users are trying to transfer money between accounts, the system should handle this without causing a deadlock.
        # To run a transfer safely and lock both accounts in a consistent order to prevent deadlocks.
    def transfer_to(self, other: "BankAccount", amount: float) -> None:
        if other is self:
            raise ValueError("Cannot transfer to the same account")
        amount = _validate_amount(amount)

        # Consistent lock ordering prevents deadlocks
        first, second = (self, other) if self.account_number < other.account_number else (other, self)

        with first._lock:
            with second._lock:
                self._withdraw_unlocked(amount)
                other._deposit_unlocked(amount)


# Unsafe Bank Account Class (for testing purposes, to demonstrate the effects of race conditions and the importance of thread safety).
class UnsafeBankAccount(Account):
    def __init__(self, account_number: int, balance: float = 0.0):
        self._account_number = int(account_number)
        self._balance = _round_money(balance)

    @property
    def account_number(self) -> int:
        return self._account_number

    def deposit(self, amount: float) -> None:
        amount = _validate_amount(amount)
        # Multiple threads can read the same balance before any write happens, causing "lost updates" when they overwrite each other.
        bal = self._balance

        # Encourages thread interleaving between the read and the write, making the race condition easier to reproduce in tests.
        time.sleep(0)

        self._balance = _round_money(bal + amount)

    def withdraw(self, amount: float) -> None:
        amount = _validate_amount(amount)
        bal = self._balance
        time.sleep(0)
        if bal < amount:
            raise InsufficientFundsError(
                f"Insufficient funds: balance={bal}, requested={amount}"
            )
        # Intentionally unsafe update (no lock).
        self._balance = _round_money(bal - amount)
    def get_balance(self) -> float:
        # Unsafe read (no lock) 
        return self._balance

# Added a Decorator (AccountLogger) to demonstrate a Structural Pattern.
# It wraps any Account and can be extended to log or trace without changing BankAccount.
# Stores a log of calls without printing and keeps test output clean. Thread-safe logging for concurrent tests.
class AccountLogger(Account):
    def __init__(self, wrapped: Account, enabled: bool = False):
        self._wrapped = wrapped
        self._enabled = enabled
        self.log = []  # stores tuples like ("deposit", amount)
        self._log_lock = threading.Lock()

    @property
    def account_number(self) -> int:
        return self._wrapped.account_number

    def _record(self, action: str, amount: float, status: str) -> None:
        if self._enabled:
            entry = (threading.current_thread().name, action, round(float(amount), 2), status)
            with self._log_lock:
                self.log.append(entry)

    def deposit(self, amount: float) -> None:
        try:
            self._wrapped.deposit(amount)
            self._record("deposit", amount, "PASS")
        except Exception:
            # If deposit fails for any reason (e.g., invalid amount), record it.
            self._record("deposit", amount, "FAILED")
            raise

    def withdraw(self, amount: float) -> None:
        try:
            self._wrapped.withdraw(amount)
            self._record("withdraw", amount, "PASS")
        except InsufficientFundsError:
            # Record FAILED then re-raise so the caller can handle it if needed.
            self._record("withdraw", amount, "FAILED")
            raise
        except Exception:
            self._record("withdraw", amount, "FAILED")
            raise

    def get_balance(self) -> float:
        return self._wrapped.get_balance()


# 3) Transaction Simulation:
# 3.1)Create a TransactionSimulator class.
class TransactionSimulator:
    # now accepts List[Account] (DIP improvement) and optional factory.
    def __init__(self, accounts: List[Account], op_factory: "OperationFactory" = None):
        self._accounts = {a.account_number: a for a in accounts}
        self._op_factory = op_factory or BasicOperationFactory()

    def _build_operations(
        self,
        deposit_range: Tuple[float, float],
        withdraw_range: Tuple[float, float]
    ) -> List[Operation]:
        return self._op_factory.create_operations(deposit_range, withdraw_range)
# Each user should perform a series of deposits and withdrawals.
# Use threads to simulate concurrent transactions.
    def run_on_single_account(
        self,
        account_number: int,
        num_users: int,
        ops_per_user: int,
        seed: int = 1,
        deposit_range: Tuple[float, float] = (1.0, 50.0),
        withdraw_range: Tuple[float, float] = (1.0, 50.0),
    ) -> None:
        # 3.1)Multiple users performing transactions on the same bank account concurrently.
        account: Account = self._accounts[account_number]
        operations = self._build_operations(deposit_range, withdraw_range)
#This worker function simulates one user thread by performing ops_per_user random transactions on the same account
# Each iteration selects one operation randomly from the available operations list.
        def worker(_uid: int) -> None:
            rng = random.Random(seed + _uid)
            # 3.2) Each user performs a series of deposits and withdrawals.
            for _ in range(ops_per_user):
                op = rng.choice(operations)  # open for extension via new Operation
                op.apply(account, rng)
        # 3.3) Use threads to simulate concurrent transactions.
        threads = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(num_users)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


# 5)Testing and Validation:
# Write unit tests to validate that the system is thread-safe and handles concurrent transactions correctly.
# Simulate scenarios where multiple users are performing transactions simultaneously and verify that the final balance is correct.
class TestThreadSafeBanking(unittest.TestCase):
    # Test 1: Concurrent deposits only
    def test_deposits_concurrent_only(self):
        # Start with a known balance
        acc = BankAccount(1, balance=0.0)

        num_users = 50
        deposits_per_user = 1000
        deposit_amount = 1.00

        start = threading.Barrier(num_users)

        def worker() -> None:
            start.wait()
            for _ in range(deposits_per_user):
                acc.deposit(deposit_amount)

        threads = [threading.Thread(target=worker, daemon=True) for _ in range(num_users)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = round(num_users * deposits_per_user * deposit_amount, 2)
        actual = acc.get_balance()

        print("\n--- Test 1 Summary (Deposits Only) ---")
        print(f"Users/Threads: {num_users}")
        print(f"Deposits per user: {deposits_per_user}")
        print(f"Deposit amount: {deposit_amount:.2f}")
        print(f"Expected final balance: {expected:.2f}")
        print(f"Actual final balance: {actual:.2f}")

        self.assertEqual(actual, expected)

        # Test 2: Demonstrate Race Condition using an UNSAFE (non-thread-safe) account.
    # This test is for educational evidence only and should not replace the safe implementation.
    def test_race_condition_demo_unsafe_account(self):
        num_users = 30
        deposits_per_user = 2000
        deposit_amount = 1.00
        expected = round(num_users * deposits_per_user * deposit_amount, 2)

        # Try a few times to avoid rare "lucky" schedules where it might match.
        actual = None
        for attempt in range(5):
            acc = UnsafeBankAccount(1, balance=0.0)
            start = threading.Barrier(num_users)

            def worker():
                start.wait()
                for _ in range(deposits_per_user):
                    acc.deposit(deposit_amount)

            threads = [threading.Thread(target=worker, daemon=True) for _ in range(num_users)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            actual = acc.get_balance()
            if actual != expected:
                break  # Race condition observed

        print("\n--- Test 2 Summary (Race Condition Demo - Unsafe Account) ---")
        print(f"Users/Threads: {num_users}")
        print(f"Deposits per user: {deposits_per_user}")
        print(f"Deposit amount: {deposit_amount:.2f}")
        print(f"Expected final balance: {expected:.2f}")
        print(f"Actual final balance:   {actual:.2f}")
        print(f"Difference:             {round((actual or 0) - expected, 2):.2f}")

        # We expect a mismatch at least once due to race conditions.
        self.assertNotEqual(actual, expected, "Race condition did not manifest; try increasing threads/loops.")


    #Test 3: Another realistic scenario with 3 users, each performing 10 operations concurrently.
    def test_small_realistic_concurrent_transactions(self):
        acc = BankAccount(1, balance=5000.00)

    # 3 users, each has exactly 10 operations (realistic-ish)
        users_ops = {
            1: [
                ("deposit", 1200.00, "salary top-up"),
                ("withdraw", 85.50, "groceries"),
                ("withdraw", 40.00, "fuel"),
                ("withdraw", 120.00, "internet bill"),
                ("deposit", 60.00, "refund"),
                ("withdraw", 25.00, "coffee"),
                ("withdraw", 200.00, "shopping"),
                ("deposit", 150.00, "cash deposit"),
                ("withdraw", 75.25, "pharmacy"),
                ("withdraw", 90.00, "dinner"),
            ],
            2: [
                ("withdraw", 300.00, "rent contribution"),
                ("deposit", 200.00, "transfer in"),
                ("withdraw", 55.75, "groceries"),
                ("withdraw", 20.00, "taxi"),
                ("deposit", 100.00, "cash deposit"),
                ("withdraw", 15.00, "snack"),
                ("withdraw", 45.00, "fuel"),
                ("deposit", 80.00, "refund"),
                ("withdraw", 60.00, "utilities"),
                ("withdraw", 30.00, "mobile top-up"),
            ],
            3: [
                ("deposit", 500.00, "bonus"),
                ("withdraw", 150.00, "shopping"),
                ("withdraw", 35.00, "breakfast"),
                ("deposit", 120.00, "transfer in"),
                ("withdraw", 65.00, "groceries"),
                ("withdraw", 25.00, "coffee"),
                ("withdraw", 90.00, "fuel"),
                ("deposit", 40.00, "refund"),
                ("withdraw", 110.00, "online order"),
                ("withdraw", 50.00, "pharmacy"),
            ],
        }

    # Print the exact operations for clarity (optional)
        print("\n--- Planned Operations Per User in Test 3 ---")
        for uid, ops in users_ops.items():
            print(f"User {uid}:")
            for kind, amt, label in ops:
                print(f"  - {kind.upper():8} {amt:8.2f}   ({label})")

        start = threading.Barrier(len(users_ops))

        def worker(uid: int) -> None:
            start.wait()
            for kind, amt, _label in users_ops[uid]:
                if kind == "deposit":
                    acc.deposit(amt)
                else:
                    acc.withdraw(amt)

        threads = [threading.Thread(target=worker, args=(uid,), daemon=True) for uid in users_ops]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # Calculate expected final balance deterministically
        total_deposits = sum(amt for ops in users_ops.values() for kind, amt, _ in ops if kind == "deposit")
        total_withdraws = sum(amt for ops in users_ops.values() for kind, amt, _ in ops if kind == "withdraw")
        expected = round(5000.00 + total_deposits - total_withdraws, 2)

        actual = acc.get_balance()

        print("\n--- Test 3 Summary (Small Realistic Concurrent Transactions) ---")
        print(f"Starting balance: {5000.00:.2f}")
        print(f"Total deposits:   {total_deposits:.2f}")
        print(f"Total withdrawals:{total_withdraws:.2f}")
        print(f"Expected:         {expected:.2f}")
        print(f"Actual:           {actual:.2f}")

        self.assertEqual(actual, expected)

    # Test 4: 2 threads with 5 operations each to validate realistic concurrent transactions and their outcomes.
    # Including failed withdrawals when funds are insufficient.
    def test_realistic_two_threads_five_ops_each(self):
        base_acc = BankAccount(1, balance=200.00)
        acc = AccountLogger(base_acc, enabled=True)

        # Barrier to synchronise the start
        start_barrier = threading.Barrier(2)

        # Thread 0: income / top-ups (5 ops)
        user0_ops = [
            ("deposit", 300.00, "salary"),
            ("deposit", 50.00,  "refund"),
            ("deposit", 60.00,  "transfer in"),
            ("deposit", 40.00,  "cash deposit"),
            ("deposit", 25.00,  "bonus"),
        ]

        # Thread 1: spending (5 ops)
        user1_ops = [
            ("withdraw", 120.00, "groceries"),
            ("withdraw", 180.00, "utilities"),
            ("withdraw", 250.00, "shopping"),
            ("withdraw", 60.00,  "pharmacy"),
            ("withdraw", 90.00,  "transport"),
        ]

        users_ops = {0: user0_ops, 1: user1_ops}

        # Print planned operations ONCE (not inside worker)
        print("\n--- Planned Operations in Test 4 (2 threads, 5 operations) ---")
        for uid, ops in users_ops.items():
            print(f"User {uid}:")
            for action, amt, label in ops:
                print(f"  - {action.upper():8} {amt:8.2f}   ({label})")

        # Single worker only
        def worker(uid: int) -> None:
            # Both threads wait here, then start together
            start_barrier.wait()

            for action, amt, _label in users_ops[uid]:
                if action == "deposit":
                    acc.deposit(amt)
                else:
                    try:
                        acc.withdraw(amt)
                    except InsufficientFundsError:
                        pass  # AccountLogger already recorded FAILED

        th0 = threading.Thread(target=worker, args=(0,), name="User-0", daemon=True)
        th1 = threading.Thread(target=worker, args=(1,), name="User-1", daemon=True)

        th0.start()
        th1.start()
        th0.join()
        th1.join()

        # Compute expected based on what actually succeeded (from AccountLogger log)
        total_deposits_pass = sum(
            amount for (_t, act, amount, status) in acc.log
            if act == "deposit" and status == "PASS"
        )
        total_withdraws_pass = sum(
            amount for (_t, act, amount, status) in acc.log
            if act == "withdraw" and status == "PASS"
        )

        expected = round(200.00 + total_deposits_pass - total_withdraws_pass, 2)
        actual = acc.get_balance()

        failed_withdraws = [
            (t, amount) for (t, act, amount, status) in acc.log
            if act == "withdraw" and status == "FAILED"
        ]

        print("\n--- AccountLogger Execution Log (order may vary) ---")
        for row in acc.log:
            print(row)

        print("\n--- Test 4 Summary (2 threads) ---")
        print(f"Starting balance: {200.00:.2f}")
        print(f"Total Deposits (PASS):   {total_deposits_pass:.2f}")
        print(f"Total Withdraws (PASS):  {total_withdraws_pass:.2f}")
        print(f"Expected balance:        {expected:.2f}")
        print(f"Actual balance:          {actual:.2f}")
        print(f"Failed withdraw attempts: {len(failed_withdraws)}")
        if failed_withdraws:
            print("Failed examples:", failed_withdraws)

        self.assertEqual(actual, expected)


    # Test 5: To validate thread-safe + concurrent transactions
    def test_concurrent_deposits_and_withdraws(self):
        acc = BankAccount(1, balance=100000.00)

        # Each user should perform a series of deposits and withdrawals.
        rng = random.Random(123)
        num_users = 30
        ops_per_user = 200

        # A list containing user's transactions.  
        ops: List[List[Tuple[str, float]]] = []
        total_deposits = 0.0
        total_withdraws = 0.0

        for _ in range(num_users):
            user_ops = []
            for _ in range(ops_per_user):
                if rng.random() < 0.5:
                    amt = round(rng.uniform(1, 10), 2)
                    total_deposits += amt
                    user_ops.append(("deposit", amt))
                else:
                    amt = round(rng.uniform(1, 10), 2)
                    total_withdraws += amt
                    user_ops.append(("withdraw", amt))
            ops.append(user_ops)

        # To validate Simulate transactions simultaneously.
        start = threading.Barrier(num_users)

        def worker(user_ops: List[Tuple[str, float]]) -> None:
            start.wait()
            for kind, amt in user_ops:
                if kind == "deposit":
                    acc.deposit(amt)
                else:
                    acc.withdraw(amt)

        threads = [threading.Thread(target=worker, args=(ops[i],), daemon=True) for i in range(num_users)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Calculate the balance
        expected = round(100000.00 + total_deposits - total_withdraws, 2)

        final_balance = acc.get_balance()
        difference = round(final_balance - expected, 2)

        print("\n--- Test 5 Concurrent Deposits/Withdrawals Summary ---")
        print(f"Users/Threads: {num_users}")
        print(f"Operations per user: {ops_per_user}")
        print(f"Total operations: {num_users * ops_per_user}")
        print(f"Starting balance: {100000.00:.2f}")
        print(f"Total deposits: {total_deposits:.2f}")
        print(f"Total withdrawals: {total_withdraws:.2f}")
        print(f"Expected final balance: {expected:.2f}")
        print(f"Actual final balance: {final_balance:.2f}")
        print(f"Difference (Actual - Expected): {difference:.2f}")

        # Verify final balance is correct + thread-safety validation
        self.assertEqual(acc.get_balance(), expected)


# Test 6: Deadlock Prevention during transfers.
    def test_deadlock_free_transfers(self):
        # Two difference accounts with initial balance of 10000.0 each.
        a = BankAccount(100, 10000.0)
        b = BankAccount(200, 10000.0)

        # Barrier makes both threads start at nearly the same time.
        start = threading.Barrier(2)

        counts = [0, 0]

        # Thread 1 waits at the barrier, then performs 5,000 
        # transfers from account A to B, transferring 1.0 each time.
        def t1() -> None:
            start.wait()
            for _ in range(5000):
                a.transfer_to(b, 1.0)
                counts[0] += 1

        # Thread 2 does the opposite transfers (from B to A).
        def t2() -> None:
            start.wait()
            for _ in range(5000):
                b.transfer_to(a, 1.0)
                counts[1] += 1

        th1 = threading.Thread(target=t1, daemon=True)
        th2 = threading.Thread(target=t2, daemon=True)
        th1.start()
        th2.start()

        # Wait for each thread to finish, but only up to 5 seconds.
        # If a deadlock occurs, the threads typically won’t finish within this time.
        th1.join(timeout=5)
        th2.join(timeout=5)
        #Test deadlock free transfers
        self.assertFalse(th1.is_alive() or th2.is_alive(), "Threads likely deadlocked")

        total = round(a.get_balance() + b.get_balance(), 2)


        print("\n--- Test 6 Transfer Summary ---")
        print(f"Thread1: completed {counts[0]} transfers (A -> B)")
        print(f"Thread2: completed {counts[1]} transfers (B -> A)")
        print(f"Final Balance A (Account 100): {a.get_balance():.2f}")
        print(f"Final Balance B (Account 200): {b.get_balance():.2f}")
        print(f"Total (A + B): {total:.2f}")

        self.assertEqual(total, 20000.0)


    # Test 7: Validate TransactionSimulator runs concurrent operations on a single account
    # and produces a correct final balance (deterministic operations via injected factory).
    def test_transaction_simulator_integration(self):
        # --- Arrange ---
        start_balance = 10000.00

        # Base account 
        base_acc = BankAccount(1, balance=start_balance)
        # Wrap it with AccountLogger (DIP)
        acc = AccountLogger(base_acc, enabled=True)

        # Deterministic operations (fixed amounts) to make expected outcome predictable
        class FixedDeposit(Operation):
            def __init__(self, amount: float):
                self.amount = amount

            def apply(self, account: Account, rng: random.Random) -> None:
                account.deposit(self.amount)

        class FixedWithdraw(Operation):
            def __init__(self, amount: float):
                self.amount = amount

            def apply(self, account: Account, rng: random.Random) -> None:
                # Should not fail because start_balance is high, but keep it safe.
                try:
                    account.withdraw(self.amount)
                except InsufficientFundsError:
                    pass

        deposit_amount = 10.00
        withdraw_amount = 7.50

        fixed_ops = [FixedDeposit(deposit_amount), FixedWithdraw(withdraw_amount)]

        # Inject operations into the simulator via the factory
        op_factory = BasicOperationFactory(operations=fixed_ops)
        simulator = TransactionSimulator([acc], op_factory=op_factory)

        num_users = 3
        ops_per_user = 50
        seed = 42

        # Compute expected result deterministically by reproducing the same rng.choice sequence
        total_deposits = 0.0
        total_withdraws = 0.0

        for uid in range(num_users):
            rng = random.Random(seed + uid)
            for _ in range(ops_per_user):
                chosen = rng.choice(fixed_ops)  # same logic used inside TransactionSimulator
                if isinstance(chosen, FixedDeposit):
                    total_deposits += deposit_amount
                else:
                    total_withdraws += withdraw_amount

        expected = round(start_balance + total_deposits - total_withdraws, 2)

        # --- Act ---
        simulator.run_on_single_account(
            account_number=1,
            num_users=num_users,
            ops_per_user=ops_per_user,
            seed=seed,
            deposit_range=(1.0, 1.0),   # not used because factory returns fixed_ops
            withdraw_range=(1.0, 1.0),  # not used because factory returns fixed_ops
        )

        actual = acc.get_balance()

        # Optional prints (you can remove if you want cleaner output)
        print("\n--- Test 7 Summary (TransactionSimulator Integration) ---")
        print(f"Users/Threads: {num_users}")
        print(f"Ops per user:  {ops_per_user}")
        print(f"Start balance: {start_balance:.2f}")
        print(f"Total deposits: {total_deposits:.2f}")
        print(f"Total withdraws:{total_withdraws:.2f}")
        print(f"Expected:      {expected:.2f}")
        print(f"Actual:        {actual:.2f}")

        print(f"Logger entries count: {len(acc.log)}")
        print(f"First 5 log entries:", [entry[1:] for entry in acc.log[:5]])

        # Balance correctness + logger validation (structural pattern)
        self.assertEqual(actual, expected)
        self.assertTrue(len(acc.log) > 0, "AccountLogger did not record any operations")
        self.assertEqual(len(acc.log), num_users * ops_per_user, "Unexpected number of logged operations")

    # Test 8: Livelock demonstration.
    # This does NOT test BankAccount directly. It demonstrates livelock:
    # threads keep retrying and remain active, but make no progress.
    def test_livelock_demo_polite_retry(self):
        lock_a = threading.Lock()
        lock_b = threading.Lock()

        # We use 3 barriers so both threads move in sync (step-by-step).
        phase1 = threading.Barrier(2)  # both threads hold their FIRST lock
        phase2 = threading.Barrier(2)  # both threads have tried the SECOND lock
        phase3 = threading.Barrier(2)  # both threads start the next attempt together

        attempts = 500

        # "progress" counts how many times a thread managed to hold BOTH locks.
        # In this demo, progress should stay 0 (active retries but no success).
        progress = {"count": 0}
        progress_lock = threading.Lock()

        def worker(first: threading.Lock, second: threading.Lock):
            for _ in range(attempts):
                # Step 1: take the first lock (each thread takes a different lock)
                first.acquire()
                try:
                    # Wait until the other thread also holds its first lock
                    phase1.wait(timeout=2)

                    # Step 2: try to take the second lock WITHOUT blocking
                    # This should fail because the other thread is holding it as its first lock.
                    got_second = second.acquire(blocking=False)

                    if got_second:
                        try:
                            # If this happens, it means progress was made (not livelock)
                            with progress_lock:
                                progress["count"] += 1
                        finally:
                            second.release()

                    # Step 3: confirm both threads have attempted the second lock
                    phase2.wait(timeout=2)

                finally:
                    # Step 4: release the first lock (back off and retry)
                    first.release()

                # Step 5: align the next retry so they keep "getting in each other's way"
                phase3.wait(timeout=2)

        # Thread 1 tries A then B, Thread 2 tries B then A
        t1 = threading.Thread(target=worker, args=(lock_a, lock_b), daemon=True)
        t2 = threading.Thread(target=worker, args=(lock_b, lock_a), daemon=True)

        t1.start()
        t2.start()
        t1.join(timeout=5)
        t2.join(timeout=5)

        # They should finish (this is not a deadlock).
        self.assertFalse(t1.is_alive() or t2.is_alive(), "Threads got stuck (unexpected blocking)")

        # In a livelock-style demo, both threads keep retrying but never succeed.
        self.assertEqual(progress["count"], 0)

        print("\n--- Test 8 Summary (Livelock Demo - Polite Retry) ---")
        print(f"Attempts per thread: {attempts}")
        print(f"Progress count (should be 0): {progress['count']}")


if __name__ == "__main__":
    unittest.main()
