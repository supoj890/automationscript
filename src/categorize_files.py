import os
from collections import defaultdict

def categorize_files(file_list):
    # Using defaultdict prevents KeyErrors when appending to a new extension key
    categorized = defaultdict(list)
    
    for filename in file_list:
        # splitext returns a tuple: ('base_name', '.extension')
        _, ext = os.path.splitext(filename)
        
        if ext:
            # Remove the leading dot [1:] and convert to lowercase
            clean_ext = ext[1:].lower()
            categorized[clean_ext].append(filename)
        else:
            # If ext is an empty string, there is no extension
            categorized['unknown'].append(filename)
            
    # Convert back to a standard dictionary for the final output
    return dict(categorized)

# --- Test against the example ---
files = [
    "Q1_Report.PDF", 
    "budget_v2.xlsx", 
    "vacation_photo.Jpg", 
    "README", 
    "notes.txt", 
    "logo.jpg"
]

print(categorize_files(files))