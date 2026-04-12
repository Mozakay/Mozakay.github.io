import random
import threading
import time

from abc import ABC, abstractmethod
from typing import List, Tuple


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

# Abstract operation used by TransactionSimulator.
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
        self._log = []  # stores tuples like ("deposit", amount)
        self._log_lock = threading.Lock()

    @property
    def account_number(self) -> int:
        return self._wrapped.account_number

    def _record(self, action: str, amount: float, status: str) -> None:
        if self._enabled:
            entry = (threading.current_thread().name, action, round(float(amount), 2), status)
            with self._log_lock:
                self._log.append(entry)

    def get_log(self) -> List[tuple]:
        with self._log_lock:
            return list(self._log)

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
