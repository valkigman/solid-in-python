from abc import ABC, abstractmethod

class Order:
    items = []
    quantities = []
    prices = []
    status = 'open'

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total
    
class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

class SMSAuth(Authorizer):
    authorized = False

    def verify_code(self, code):
        print(f"Verifying code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized
    
class NotARobot(Authorizer):
    authorized = False

    def not_a_robot(self):
        print("Are you a robot? Nope")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: Authorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not uthorised")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaywayPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address, authorizer: Authorizer):
        self.email_address = email_address
        self.authorizer = authorizer
        
    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not uthorised")
        print("Processing Payway payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("Mouse", 2, 30)
order.add_item("Charger", 2, 60)

print(order.total_price())
authorizer = NotARobot()
processor = PaywayPaymentProcessor("kvale8@gmail.com", authorizer)
authorizer.not_a_robot()
processor.pay(order)