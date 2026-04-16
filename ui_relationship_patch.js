// Relationship Mode JavaScript Patch
// This patch should be injected into the ui_final.html to support account-transaction relationships

// State variable - should already exist from earlier insertion
// let relationshipMode = 'one_to_many';

// Button click handler for relationship mode selection
function selectRelationship(mode) {
  relationshipMode = mode;
  
  // Update button states
  ['one_to_one', 'one_to_many', 'many_to_one'].forEach(m => {
    const btnId = `rel-${m.replace(/_/g, '-')}`;
    const btn = document.getElementById(btnId);
    if(btn) {
      if(m === mode) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    }
  });
  
  // Update description text
  const descMap = {
    'one_to_one': '1-to-1: Each account can only accept one transaction (constraint: max 1 txn per account)',
    'one_to_many': '1-to-Many: One account accepts multiple transactions (no constraint, full concurrency)',
    'many_to_one': 'M-to-1: Many transactions share one account (equivalent to 1-to-Many in this sim)'
  };
  
  const descEl = document.getElementById('rel-desc');
  if(descEl) {
    descEl.textContent = descMap[mode] || 'Unknown relationship mode';
  }
  
  addLog(`📊 Account-Transaction Relationship: ${mode.replace(/_/g, '-').toUpperCase()}`);
}

// Override or wrap the existing fetch call to /api/simulate
// This needs to be added to the existing startSimulation function
// The payload should include: relationshipMode: relationshipMode

// Example payload structure (to be added to existing startSimulation):
// const payload = {
//   algorithm: selectedAlgorithm,  // 'rr' or 'priority'
//   quantumMs: parseInt(document.getElementById('quantum').value),
//   initialBalance: parseInt(document.getElementById('initBalance').value),
//   threads: threads,
//   relationshipMode: relationshipMode  // <-- ADD THIS LINE
// };

console.log('✅ Relationship mode patch loaded');
console.log('Available modes: one_to_one, one_to_many, many_to_one');
console.log('Default mode: one_to_many');
