from abc import ABC, abstractmethod

# Using inheritance:
 
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
    

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class PaymentProcessor_SMS(PaymentProcessor):
    @abstractmethod
    def auth_sms(self, code):
        pass

class DebitPaymentProcessor(PaymentProcessor_SMS):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False  

    def auth_sms(self, code):
        print(f'Verifying SMS code {code}')
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False  
    
    def auth_sms(self, code):
        raise Exception("Credit card payments don't support SMS code authorization.")

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaywayPaymentProcessor(PaymentProcessor_SMS):
    def __init__(self, email_address):
        self.email_address = email_address
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True 
        
    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing Payway payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("Mouse", 2, 30)
order.add_item("Charger", 2, 60)

print(order.total_price())
processor = PaywayPaymentProcessor("kvale8@gmail.com")
processor.auth_sms(423567)
processor.pay(order)

# Using Composition:

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
    
class SMSAuth:
    authorized = False

    def verify_code(self, code):
        print(f"Verifying code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: SMSAuth):
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
    def __init__(self, email_address, authorizer: SMSAuth):
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
authorizer = SMSAuth()
processor = PaywayPaymentProcessor("kvale8@gmail.com", authorizer)
authorizer.verify_code(435678)
processor.pay(order)