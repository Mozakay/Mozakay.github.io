from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): ...

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount): print(f"Processing credit card payment of ${amount}")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount): print(f"Processing PayPal payment of ${amount}")

class BankTransferPayment(PaymentStrategy):
    def pay(self, amount): print(f"Processing bank transfer payment of ${amount}")

class PaymentProcessor:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process_payment(self, amount):
        if self.strategy is None:
            raise ValueError("No payment strategy set")
        self.strategy.pay(amount)

processor = PaymentProcessor(CreditCardPayment())
processor.process_payment(100)
processor.set_strategy(PayPalPayment())
processor.process_payment(50)
