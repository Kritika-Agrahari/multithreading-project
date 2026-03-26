import tkinter as tk
import threading

from bank_account import BankAccount
from transaction import TransactionThread
from scheduler import RoundRobinScheduler

account = BankAccount("ACC123", 1000)
scheduler = RoundRobinScheduler(1)

# ---------- UI FUNCTIONS ----------

def start_simulation():
    threads = [
        TransactionThread(1, account, "deposit", 500),
        TransactionThread(2, account, "withdraw", 700),
        TransactionThread(3, account, "withdraw", 300),
    ]

    for t in threads:
        scheduler.add_thread(t)

    threading.Thread(target=lambda: scheduler.run(update_ui)).start()

def update_ui():
    update_balance()
    update_log()
    update_queue()
    update_states()
    draw_gantt()
    update_metrics()

def update_balance():
    balance_label.config(text=f"Balance: ₹{account.balance}")

def update_log():
    log_box.delete(1.0, tk.END)
    for entry in account.log:
        log_box.insert(tk.END, entry + "\n")

def update_queue():
    queue_box.delete(1.0, tk.END)
    for t in scheduler.queue:
        queue_box.insert(tk.END, f"T{t.thread_id}\n")

def update_states():
    state_box.delete(1.0, tk.END)
    for t in scheduler.queue:
        state_box.insert(tk.END, f"T{t.thread_id}: {t.state}\n")

def draw_gantt():
    canvas.delete("all")
    x = 10
    for t in scheduler.gantt:
        canvas.create_rectangle(x, 20, x+50, 70, fill="skyblue")
        canvas.create_text(x+25, 45, text=t)
        x += 60

def update_metrics():
    metrics_label.config(
        text=f"Context Switches: {scheduler.context}"
    )

# ---------- UI DESIGN ----------

root = tk.Tk()
root.title("💳 Advanced Banking Simulator")
root.geometry("900x700")
root.configure(bg="#1e1e2f")

title = tk.Label(root, text="Real-Time Banking Simulator",
                 font=("Arial", 20, "bold"), bg="#1e1e2f", fg="white")
title.pack(pady=10)

balance_label = tk.Label(root, text="Balance: ₹1000",
                         font=("Arial", 14), bg="#1e1e2f", fg="#00ffcc")
balance_label.pack()

metrics_label = tk.Label(root, text="Context Switches: 0",
                         font=("Arial", 12), bg="#1e1e2f", fg="orange")
metrics_label.pack()

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

# Queue
queue_box = tk.Text(frame, width=20, height=10)
queue_box.grid(row=0, column=0, padx=10)

# Log
log_box = tk.Text(frame, width=40, height=10)
log_box.grid(row=0, column=1, padx=10)

# States
state_box = tk.Text(root, height=5, width=50)
state_box.pack(pady=10)

# Gantt Chart
canvas = tk.Canvas(root, width=700, height=100, bg="white")
canvas.pack(pady=10)

# Button
btn = tk.Button(root, text="▶ Start Simulation",
                command=start_simulation,
                bg="#00cc99", font=("Arial", 12, "bold"))
btn.pack(pady=20)

root.mainloop()
