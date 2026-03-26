# scheduler.py
import time
from bank_account import BankAccount
from transaction import TransactionThread

class RoundRobinScheduler:
    def __init__(self, time_quantum=1):
        self.queue = []
        self.time_quantum = time_quantum
        self.context_switches = 0

    def add_thread(self, thread):
        self.queue.append(thread)
        print(f"[Scheduler] Thread {thread.thread_id} added to Ready Queue")

    def run(self):
        print("\n⚙️  Scheduler Starting...\n")
        while self.queue:
            thread = self.queue.pop(0)      # Take first thread

            print(f"[CPU] ▶ Executing Thread {thread.thread_id} "
                  f"({thread.txn_type} ₹{thread.amount})")

            thread.start()
            thread.join(timeout=self.time_quantum)  # Run for time quantum

            self.context_switches += 1
            print(f"[CPU] ↔ Context Switch #{self.context_switches}\n")
            time.sleep(0.2)

        print(f"\n✅ All threads executed.")
        print(f"📊 Total Context Switches: {self.context_switches}")


def main():
    account = BankAccount("ACC123", 1000)

    threads = [
        TransactionThread(1, account, "deposit", 500),
        TransactionThread(2, account, "withdraw", 700),
        TransactionThread(3, account, "withdraw", 300),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("Final Balance:", account.balance)


if __name__ == "__main__":
    main()
