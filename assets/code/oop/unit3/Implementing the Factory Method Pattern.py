from abc import ABC, abstractmethod

# 1) Car interface / abstract class
class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

# 2) Concrete car classes
class Sedan(Car):
    def drive(self):
        return "Driving a Sedan"

class SUV(Car):
    def drive(self):
        return "Driving an SUV"

class Hatchback(Car):
    def drive(self):
        return "Driving a Hatchback"
# New Concrete Product
class ElectricCar(Car):
    def drive(self):
        return "Driving an Electric Car"
    
# 3) CarFactory abstract class
class CarFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass

# 4) Concrete factories
class SedanFactory(CarFactory):
    def create_car(self):
        return Sedan()

class SUVFactory(CarFactory):
    def create_car(self):
        return SUV()

class HatchbackFactory(CarFactory):
    def create_car(self):
        return Hatchback()

# New Concrete Creator
class ElectricFactory(CarFactory):
    def create_car(self):
        return ElectricCar()

# 5) Client code 
def client_code(factory: CarFactory):
    car = factory.create_car()      
    print(car.drive())

# Demonstration
if __name__ == "__main__":
    client_code(SedanFactory())      # Output: Driving a Sedan
    client_code(SUVFactory())        # Output: Driving an SUV
    client_code(HatchbackFactory())  # Output: Driving a Hatchback
    client_code(ElectricFactory())   # Output: Driving an Electric Car
