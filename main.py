"""
Real-Time Multithreaded Banking Transaction Processing Simulator
================================================================
main.py — Integration entry point

Demonstrates:
  1. Thread lifecycle with Round Robin scheduling
  2. Synchronization: safe vs unsafe bank account
  3. Thread mapping models: Many-to-One, One-to-One, Many-to-Many

Run:  python main.py
"""

from bank_account import BankAccount
from transaction_thread import TransactionThread
from scheduler import RoundRobinScheduler
from synchronization import run_all_sync_demos
from thread_models import compare_models


def demo_scheduler():
    """
    PART 1: Thread lifecycle + Round Robin scheduling demo.
    Creates 5 transactions, runs them through the scheduler,
    and prints the Gantt chart and metrics.
    """
    print("\n" + "#"*60)
    print("  PART 1: Round Robin Scheduler + Thread Lifecycle")
    print("#"*60)

    account = BankAccount("ACC001", balance=5000)

    transactions = [
        TransactionThread(1, account, "deposit",  1000, processing_time=1.5),
        TransactionThread(2, account, "withdraw",  500, processing_time=1.0),
        TransactionThread(3, account, "deposit",  2000, processing_time=2.0),
        TransactionThread(4, account, "withdraw", 1500, processing_time=0.8),
        TransactionThread(5, account, "deposit",   300, processing_time=1.2),
    ]

    scheduler = RoundRobinScheduler(time_quantum=1)

    print("\n  Adding transactions to scheduler queue...")
    for t in transactions:
        scheduler.add_thread(t)

    print("\n  Starting scheduler...")
    scheduler.run()

    # Print results
    scheduler.print_metrics()
    account.print_log()


def demo_synchronization():
    """
    PART 2: Safe vs Unsafe bank account demo.
    Shows race condition without lock vs correct result with lock.
    """
    print("\n" + "#"*60)
    print("  PART 2: Synchronization — Race Condition Demo")
    print("#"*60)

    run_all_sync_demos()


def demo_thread_models():
    """
    PART 3: Compare all three thread mapping models.
    Runs the same 5 transactions under each model and compares timing.
    """
    print("\n" + "#"*60)
    print("  PART 3: Thread Mapping Models — Performance Comparison")
    print("#"*60)

    transaction_data = [
        ("deposit",  500),
        ("withdraw", 200),
        ("deposit",  800),
        ("withdraw", 300),
        ("deposit",  100),
    ]

    compare_models(BankAccount, transaction_data)


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  BANKING TRANSACTION PROCESSING SIMULATOR")
    print("  OS Concepts: Threads | Scheduling | Synchronization")
    print("="*60)

    demo_scheduler()
    demo_synchronization()
    demo_thread_models()

    print("\n" + "="*60)
    print("  Simulation complete.")
    print("="*60)
