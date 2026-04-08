def merge_datasets(profiles, billing):
    # 1. Create an O(1) lookup dictionary from the billing list
    # Key = user_id, Value = the entire billing dictionary
    billing_lookup = {record['user_id']: record for record in billing}
    
    merged_data = []
    
    # 2. Iterate through profiles exactly once
    for profile in profiles:
        user_id = profile['user_id']
        
        # 3. Fetch the matching billing data (default to empty dict if missing)
        bill_data = billing_lookup.get(user_id, {})
        
        # 4. Merge dictionaries using Python's unpacking syntax (**)
        combined_record = {**profile, **bill_data}
        merged_data.append(combined_record)
        
    return merged_data

# --- Test Data ---
profiles = [
    {"user_id": 101, "name": "Alice_Admin"},
    {"user_id": 102, "name": "Bob_User"},
    {"user_id": 103, "name": "Charlie_Dev"}
]

billing = [
    {"user_id": 102, "plan": "Basic", "owed": 15.00},
    {"user_id": 103, "plan": "Pro", "owed": 0.00},
    {"user_id": 101, "plan": "Enterprise", "owed": 500.00}
]

# --- Execution ---
import pprint
pprint.pprint(merge_datasets(profiles, billing), sort_dicts=False)