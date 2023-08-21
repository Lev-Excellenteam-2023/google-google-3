from typing import List, Tuple

from search.AutoCompleteData import AutoCompleteData, SentenceIndex

TrieTree = lambda: None

def get_best_kֵ_completions(prefix: str,k:int =5) -> List[AutoCompleteData]:
    """
    function to get the best k completions from the database.
    :param prefix: string of words that user input
    :param k: number of the best completions to return.
    :return: a list of AutoCompleteData objects
    """
    sentences = search(prefix)[:k]
    lst_of_auto_complete_data = [AutoCompleteData(sentence, len(prefix)) for sentence in sentences if sentence]
    if len(lst_of_auto_complete_data) < k:
        lst_of_auto_complete_data += get_best_kֵ_completions(prefix[:-1], k - len(lst_of_auto_complete_data))
    return lst_of_auto_complete_data



def search ( user_input: str ) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param user_input: string of words that user input
    :return: a list of sentences that match the user input.
    """
    words = user_input.split()
    trie_tree = TrieTree()
    trie_tree.build_trie_tree()
    indexes = search_words(words, trie_tree)
    return indexes


def search_word( word: str, trie_tree ) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param word: word to search_test in Trie tree.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    return trie_tree.search(word)


def search_words ( words: List[str], trie_tree ) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param words: list of words to search_test in Trie tree.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    indexes = [search_word(word, trie_tree) for word in words]
    res = []
    if not indexes[-1]:
        for word_completion in find_word_completion(words[-1], trie_tree):
            indexes[-1] = search_word(word_completion, trie_tree)
            res += filter_by_indexes(indexes)
    else:
        res += filter_by_indexes(indexes)
    return res


def filter_by_indexes( indexes: List[List[SentenceIndex]]) -> List[SentenceIndex]:
    """
    function to filter the autocomplete sentences by indexes.
    :param indexes: list of tuples of indexes of: (file_id, sentence_id, position)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    res = []
    for index in indexes:
        if not res:
            res = index
        else:
            res = compare_indexes(res, index)
    return res


def compare_indexes ( indexes_of_first_word: List[SentenceIndex],
                      indexes_of_second_word: List[SentenceIndex] ) -> List[SentenceIndex]:
    """
    function to compare the indexes of the first word to the indexes of the second word.
    :param indexes_of_first_word: list of indexes of the first word.
    :param indexes_of_second_word: list of indexes of the second word.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    # check if the words are in the same file and sentence and the second word is after the first word.
    return [index for index in indexes_of_first_word for index2 in indexes_of_second_word if
            index.file_id == index2.file_id and index.sentence_id == index2.sentence_id and
            index.position == index2.position - 1]


def find_word_completion( word_start: str, trie_tree ) -> List[str]:
    """
    function to find the word completion.
    :param word_start: the start of the word.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    return trie_tree.search_prefix(word_start)
