import threading
import time
 
 
class TransactionThread(threading.Thread):
    """
    Represents a single bank transaction as a thread.
    Each deposit or withdrawal becomes one TransactionThread.
 
    IMPORTANT: This class does NOT set self.state anywhere.
    The scheduler is the sole owner of all state transitions.
    """
 
    def __init__(self, thread_id, account, txn_type, amount, processing_time=2):
        super().__init__()
        self.thread_id = thread_id
        self.account = account
        self.txn_type = txn_type          # "deposit" or "withdraw"
        self.amount = amount
        self.processing_time = processing_time  # simulates real-world processing delay
        self.state = "NEW"                # initial state — scheduler will move it forward
        self.daemon = True                # thread dies if main program exits
 
    def run(self):
        """
        Core execution logic.
        Called by thread.start() — do NOT call directly.
        State is managed externally by the scheduler.
        """
        time.sleep(self.processing_time)   # simulate processing time
 
        if self.txn_type == "deposit":
            self.account.deposit(self.amount)
        elif self.txn_type == "withdraw":
            self.account.withdraw(self.amount)
        else:
            print(f"[Thread {self.thread_id}] Unknown transaction type: {self.txn_type}")
 
    def __repr__(self):
        return f"Thread(id={self.thread_id}, type={self.txn_type}, amount={self.amount}, state={self.state})"
