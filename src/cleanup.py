import os
import time
import glob
from src.logger import logger

def cleanup_old_temp_files(directory=".", prefix="temp_", max_age_seconds=3600):
    """
    Delete temporary files older than max_age_seconds.
    Default age is 1 hour.
    """
    pattern = os.path.join(directory, f"{prefix}*")
    files = glob.glob(pattern)
    
    current_time = time.time()
    count = 0
    
    for file_path in files:
        try:
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                count += 1
        except Exception as e:
            logger.error("Error deleting %s: %s", file_path, e, exc_info=True)
            
    return count

if __name__ == "__main__":
    # Manual trigger
    deleted = cleanup_old_temp_files()
    logger.info("Cleaned up %d temporary files.", deleted)
