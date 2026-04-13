import os
import shutil
from collections import defaultdict

def categorize_files(file_list):
    categorized = defaultdict(list)
    for filename in file_list:
        _, ext = os.path.splitext(filename)
        if ext:
            categorized[ext[1:].lower()].append(filename)
        else:
            categorized['unknown'].append(filename)
    return categorized

def organize_directory(target_directory):
    # 1. Get a list of all files in the target_directory using os.listdir()
    all_items = os.listdir(target_directory)
    files_only = [f for f in all_items if os.path.isfile(os.path.join(target_directory, f))]
    
    # 2. Pass the list of files to your categorize_files function
    file_groups = categorize_files(files_only)
    
    # 3. THE DIRTY CODE: 
    for ext, files in file_groups.items():
        # Define the path for the new folder based on the extension
        folder_path = os.path.join(target_directory, ext)
        
        # Create the directory if it doesn't already exist
        # exist_ok=True is crucial here so the script doesn't crash on future runs!
        os.makedirs(folder_path, exist_ok=True)
        
        # Move each file into its new home
        for file in files:
            source_path = os.path.join(target_directory, file)
            destination_path = os.path.join(folder_path, file)
            
            # Using shutil.move to physically relocate the file
            shutil.move(source_path, destination_path)

# Example execution:
# organize_directory('/path/to/your/test_folder')