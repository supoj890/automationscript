import pandas as pd

# --- Simulated System Data ---
hr_data = pd.DataFrame([
    {"emp_id": 101, "name": "Alice", "status": "Active"},
    {"emp_id": 102, "name": "Bob", "status": "Terminated"},
    {"emp_id": 103, "name": "Charlie", "status": "Terminated"},
    {"emp_id": 104, "name": "David", "status": "Active"}
])

it_assets = pd.DataFrame([
    {"emp_id": 101, "device": "MacBook Pro"},
    {"emp_id": 102, "device": "Dell XPS"}, 
    {"emp_id": 105, "device": "ThinkPad"}
])

def generate_audit_report(users_df, assets_df):
    # 1. Merge users_df and assets_df on 'emp_id'
    merged_df = pd.merge(users_df, assets_df, on='emp_id', how='inner')
    
    # 2. Filter the merged DataFrame for 'Terminated' status
    flagged_df = merged_df[merged_df['status'] == 'Terminated']
    
    # 3. Export the filtered DataFrame to Excel
    flagged_df.to_excel('unreturned_assets.xlsx', index=False)

# Example execution:
generate_audit_report(hr_data, it_assets)
print("Audit report generated: 'unreturned_assets.xlsx'")