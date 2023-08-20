from collections import namedtuple
from typing import List

NUM_OF_CHARS = 36

SentenceIndex = namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])


class TrieNode:
    """
    TrieNode represents a node in the Trie data structure.
    """

    def __init__(self):
        self.children = [None] * NUM_OF_CHARS
        self.word_location = []
        # isEndOfWord is True if node represents the end of a word
        self.isEndOfWord = False


class Trie:
    """
    Trie is a data structure for efficient word insertion and searching.
    """

    def __init__(self):
        self.root = self.get_node()

    @staticmethod
    def get_node() -> TrieNode:
        """
        Returns a new TrieNode (initialized to NULLs).
        """
        return TrieNode()

    @staticmethod
    def char_to_index(ch) -> int:
        """
        Converts the given character into an index (0-25) assuming lowercase 'a' to 'z'.
        """
        if ch.isalpha():
            return ord(ch.lower()) - ord('a')
        return ord(ch) - ord('0') + 26

    def insert(self, key: str, file_id: int, row_number: int, word_index: int) -> None:
        """
        Inserts a word into the Trie.
        Returns:
            None
            :param key: key (str): The word to be inserted.
            :param file_id: file_id(int) The file id
            :param row_number: row_number(int) The word number of row
            :param word_index: word_index(int) The word index in the sentence
        """
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self.char_to_index(key[level])
            # If the current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.get_node()
            pCrawl = pCrawl.children[index]

        # Mark the last node as the end of the word
        pCrawl.word_location.append(SentenceIndex(file_id, row_number, word_index))
        pCrawl.isEndOfWord = True

    def search(self, key: str) -> List[SentenceIndex]:
        """
        Searches for a word in the Trie.

        Args:
            key (str): The word to be searched.

        Returns:
            bool: True if the word is found in the Trie, False otherwise.
        """
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self.char_to_index(key[level])
            if not pCrawl.children[index]:
                return []
            pCrawl = pCrawl.children[index]
        return pCrawl.word_location
