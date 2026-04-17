import os
import sys
import logging
import zipfile
from pathlib import Path
from datetime import datetime, timedelta

# --- Expert Twist: Environment Variable for Log Retention ---
# Usage: export LOG_DIR="/var/logs/app" && export MAX_AGE_DAYS=7
LOG_DIR = Path(os.getenv("LOG_DIR", "./Logs"))  # Default to ./Logs if not set
ARCHIVE_DIR = path(os.getenv("ARCHIVE_DIR", "./archive"))  # Default to ./archive if not set
MAX_AGE_DAYS = int(os.getenv("MAX_AGE_DAYS", "7"))  # Default to 7 days if not set
LOG_FILE = "cleanup.log"

## --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE) ,
        logging.StreamHandler(sys.stdout)
    ]
)

def rotate_logs(dry_run=False):
    # 1. Setup Archieve Directory
    if not ARCHIVE_DIR.exists():
        if dry_run:
            logging.info(f"[DRY-RUN] Would create archive directory: {ARCHIVE_DIR}")
        else:
            ARCHIVE_DIR.mkdir(parents=True)
            logging.info(f"Created archive directory: {ARCHIVE_DIR}")
    # 2. Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(days=MAX_AGE_DAYS)
    logging.info(f"Rotating logs older than: {cutoff_date.strftime('%Y-%m-$d %H:%M:%S')}")

    files_archived = 0

    # 3. Iterate through log files
    for file_path in LOG_DIR.iterdir():
        if file_path.is_file():
            try:
                last_modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

                if last_modified_time < cutoff_date:
                    archive_name = ARCHIVE_DIR / f"{file_path.stem}_{last_modified_time.strftime('%Y%m%d%H%M%S')}.zip"

                    if dry_run:
                        logging.info(f"[DRY-RUN] Would archive: {file_path} to {archive_name}")
                    else:
                        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            zipf.write(file_path, arcname=file_path.name)
                        file_path.unlink()  # Delete the original file after archiving
                        logging.info(f"Archived: {file_path} to {archive_name}")

                    files_archived += 1
            except PermissionError:
                logging.error(f"Permission denied: {file_path}")
            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")

    logging.info(f"Summary: {files_archived} files archived.")

if __name__ == "__main__":
    dry_mode = "--dry-run" in sys.argv
    rotate_logs(dry_run=dry_mode)