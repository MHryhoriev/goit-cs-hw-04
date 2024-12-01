from typing import Dict, List

def display_results(results: Dict[str, List[str]]):
    """
    Displays the results of the keyword search.

    Args:
        results (Dict[str, List[str]]): A dictionary where the keys are keywords
                                        and the values are lists of file paths
                                        where the keywords were found.
    """
    print("\nKeyword search results:")
    print("=" * 50)
    for keyword, files in sorted(results.items(), key=lambda x: x[0]):
        print(f"Keyword: '{keyword}'")
        if files:
            print(f"  Found in {len(files)} files:")
            for file in sorted(files):
                print(f"    - {file}")
        else:
            print("  Not found in any file.")
        print("-" * 50)


def create_file_chunks(files: List[str]):
    num_threads = min(len(files), 4)
    chunk_size = len(files) // num_threads + (len(files) % num_threads > 0)
    return [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]