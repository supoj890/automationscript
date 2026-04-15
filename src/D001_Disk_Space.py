import os
import sys
import logging
from pathlib import Path

# --- Configuration ---
LOG_DIR = Path("./Logs")    #Change this to your desired log directory
SIZE_THRESHOLD_MB = 5       #Set the size threshold in MB
SIZE_THRESHOLD_BYTES = SIZE_THRESHOLD_MB * 1024 * 1024
LOG_FILE = "cleanup.log"

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE) ,
        logging.StreamHandler(sys.stdout)
    ]
)

def clean_logs(dry_run=False):
    if dry_run:
        logging.info("Running in dry-run mode. No files will be deleted.") 
    
    total_reclaimed_bytes = 0
    files_processed = 0

    # Ensure Directory exists
    if not LOG_DIR.exists():
        logging.warning(f"Log directory {LOG_DIR} does not exist. Exiting.")
        return
    
    # Iterate Through Log Files
    for file_path in LOG_DIR.iterdir():
        if file_path.is_file():
            try:
                file_size = file_path.stat().st_size

                if file_size > SIZE_THRESHOLD_BYTES:
                    readable_size = file_size / (1024 * 1024)  # Convert to MB

                    if dry_run:
                        logging.info(f"[DRY-RUN] Would delete: {file_path} (Size: {readable_size:.2f} MB)")
                    else:  
                        file_path.unlink()  # Delete the file
                        logging.info(f"Deleted: {file_path} (Size: {readable_size:.2f} MB)")

                    total_reclaimed_bytes += file_size
                    files_processed += 1   
            except PermissionError:
                logging.error(f"Permission denied: {file_path}")
            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")

    # Summary
    reclaimed_mb = total_reclaimed_bytes / (1024 * 1024)
    status_verb = "would be reclaimed" if dry_run else "reclaimed"
    logging.info(f"Summary: {files_processed} files processed. Total space {status_verb}: {reclaimed_mb:.2f} MB.")

if __name__ == "__main__":
    # Check for dry-run argument
    dry_run_mode = "--dry-run" in sys.argv
    clean_logs(dry_run=dry_run_mode)