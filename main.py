import os
import time
from file_processor.multithreading import process_files_multithreading
from file_processor.multiprocessing import process_files_multiprocessing
from file_processor.utils import display_results

# Search keywords
KEYWORDS = ["технології", "природа", "гармонія", "майбутнє", "людство"]

# Path to files
DATA_FOLDER = "data"

if __name__ == "__main__":
    # Getting a list of files
    files = [os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER) if f.endswith(".txt")]

    # Multithreaded approach
    print("\n=== Multithreaded approach ===")
    start_time = time.time()
    threading_results = process_files_multithreading(files, KEYWORDS)
    display_results(threading_results)
    print("Multithreading execution time:", time.time() - start_time, "seconds")

    # Multiprocessor approach
    print("\n=== Multiprocessor approach ===")
    start_time = time.time()
    multiprocessing_results = process_files_multiprocessing(files, KEYWORDS)
    display_results(multiprocessing_results)
    print("Multiprocessing execution time:", time.time() - start_time, "seconds")
