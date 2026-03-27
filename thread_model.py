import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
 
 
# ─────────────────────────────────────────────────────────────
#  THREAD MAPPING MODELS
#  Demonstrates how user-level threads map to kernel threads.
#
#  All three models run the same set of TransactionThreads —
#  the difference is HOW they are executed and with what level
#  of parallelism.
# ─────────────────────────────────────────────────────────────
 
 
class ManyToOneModel:
    """
    MANY-TO-ONE MODEL
    -----------------
    All user threads map to a SINGLE kernel thread (worker).
    Only one transaction executes at a time — no parallelism.
    
    Real-world analogy: One bank teller serving all customers
    one by one, no matter how many are waiting.
    
    Pros : Simple, no race conditions even without locks
    Cons : Slow — all transactions are sequential
    """
 
    def __init__(self):
        self.model_name = "Many-to-One"
        self.results = []
 
    def run_transactions(self, transactions):
        """
        Uses a thread pool with max_workers=1.
        All transactions are submitted but only one runs at a time.
        """
        print(f"\n{'='*50}")
        print(f"  MODEL: {self.model_name}")
        print(f"  Workers: 1  |  Transactions: {len(transactions)}")
        print(f"{'='*50}")
 
        start_time = time.time()
 
        with ThreadPoolExecutor(max_workers=1) as executor:
            # Submit all transaction run() methods to the single worker
            futures = {executor.submit(t.run): t for t in transactions}
 
            for future in as_completed(futures):
                t = futures[future]
                try:
                    future.result()
                    print(f"  [DONE] Thread {t.thread_id} | {t.txn_type} ₹{t.amount}")
                except Exception as e:
                    print(f"  [ERROR] Thread {t.thread_id}: {e}")
 
        elapsed = time.time() - start_time
        print(f"\n  Total time: {elapsed:.2f}s  |  Context: Sequential (1 worker)")
        return elapsed
 
 
class OneToOneModel:
    """
    ONE-TO-ONE MODEL
    ----------------
    Each user thread maps directly to one kernel thread.
    This is what Python's threading.Thread does by default.
    All transactions can run truly in parallel (on separate CPU cores).
    
    Real-world analogy: Each customer gets their own dedicated teller.
    
    Pros : True parallelism — fastest for independent tasks
    Cons : High memory overhead for large numbers of threads
    """
 
    def __init__(self):
        self.model_name = "One-to-One"
        self.results = []
 
    def run_transactions(self, transactions):
        """
        Starts each TransactionThread directly using thread.start().
        Each maps to its own OS-level thread.
        """
        print(f"\n{'='*50}")
        print(f"  MODEL: {self.model_name}")
        print(f"  Workers: {len(transactions)} (one per transaction)")
        print(f"  Transactions: {len(transactions)}")
        print(f"{'='*50}")
 
        start_time = time.time()
 
        # Start all threads simultaneously
        for t in transactions:
            t.start()
            print(f"  [STARTED] Thread {t.thread_id} | {t.txn_type} ₹{t.amount}")
 
        # Wait for all to complete
        for t in transactions:
            t.join()
            print(f"  [DONE]    Thread {t.thread_id} | {t.txn_type} ₹{t.amount}")
 
        elapsed = time.time() - start_time
        print(f"\n  Total time: {elapsed:.2f}s  |  Context: Parallel ({len(transactions)} workers)")
        return elapsed
 
 
class ManyToManyModel:
    """
    MANY-TO-MANY MODEL
    ------------------
    N user threads are multiplexed over M kernel threads, where M <= N.
    The pool manages which thread gets CPU time.
    
    Real-world analogy: 10 customers served by 3 tellers.
    When a teller finishes, they call the next customer.
    
    Pros : Balanced — good parallelism without thread explosion
    Cons : Slightly more complex coordination
    
    This is the most realistic model for production banking systems.
    """
 
    def __init__(self, num_workers=3):
        self.model_name = "Many-to-Many"
        self.num_workers = num_workers
        self.results = []
 
    def run_transactions(self, transactions):
        """
        Uses a thread pool with num_workers workers to handle
        all transactions. Worker threads are reused across jobs.
        """
        print(f"\n{'='*50}")
        print(f"  MODEL: {self.model_name}")
        print(f"  Workers: {self.num_workers}  |  Transactions: {len(transactions)}")
        print(f"{'='*50}")
 
        start_time = time.time()
 
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = {executor.submit(t.run): t for t in transactions}
 
            for future in as_completed(futures):
                t = futures[future]
                try:
                    future.result()
                    print(f"  [DONE] Thread {t.thread_id} | {t.txn_type} ₹{t.amount}")
                except Exception as e:
                    print(f"  [ERROR] Thread {t.thread_id}: {e}")
 
        elapsed = time.time() - start_time
        print(f"\n  Total time: {elapsed:.2f}s  |  Context: {self.num_workers} workers pooled")
        return elapsed
 
 
# ─────────────────────────────────────────────────────────────
#  COMPARISON RUNNER
#  Run all 3 models with the same transactions and compare times.
# ─────────────────────────────────────────────────────────────
 
def compare_models(account_class, transaction_data):
    """
    Runs the same set of transactions under all three models
    and prints a side-by-side performance comparison.
 
    Args:
        account_class : The BankAccount class to instantiate
        transaction_data : List of (txn_type, amount) tuples
    """
    from transaction_thread import TransactionThread
 
    results = {}
 
    models = [
        ("Many-to-One",  ManyToOneModel()),
        ("One-to-One",   OneToOneModel()),
        ("Many-to-Many", ManyToManyModel(num_workers=3)),
    ]
 
    for name, model in models:
        # Fresh account for each model so balances don't mix
        account = account_class("COMPARE", 1000)
 
        # Rebuild threads (can't reuse — threads can only start once)
        threads = [
            TransactionThread(i + 1, account, txn_type, amount, processing_time=1)
            for i, (txn_type, amount) in enumerate(transaction_data)
        ]
 
        elapsed = model.run_transactions(threads)
        results[name] = {
            "time": elapsed,
            "final_balance": account.balance,
        }
 
    # ── Print comparison table ──
    print(f"\n{'='*50}")
    print("  PERFORMANCE COMPARISON")
    print(f"{'='*50}")
    print(f"  {'Model':<20} {'Time (s)':<12} {'Final Balance'}")
    print(f"  {'-'*46}")
    for name, r in results.items():
        print(f"  {name:<20} {r['time']:<12.2f} ₹{r['final_balance']}")
    print(f"{'='*50}\n")
