from threading import Thread, Lock
from typing import List, Dict
from .search import search_keywords_in_file
from .utils import create_file_chunks

def worker(file_chunk: List[str], keywords: List[str], result_store: Dict[str, List[str]], lock: Lock):
    """
    Worker function to search for keywords in a chunk of files. It updates the shared result store using a lock to ensure
    thread-safety when modifying the result dictionary.

    Args:
        file_chunk (List[str]): A list of file paths to process.
        keywords (List[str]): The list of keywords to search for.
        result_store (Dict[str, List[str]]): The dictionary where results will be stored.
        lock (Lock): A lock object to synchronize access to the shared result store.
    """
    for file_path in file_chunk:
        matches = search_keywords_in_file(file_path, keywords)
        with lock:
            for keyword, files in matches.items():
                result_store[keyword].extend(files)

def process_files_multithreading(files: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    """
    Processes a list of files using multiple threads. It divides the files into chunks and processes them concurrently
    to search for keywords.

    Args:
        files (List[str]): A list of file paths to process.
        keywords (List[str]): The list of keywords to search for.

    Returns:
        Dict[str, List[str]]: A dictionary with keywords as keys and lists of file paths as values indicating where 
                               each keyword was found.
    """
    file_chunks = create_file_chunks(files)

    result_dict = {keyword: [] for keyword in keywords}
    lock = Lock()
    threads = []

    # Create and start threads
    for file_chunk in file_chunks:
        thread = Thread(target=worker, args=(file_chunk, keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return result_dict
