import time

class RoundRobinScheduler:
    def __init__(self, time_quantum=1):
        self.queue = []
        self.time_quantum = time_quantum
        self.context = 0
        self.gantt = []

    def add_thread(self, thread):
        thread.state = "READY"
        self.queue.append(thread)

    def run(self, update_ui):
        while self.queue:
            thread = self.queue.pop(0)

            # mark running
            thread.state = "RUNNING"

            # start once
            if not hasattr(thread, "started"):
                thread.start()
                thread.started = True

            thread.join(timeout=self.time_quantum)

            self.context += 1
            self.gantt.append(f"T{thread.thread_id}")

            # if not finished → back to queue
            if thread.is_alive():
                thread.state = "READY"
                self.queue.append(thread)
            else:
                thread.state = "TERMINATED"

            update_ui()
            time.sleep(0.8)
