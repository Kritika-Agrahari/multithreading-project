import threading

class BankAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()
        self.log = []

    def deposit(self, amount):
        with self.lock:
            self.balance += amount
            self.log.append(f"DEPOSIT ₹{amount} → ₹{self.balance}")

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                self.log.append(f"WITHDRAW ₹{amount} → ₹{self.balance}")
            else:
                self.log.append(f"FAILED WITHDRAW ₹{amount}")
