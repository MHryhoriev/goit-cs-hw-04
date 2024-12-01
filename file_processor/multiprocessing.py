from multiprocessing import Process, Queue
from typing import List, Dict
from .search import search_keywords_in_file
from .utils import create_file_chunks

def worker(file_chunk: List[str], keywords: List[str], queue: Queue):
    """
    Worker function to process a chunk of files, searching for keywords, and putting the results into the queue.

    Args:
        file_chunk (List[str]): List of file paths to process.
        keywords (List[str]): List of keywords to search for.
        queue (Queue): The queue to put the results into.
    """
    results = {keyword: [] for keyword in keywords}
    for file_path in file_chunk:
        matches = search_keywords_in_file(file_path, keywords)
        for keyword, files in matches.items():
            results[keyword].extend(files)
    queue.put(results)

def process_files_multiprocessing(files: List[str], keywords: List[str]) -> Dict[str, List[str]]:
    """
    Process files in parallel using multiple processes. The files are divided into chunks, and each process searches for keywords.

    Args:
        files (List[str]): List of file paths to process.
        keywords (List[str]): List of keywords to search for.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are keywords and values are lists of file paths
                               where the keywords were found.
    """
    file_chunks = create_file_chunks(files)

    queue = Queue()
    processes = []

    # Start processes
    for file_chunk in file_chunks:
        process = Process(target=worker, args=(file_chunk, keywords, queue))
        processes.append(process)
        process.start()

    # Collect results from each process
    aggregated_results = {keyword: [] for keyword in keywords}
    for _ in range(len(processes)):
        partial_results = queue.get()
        for keyword, paths in partial_results.items():
            aggregated_results[keyword].extend(paths)

    # Wait for all processes to finish
    for process in processes:
        process.join()

    return aggregated_results
