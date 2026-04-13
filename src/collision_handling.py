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
    all_items = os.listdir(target_directory)
    files_only = [f for f in all_items if os.path.isfile(os.path.join(target_directory, f))]
    file_groups = categorize_files(files_only)
    
    for ext, files in file_groups.items():
        folder_path = os.path.join(target_directory, ext)
        os.makedirs(folder_path, exist_ok=True)
        
        for file in files:
            source_path = os.path.join(target_directory, file)
            destination_path = os.path.join(folder_path, file)
            
            # --- NEW COLLISION HANDLING LOGIC ---
            # If the file already exists in the target folder, we need to rename it
            if os.path.exists(destination_path):
                # Separate the original filename into base and extension
                base_name, file_ext = os.path.splitext(file)
                counter = 1
                
                # Keep looping and incrementing the counter until we find a free name
                while os.path.exists(destination_path):
                    new_filename = f"{base_name}_{counter}{file_ext}"
                    destination_path = os.path.join(folder_path, new_filename)
                    counter += 1
            # ------------------------------------
            
            # Move the file (using the original name, or the newly generated one)
            shutil.move(source_path, destination_path)

# Example execution:
# organize_directory('/path/to/your/test_folder')