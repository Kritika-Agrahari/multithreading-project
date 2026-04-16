#!/usr/bin/env python3
"""
Test script for Account-Transaction Relationship Modes
Tests: One-to-One, One-to-Many, Many-to-One relationships
"""

import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:5000"

def test_relationship_mode(mode, threads_data):
    """Test a specific relationship mode with sample transaction data"""
    print(f"\n{'='*60}")
    print(f"Testing: {mode.upper()}")
    print(f"{'='*60}")
    
    payload = {
        "algorithm": "rr",
        "quantumMs": 600,
        "initialBalance": 5000,
        "threads": threads_data,
        "relationshipMode": mode
    }
    
    print(f"📊 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(f"{API_BASE}/api/simulate", json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Success! Response Status: {response.status_code}")
        print(f"Final Balance: Rs{result.get('finalBalance', 'N/A')}")
        print(f"Completed Transactions: {result.get('completedThreads')} / {result.get('totalThreads')}")
        print(f"Context Switches: {result.get('contextSwitches')}")
        print(f"Relationship Mode (returned): {result.get('relationshipMode')}")
        
        # Show log entries
        logs = result.get('logs', [])
        print(f"\n📝 Transaction Log ({len(logs)} entries):")
        for i, log in enumerate(logs[:5], 1):  # Show first 5 logs
            print(f"  {i}. [{log['type']}] {log['message']} (Balance: Rs{log['balance']})")
        
        if len(logs) > 5:
            print(f"  ... and {len(logs) - 5} more entries")
            
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None


def main():
    print("\n" + "="*60)
    print("ACCOUNT-TRANSACTION RELATIONSHIP MODE TEST SUITE")
    print("="*60)
    print(f"Testing against: {API_BASE}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Create sample transactions
    sample_transactions = [
        {"id": 1, "type": "deposit", "amount": 500, "processingTime": 600, "priority": 1},
        {"id": 2, "type": "withdraw", "amount": 200, "processingTime": 600, "priority": 1},
        {"id": 3, "type": "deposit", "amount": 300, "processingTime": 600, "priority": 1},
        {"id": 4, "type":  "withdraw", "amount": 150, "processingTime": 600, "priority": 1},
        {"id": 5, "type": "deposit", "amount": 400, "processingTime": 600, "priority": 1},
    ]
    
    # Test each relationship mode
    results = {}
    for mode in ["one_to_one", "one_to_many", "many_to_one"]:
        result = test_relationship_mode(mode, sample_transactions)
        if result:
            results[mode] = result
    
    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY OF RESULTS")
    print(f"{'='*60}")
    
    for mode, result in results.items():
        if result:
            final_balance = result.get('finalBalance', 'N/A')
            completed = result.get('completedThreads', 0)
            total = result.get('totalThreads', 0)
            status = "✅ PASSED" if completed == total else "⚠️  PARTIAL"
            print(f"{mode:15} | Balance: Rs{final_balance:5} | {completed}/{total} txns | {status}")
    
    print(f"\n{'='*60}")
    print("Relationship Modes Explained:")
    print(f"{'='*60}")
    print("""
1️⃣  ONE-TO-ONE (1:1)
    - Constraint: Each account can accept ONLY ONE transaction
    - Behavior: First txn succeeds, subsequent txns are blocked
    - Use Case: Single authorization per account account
    
2️⃣  ONE-TO-MANY (1:M)  
    - Constraint: No limit on transactions per account
    - Behavior: All transactions execute normally
    - Use Case: Standard banking (multiple deposits/withdrawals)
    
3️⃣  MANY-TO-ONE (M:1)
    - Constraint: All transactions map to single account
    - Behavior: Same as 1:M in this single-account simulator
    - Use Case: Aggregation, pooling scenarios
    """)
    
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
