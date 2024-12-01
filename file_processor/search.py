from typing import List, Dict

def search_keywords_in_file(file_path: str, keywords: List[str]) -> Dict[str, List[str]]:
    """
    Searches for the given keywords in a file and returns the file paths where each keyword is found.

    Args:
        file_path (str): The path of the file to search within.
        keywords (List[str]): A list of keywords to search for within the file.

    Returns:
        Dict[str, List[str]]: A dictionary where the keys are keywords and the values are lists of file paths
                               where each keyword was found. If a keyword is not found in the file, it will
                               not appear in the dictionary.
    """
    matches = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    matches[keyword].append(file_path)
    except Exception as e:
        print(f"File processing error {file_path}: {e}")
    return matches
