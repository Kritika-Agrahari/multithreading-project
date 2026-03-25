# 🏦 Real-Time Multithreaded Banking Transaction Simulator

---

## 📌 Project Overview

This project simulates a real-world banking system where multiple users perform transactions like deposit and withdrawal at the same time.

The goal is to demonstrate Operating System concepts such as:
- Multithreading
- CPU Scheduling
- Synchronization
- Critical Section Problem

---

## 🎯 Problem Statement

In a banking system, multiple users may try to access and modify the same account simultaneously.

Without proper control, this can lead to:
- Incorrect account balance
- Data inconsistency
- System errors

---

## 🧠 Concepts Used

### 1. Multithreading
Multiple threads execute transactions concurrently.

### 2. Critical Section
The part of code where shared resource (bank balance) is accessed.

### 3. Race Condition
Occurs when multiple threads modify shared data at the same time.

### 4. Synchronization (to be implemented later)
Used to protect shared data using locks.

---

## 🏗️ Project Modules

| Module | Description |
|------|--------|
| Module 1 | Thread creation and lifecycle |
| Module 2 | Scheduler and CPU simulation |
| Module 3 | Synchronization and bank account |

---

## 🚀 How to Run

```bash
python main.py
