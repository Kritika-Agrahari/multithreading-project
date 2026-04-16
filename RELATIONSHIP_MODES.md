# Account-Transaction Relationship Modes Implementation

## ✅ Status Summary

**Backend**: Fully implemented and tested ✅
**Frontend**: UI controls added, JavaScript functions added, needs final integration

---

## 🎯 Features Implemented

### 1. **Backend API Updates** (backend_server.py)
- ✅ Updated `/api/simulate` endpoint to accept `relationshipMode` parameter
- ✅ Modified `_simulate_round_robin()` function to respect relationship constraints
- ✅ Modified `_simulate_priority()` function to respect relationship constraints
- ✅ Response includes `relationshipMode` field for confirmation

### 2. **Frontend UI Updates** (ui_final.html)
- ✅ Added relationship selector buttons (1-to-1, 1-to-Many, M-to-1)
- ✅ Added relationship mode description text
- ✅ Added JavaScript state variable `relationshipMode`
- ✅ Added `selectRelationship()` function to handle button clicks

### 3. **Test Suite** (test_relationships.py)
- ✅ Validates all three relationship modes
- ✅ Confirms constraints are properly enforced
- ✅ Provides clear output showing transaction blocking behavior

---

## 📊 Relationship Modes Explained

### 1️⃣ ONE-TO-ONE (1:1) Relationship
**Constraint**: Each account can accept ONLY ONE transaction
- First transaction executes normally
- All subsequent transactions are BLOCKED
- Final balance reflects only the first transaction
- **Use Case**: Single authorization per account, one-time transactions

**Test Result**:
```
Initial: Rs5000
1. DEPOSIT Rs500 → Rs5500 ✅
2. WITHDRAW Rs200 → BLOCKED ❌
3. DEPOSIT Rs300 → BLOCKED ❌
4. WITHDRAW Rs150 → BLOCKED ❌
5. DEPOSIT Rs400 → BLOCKED ❌
Final: Rs5500
```

### 2️⃣ ONE-TO-MANY (1:M) Relationship [DEFAULT]
**Constraint**: No limit on transactions per account
- All transactions execute in order
- Full concurrency and scheduling supported
- Standard banking behavior
- **Use Case**: Normal banking operations (multiple deposits/withdrawals)

**Test Result**:
```
Initial: Rs5000
1. DEPOSIT Rs500 → Rs5500 ✅
2. WITHDRAW Rs200 → Rs5300 ✅
3. DEPOSIT Rs300 → Rs5600 ✅
4. WITHDRAW Rs150 → Rs5450 ✅
5. DEPOSIT Rs400 → Rs5850 ✅
Final: Rs5850
```

### 3️⃣ MANY-TO-ONE (M:1) Relationship
**Constraint**: All transactions map to single account
- In this single-account simulator, behaves like 1:M
- All transactions execute normally
- Useful for aggregation/pooling scenarios
- **Use Case**: Multi-source transactions to single target account

**Test Result**:
```
Initial: Rs5000
1. DEPOSIT Rs500 → Rs5500 ✅
2. WITHDRAW Rs200 → Rs5300 ✅
3. DEPOSIT Rs300 → Rs5600 ✅
4. WITHDRAW Rs150 → Rs5450 ✅
5. DEPOSIT Rs400 → Rs5850 ✅
Final: Rs5850
```

---

## 🔧 Frontend Integration Steps

### Step 1: Update the startSimulation() function
Locate the `fetch()` call to `/api/simulate` and add `relationshipMode` to the payload:

```javascript
// Find this section in startSimulation():
const payload = {
  algorithm: selectedAlgorithm,
  quantumMs: quantum,
  initialBalance: initBalance,
  threads: threads
  // ADD THIS LINE:
  relationshipMode: relationshipMode
};
```

### Step 2: Verify HTML buttons are wired up
The buttons should already be in the HTML (lines 1123-1135):
```html
<button id="rel-one-to-one" class="btn btn-sm" onclick="selectRelationship('one_to_one')">1-to-1</button>
<button id="rel-one-to-many" class="btn btn-sm active" onclick="selectRelationship('one_to_many')">1-to-M</button>
<button id="rel-many-to-one" class="btn btn-sm" onclick="selectRelationship('many_to_one')">M-to-1</button>
```

