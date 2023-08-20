from trie import Trie
import os
import re

pattern = r'[^a-zA-Z0-9\s]'


def read_files(trie: Trie, dir_path: str, file_index: int = 0) -> None:
    """
    Recursively reads and processes text files in a directory, inserting words into a Trie.

    Args:
        trie (Trie): The Trie data structure to insert words into.
        dir_path (str): The path to the directory containing text files.
        file_index (int, optional): The current file index (used internally for recursion). Default is 0.

    Returns:
        None
    """
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_number, line in enumerate(file):
                        clean_line = re.sub(pattern, '', line).lower().strip()
                        for word_number, word in enumerate(clean_line.split()):
                            trie.insert(word, file_index, line_number, word_number)
                file_index += 1
        else:
            read_files(trie, file_path, file_index)


if __name__ == "__main__":
    trie_s = Trie()
    read_files(trie_s, "Archive", 0)
    print(trie_s.search("python"))
