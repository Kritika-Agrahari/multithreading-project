import threading
import time

class TransactionThread(threading.Thread):
    def __init__(self, thread_id, account, txn_type, amount):
        super().__init__()
        self.thread_id = thread_id
        self.account = account
        self.txn_type = txn_type
        self.amount = amount
        self.state = "NEW"

    def run(self):
        self.state = "RUNNING"
        time.sleep(2)

        if self.txn_type == "deposit":
            self.account.deposit(self.amount)
        else:
            self.account.withdraw(self.amount)

        self.state = "TERMINATED"
