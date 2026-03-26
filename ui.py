import tkinter as tk
from tkinter import ttk
import time
import threading

from bank_account import BankAccount
from transaction import TransactionThread

# GLOBAL ACCOUNT
account = BankAccount("ACC123", 1000)

class VisualScheduler:
    def __init__(self, root):
        self.queue = []
        self.time_quantum = 1
        self.root = root
        self.context = 0

    def add_thread(self, t):
        self.queue.append(t)
        update_queue_display()

    def run(self):
        def execute():
            while self.queue:
                thread = self.queue.pop(0)

                current_label.config(
                    text=f"Running: T{thread.thread_id} ({thread.txn_type})"
                )

                # start once
                if not hasattr(thread, "started"):
                    thread.start()
                    thread.started = True

                thread.join(timeout=self.time_quantum)

                self.context += 1
                context_label.config(text=f"Context Switches: {self.context}")

                if thread.is_alive():
                    self.queue.append(thread)

                update_queue_display()
                update_balance()
                update_log()

                time.sleep(1)

            current_label.config(text="All tasks completed ✅")

        threading.Thread(target=execute).start()


# ---------- UI FUNCTIONS ----------

def update_balance():
    balance_label.config(text=f"Balance: ₹{account.balance}")

def update_log():
    log_box.delete(1.0, tk.END)
    for entry in account.log:
        log_box.insert(tk.END, entry + "\n")

def update_queue_display():
    queue_box.delete(1.0, tk.END)
    for t in scheduler.queue:
        queue_box.insert(tk.END, f"T{t.thread_id} → {t.txn_type}\n")

def start_simulation():
    threads = [
        TransactionThread(1, account, "deposit", 500),
        TransactionThread(2, account, "withdraw", 700),
        TransactionThread(3, account, "withdraw", 300),
    ]

    for t in threads:
        scheduler.add_thread(t)

    scheduler.run()


# ---------- UI DESIGN ----------

root = tk.Tk()
root.title("💳 Banking Scheduler Simulator")
root.geometry("800x600")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("default")

# Title
title = tk.Label(root, text="Real-Time Banking Simulator",
                 font=("Arial", 20, "bold"), bg="#1e1e2f", fg="white")
title.pack(pady=10)

# Balance
balance_label = tk.Label(root, text="Balance: ₹1000",
                         font=("Arial", 14), bg="#1e1e2f", fg="#00ffcc")
balance_label.pack()

# Current Thread
current_label = tk.Label(root, text="Running: None",
                         font=("Arial", 12), bg="#1e1e2f", fg="yellow")
current_label.pack(pady=5)

# Context Switch
context_label = tk.Label(root, text="Context Switches: 0",
                         font=("Arial", 12), bg="#1e1e2f", fg="orange")
context_label.pack(pady=5)

# Frames
frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

# Queue box
queue_frame = tk.LabelFrame(frame, text="Ready Queue",
                            bg="#2a2a40", fg="white", padx=10, pady=10)
queue_frame.grid(row=0, column=0, padx=10)

queue_box = tk.Text(queue_frame, width=20, height=10)
queue_box.pack()

# Log box
log_frame = tk.LabelFrame(frame, text="Transaction Log",
                          bg="#2a2a40", fg="white", padx=10, pady=10)
log_frame.grid(row=0, column=1, padx=10)

log_box = tk.Text(log_frame, width=40, height=10)
log_box.pack()

# Button
start_btn = tk.Button(root, text="▶ Start Simulation",
                      command=start_simulation,
                      bg="#00cc99", fg="black", font=("Arial", 12, "bold"))
start_btn.pack(pady=20)

# Scheduler
scheduler = VisualScheduler(root)

root.mainloop()
