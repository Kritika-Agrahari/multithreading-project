import time
 
 
class RoundRobinScheduler:
    """
    Simulates CPU scheduling using the Round Robin algorithm.
 
    Each thread gets a fixed time slice (time_quantum seconds).
    If it doesn't finish in time, it goes back to the end of
    the ready queue and waits its turn again.
 
    The scheduler is the SOLE owner of all thread state changes.
    TransactionThread.run() must NOT set self.state.
    """
 
    def __init__(self, time_quantum=1):
        self.queue = []                 # ready queue
        self.time_quantum = time_quantum
        self.context_switches = 0       # tracks CPU context switches
        self.gantt = []                 # records execution order: ["T1","T2","T1",...]
        self.metrics = {
            "total_threads"    : 0,
            "completed_threads": 0,
            "total_wait_time"  : 0.0,
            "start_time"       : None,
            "end_time"         : None,
        }
 
    def add_thread(self, thread):
        """Add a TransactionThread to the ready queue."""
        thread.state = "READY"
        self.queue.append(thread)
        self.metrics["total_threads"] += 1
        print(f"  [SCHEDULER] Thread {thread.thread_id} added to queue → state: READY")
 
    def run(self, update_ui=None):
        """
        Main Round Robin loop.
        Runs until all threads in the queue are TERMINATED.
        
        update_ui: optional callback called after each time slice
                   (used for GUI updates or console refreshes)
        """
        if not self.queue:
            print("  [SCHEDULER] Queue is empty — nothing to run.")
            return
 
        self.metrics["start_time"] = time.time()
        print(f"\n  [SCHEDULER] Starting Round Robin | quantum={self.time_quantum}s")
        print(f"  [SCHEDULER] Threads in queue: {len(self.queue)}")
        print(f"  {'─'*50}")
 
        while self.queue:
            thread = self.queue.pop(0)  # take from front of queue
 
            # ── Mark RUNNING (scheduler sets state) ──
            thread.state = "RUNNING"
            print(f"\n  [CPU] Running Thread {thread.thread_id}"
                  f" ({thread.txn_type} ₹{thread.amount}) | state: RUNNING")
 
            # ── Start the thread once ──
            if not hasattr(thread, "_started_flag"):
                thread.start()
                thread._started_flag = True
                thread._enqueue_time = time.time()
 
            # ── Give thread its time quantum ──
            thread.join(timeout=self.time_quantum)
            self.context_switches += 1
            self.gantt.append(f"T{thread.thread_id}")
 
            # ── Check if done or needs re-queuing ──
            if thread.is_alive():
                # Not finished — send back to end of queue (READY)
                thread.state = "READY"
                self.queue.append(thread)
                print(f"  [SCHEDULER] Thread {thread.thread_id} not done"
                      f" → re-queued | state: READY")
            else:
                # Finished — terminate
                thread.state = "TERMINATED"
                self.metrics["completed_threads"] += 1
                wait = time.time() - thread._enqueue_time
                self.metrics["total_wait_time"] += wait
                print(f"  [SCHEDULER] Thread {thread.thread_id} TERMINATED"
                      f" | wait time: {wait:.2f}s")
 
            # ── Optional UI callback ──
            if update_ui:
                update_ui()
 
            time.sleep(0.1)  # small pause for readability in console output
 
        self.metrics["end_time"] = time.time()
        print(f"\n  {'─'*50}")
        print(f"  [SCHEDULER] All threads completed.")
 
    def get_metrics(self):
        """
        Returns a dictionary of scheduling performance metrics.
        Call this after run() completes.
        """
        total_time = 0.0
        if self.metrics["start_time"] and self.metrics["end_time"]:
            total_time = self.metrics["end_time"] - self.metrics["start_time"]
 
        completed = self.metrics["completed_threads"]
        avg_wait = (self.metrics["total_wait_time"] / completed) if completed > 0 else 0.0
 
        return {
            "total_threads"     : self.metrics["total_threads"],
            "completed_threads" : completed,
            "context_switches"  : self.context_switches,
            "gantt_chart"       : " | ".join(self.gantt),
            "total_time_sec"    : round(total_time, 2),
            "avg_wait_time_sec" : round(avg_wait, 2),
            "cpu_utilization"   : f"{min(100, (total_time - 0.1 * len(self.gantt)) / total_time * 100):.1f}%" if total_time > 0 else "N/A",
        }
 
    def print_metrics(self):
        """Print a formatted summary of all scheduling metrics."""
        m = self.get_metrics()
        print(f"\n  {'='*50}")
        print(f"  SCHEDULER METRICS")
        print(f"  {'='*50}")
        print(f"  Total threads      : {m['total_threads']}")
        print(f"  Completed threads  : {m['completed_threads']}")
        print(f"  Context switches   : {m['context_switches']}")
        print(f"  Total time         : {m['total_time_sec']}s")
        print(f"  Avg wait time      : {m['avg_wait_time_sec']}s")
        print(f"  CPU utilization    : {m['cpu_utilization']}")
        print(f"  Gantt chart        : {m['gantt_chart']}")
        print(f"  {'='*50}\n")