### Step 3: Verify JavaScript functions
Check that these functions exist in the script section:
- `let relationshipMode = 'one_to_many';` (state variable)
- `function selectRelationship(mode) { ... }` (button handler)

---

## 📝 API Payload Example

### Request
```json
{
  "algorithm": "rr",
  "quantumMs": 600,
  "initialBalance": 5000,
  "threads": [...],
  "relationshipMode": "one_to_one"
}
```

### Response
```json
{
  "ok": true,
  "algorithm": "rr",
  "finalBalance": 5500,
  "completedThreads": 1,
  "totalThreads": 5,
  "contextSwitches": 5,
  "relationshipMode": "one_to_one",
  "logs": [
    {"type": "deposit", "message": "DEPOSIT Rs500", "balance": 5500},
    {"type": "sys", "message": "TXN BLOCKED (one-to-one constraint)", "balance": 5500},
    ...
  ],
  "slices": [...]
}
```

---

## ✅ Testing Commands

### Test all relationship modes:
```bash
cd real-time-banking-thread-simulator
python test_relationships.py
```

### Test specific mode with curl:
```bash
curl -X POST http://127.0.0.1:5000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "rr",
    "quantumMs": 600,
    "initialBalance": 5000,
    "threads": [{"id": 1, "type": "deposit", "amount": 500, "processingTime": 600}],
    "relationshipMode": "one_to_one"
  }'
```

---

## 🎨 UI Visual Feedback

The UI now includes:
1. **Three toggle buttons** for selecting relationship mode (1-to-1, 1-to-M, M-to-1)
2. **Active button highlighting** (blue glow on selected mode)
3. **Description text** that updates based on selected mode:
   - 1-to-1: "One account accepts only one transaction"
   - 1-to-Many: "One account accepts multiple transactions"
   - M-to-1: "Many transactions map to single account"
4. **Log messages** showing relationship mode in effect

---

## 🚀 Runtime Behavior

### When running with ONE-TO-ONE mode:
- First transaction in queue executes fully
- All remaining transactions see "TXN BLOCKED (one-to-one constraint)" message
- Blocks persist until simulation ends
- Useful for demonstrating mutual exclusion and synchronization concepts

### When running with ONE-TO-MANY or MANY-TO-ONE:
- All transactions execute normally in scheduled order
- Standard banking simulator behavior
- Demonstrates lock-based synchronization with multiple operations

---

## 📚 Files Modified/Created

1. **backend_server.py** - Updated API endpoint and simulation functions
2. **ui_final.html** - Added relationship selector UI and JavaScript
3. **test_relationships.py** - NEW: Comprehensive test suite
4. **ui_relationship_patch.js** - NEW: Documentation of JavaScript integration
5. **RELATIONSHIP_MODES.md** - NEW: This documentation

---

## 🔮 Future Enhancements

Potential improvements for multi-account scenarios:
- Support for multiple accounts with different relationships
- Per-account relationship configuration
- Dynamic relationship mode switching during simulation
- Visualization of relationship constraints in Gantt chart
- Statistics on blocked vs executed transactions

---

## ❓ FAQ

**Q: How does one-to-one constraint enforce "one" transaction?**
A: After first transaction executes (remaining_ms becomes 0), the account_txn_count[balance] > 0 check blocks all subsequent transactions.

**Q: Why do one-to-many and many-to-one behave the same?**
A: In this single-account simulator, they represent the same behavior. Many-to-one is more relevant in multi-account scenarios.

**Q: Can I change relationship mode during simulation?**
A: Currently no - it's set at simulation start time. Future enhancement could allow dynamic switching.

**Q: How are blocked transactions shown?**
A: They appear in the logs as "TXN BLOCKED (one-to-one constraint)" with log type "sys".

---

Generated: 2026-04-15
Status: Ready for Frontend Integration & Testing
