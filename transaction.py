import threading
import time

class TransactionThread(threading.Thread):
    def __init__(self, thread_id, account, txn_type, amount):
        super().__init__()
        self.thread_id = thread_id
        self.account = account
        self.txn_type = txn_type
        self.amount = amount

    def run(self):
        print(f"[Thread {self.thread_id}] Started")

        # ⏳ simulate execution time
        time.sleep(2)

        if self.txn_type == "deposit":
            self.account.deposit(self.amount)
        elif self.txn_type == "withdraw":
            self.account.withdraw(self.amount)

        print(f"[Thread {self.thread_id}] Finished")
