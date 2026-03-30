from abc import ABC, abstractmethod

# Named constants
BOOK_DISCOUNT = 0.9
ELECTRONICS_DISCOUNT = 0.8
NO_DISCOUNT = 1.0

# Strategy interface
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price):
        pass

# Concrete strategies
class BookDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * BOOK_DISCOUNT

class ElectronicsDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * ELECTRONICS_DISCOUNT

class NoDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * NO_DISCOUNT

# Strategy selector
def get_discount_strategy(item_type):
    if item_type == "book":
        return BookDiscount()
    elif item_type == "electronics":
        return ElectronicsDiscount()
    else:
        return NoDiscount()

# Refactored function
def calculate_total_price(items):
    total = 0
    for item in items:
        strategy = get_discount_strategy(item["type"])
        total += strategy.apply_discount(item["price"])
    return total

# Example usage
items = [
    {"type": "book", "price": 100},
    {"type": "electronics", "price": 200},
    {"type": "clothing", "price": 50}
]

print(calculate_total_price(items))