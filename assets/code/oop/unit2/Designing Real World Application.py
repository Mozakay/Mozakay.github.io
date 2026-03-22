from abc import ABC, abstractmethod
import unittest

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply_discount(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply_discount(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class FixedAmountDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply_discount(self, total: float) -> float:
        return max(total - self.amount, 0.0)


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


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"Processing credit card payment of {amount:.2f}"


class PayPalPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"Processing PayPal payment of {amount:.2f}"


class CryptoPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"Processing crypto payment of {amount:.2f}"


class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def process_payment(self, order: Order, discount_strategy: DiscountStrategy = None) -> str:
        if discount_strategy is None:
            discount_strategy = NoDiscount()

        final_total = order.calculate_discounted_total(discount_strategy)
        return self.payment_method.pay(final_total)


class TestShoppingSystem(unittest.TestCase):

    def setUp(self):
        self.book = Product("Book", 100.0)
        self.laptop = Product("Laptop", 5000.0)
        self.shirt = Product("Shirt", 200.0)

    def show_test(self, title):
        print(title)
        print("-" * 50)

    def test1_add_item(self):
        self.show_test("TEST 1: Add item to order")
        order = Order()
        order.add_item(self.book)
        print(f"Items in order: {len(order.items)}")
        print(f"First item: {order.items[0].name}")
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.items[0].name, "Book")
        print("Result: PASS")
    def tearDown(self):
        print()

    def test2_total_single_item(self):
        self.show_test("TEST 2: Calculate total for one item")
        order = Order()
        order.add_item(self.book)
        total = order.calculate_total()
        print(f"Expected total: 100.0")
        print(f"Actual total:   {total}")
        self.assertEqual(total, 100.0)
        print("Result: PASS")

    def test3_total_multiple_items(self):
        self.show_test("TEST 3: Calculate total for multiple items")
        order = Order()
        order.add_item(self.book)
        order.add_item(self.laptop)
        order.add_item(self.shirt)
        total = order.calculate_total()
        print(f"Expected total: 5300.0")
        print(f"Actual total:   {total}")
        self.assertEqual(total, 5300.0)
        print("Result: PASS")

    def test4_percentage_discount(self):
        self.show_test("TEST 4: Apply percentage discount")
        order = Order()
        order.add_item(self.book)
        order.add_item(self.shirt)
        final_total = order.calculate_discounted_total(PercentageDiscount(10))
        print(f"Original total: 300.0")
        print(f"Discounted total: {final_total}")
        self.assertEqual(final_total, 270.0)
        print("Result: PASS")

    def test5_fixed_discount(self):
        self.show_test("TEST 5: Apply fixed discount")
        order = Order()
        order.add_item(self.book)
        order.add_item(self.shirt)
        final_total = order.calculate_discounted_total(FixedAmountDiscount(50))
        print(f"Original total: 300.0")
        print(f"Discounted total: {final_total}")
        self.assertEqual(final_total, 250.0)
        print("Result: PASS")

    def test6_credit_payment(self):
        self.show_test("TEST 6: Credit card payment")
        order = Order()
        order.add_item(self.book)
        processor = PaymentProcessor(CreditCardPayment())
        result = processor.process_payment(order)
        print(f"Payment output: {result}")
        self.assertEqual(result, "Processing credit card payment of 100.00")
        print("Result: PASS")

    def test7_paypal_with_discount(self):
        self.show_test("TEST 7: PayPal payment after discount")
        order = Order()
        order.add_item(self.book)
        order.add_item(self.shirt)
        processor = PaymentProcessor(PayPalPayment())
        result = processor.process_payment(order, PercentageDiscount(10))
        print(f"Payment output: {result}")
        self.assertEqual(result, "Processing PayPal payment of 270.00")
        print("Result: PASS")

    def test8_new_payment_method(self):
        self.show_test("TEST 8: Add new payment method without modifying processor")

        class ApplePayPayment(PaymentMethod):
            def pay(self, amount: float) -> str:
                return f"Processing Apple Pay payment of {amount:.2f}"

        order = Order()
        order.add_item(self.book)
        processor = PaymentProcessor(ApplePayPayment())
        result = processor.process_payment(order)
        print(f"Payment output: {result}")
        self.assertEqual(result, "Processing Apple Pay payment of 100.00")
        print("Result: PASS")

    def test90_new_discount_strategy(self):
        self.show_test("TEST 9: Add new discount strategy without modifying order")

        class SeasonalDiscount(DiscountStrategy):
            def apply_discount(self, total: float) -> float:
                return total * 0.80

        order = Order()
        order.add_item(self.book)
        order.add_item(self.shirt)
        final_total = order.calculate_discounted_total(SeasonalDiscount())
        print(f"Discounted total: {final_total}")
        self.assertEqual(final_total, 240.0)
        print("Result: PASS")
    
    def test910_no_discount(self):
        self.show_test("TEST 10: No discount")
        order = Order()
        order.add_item(self.book)
        total = order.calculate_discounted_total(NoDiscount())
        print(f"Total without discount: {total}")
        self.assertEqual(total, 100.0)
        print("Result: PASS")

    def test911_discount_not_below_zero(self):
        self.show_test("TEST 11: Discount should not reduce total below zero")
        order = Order()
        order.add_item(self.book)
        final_total = order.calculate_discounted_total(FixedAmountDiscount(500))
        print(f"Discounted total: {final_total}")
        self.assertEqual(final_total, 0.0)
        print("Result: PASS")

    def test912_crypto_payment_substitutes_payment_method(self):
        self.show_test("TEST 12: CryptoPayment can replace PaymentMethod")
        order = Order()
        order.add_item(self.book)
        processor = PaymentProcessor(CryptoPayment())
        result = processor.process_payment(order)
        print(f"Payment output: {result}")
        self.assertEqual(result, "Processing crypto payment of 100.00")
        print("Result: PASS")

if __name__ == "__main__":
    unittest.main(verbosity=0)