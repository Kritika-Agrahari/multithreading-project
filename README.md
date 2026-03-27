🏦 **Real-Time Multithreaded Banking Transaction Simulator**

---

## 📌 Project Overview

This project simulates a real-world banking system where multiple users perform transactions (deposit and withdrawal) concurrently.

It demonstrates key **Operating System concepts** such as multithreading, CPU scheduling, synchronization, and thread lifecycle using an interactive GUI.

---

## 🎯 Problem Statement

In a banking system, multiple users may try to access and modify the same account simultaneously.

Without proper synchronization, this can lead to:

* Incorrect account balance
* Race conditions
* Data inconsistency

This project solves these issues using thread synchronization and controlled scheduling.

---

## 🧠 Concepts Used

### 1. Multithreading

Multiple threads simulate concurrent user transactions.

### 2. CPU Scheduling (Round Robin)

Threads are executed using a **Round Robin scheduling algorithm** with a fixed time quantum.

### 3. Thread Lifecycle

Each thread transitions through states:

```
NEW → READY → RUNNING → TERMINATED
```

### 4. Critical Section

The shared bank balance is a critical resource accessed by multiple threads.

### 5. Synchronization (Mutex Lock)

A lock is used to ensure only one thread modifies the balance at a time, preventing race conditions.

---

## 🏗️ Project Modules

| Module              | Description                                     |
| ------------------- | ----------------------------------------------- |
| Bank Account        | Handles balance operations with synchronization |
| Transaction Threads | Represents concurrent transactions              |
| Scheduler           | Implements Round Robin scheduling               |
| GUI                 | Visualizes queue, states, logs, and execution   |
| Gantt Chart         | Displays execution timeline                     |

---

## 🎨 Features

* ✅ Multithreaded transaction processing
* ✅ Round Robin scheduling simulation
* ✅ Thread state visualization
* ✅ Gantt chart (execution timeline)
* ✅ Synchronization using locks
* ✅ Real-time GUI updates
* ✅ Context switch tracking

---

## 🖥️ GUI Components

* 💰 Account Balance Display
* 📋 Transaction Log
* 🔄 Ready Queue
* 🧠 Thread States
* 📊 Gantt Chart
* 🔁 Context Switch Counter

---

## 🚀 How to Run

1. Open terminal in project folder
2. Run:

```bash
python ui_final.py
```

3. Click **Start Simulation** in the GUI

---

## 📊 Sample Output

* Balance updates after each transaction
* Threads executed in cyclic order
* Gantt chart shows execution sequence
* Context switches increase dynamically

---

## 🧠 Conclusion

This project successfully demonstrates how operating systems handle concurrent processes, manage CPU scheduling, and ensure data consistency using synchronization.

---

## 🔮 Future Enhancements

* User input for custom transactions
* Deadlock detection visualization
* Multiple scheduling algorithms (FCFS, Priority)
* Web-based interface

---
