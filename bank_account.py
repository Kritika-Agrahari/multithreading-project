# bank_account.py
import threading

class BankAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()
        self.log = []

    # ✅ SAFE - with lock (Monitor)
    def deposit(self, amount):
        with self.lock:
            self.balance += amount
            self.log.append(f"DEPOSIT ₹{amount} | Balance: ₹{self.balance}")
            print(f"[{self.account_id}] ✅ Deposit ₹{amount} → Balance: ₹{self.balance}")

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                self.log.append(f"WITHDRAW ₹{amount} | Balance: ₹{self.balance}")
                print(f"[{self.account_id}] ✅ Withdraw ₹{amount} → Balance: ₹{self.balance}")
            else:
                print(f"[{self.account_id}] ❌ Insufficient funds for ₹{amount}")

    # ❌ UNSAFE - no lock (shows race condition)
    def deposit_unsafe(self, amount):
        temp = self.balance
        temp += amount
        self.balance = temp
        print(f"[UNSAFE] Deposit ₹{amount} → Balance: ₹{self.balance}")

    def print_log(self):
        print("\n📋 Transaction Log:")
        for entry in self.log:
            print(f"   → {entry}")
