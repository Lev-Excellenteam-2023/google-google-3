from typing import List, Tuple
from trie import Trie
from search.data_utils import AutoCompleteData, SentenceIndex
from search.logic import find_sentence_by_indexes
from collections import defaultdict


def get_best_k_completion ( prefix: str, trie_tree: Trie, data_list: List[str], k: int = 5 ) -> List[AutoCompleteData]:
    """
    function to get the best k completions from the database.
    :param trie_tree:
    :param prefix: string of words that user input
    :param data_list: list of the sentences.
    :param k: number of the best completions to return.
    :return: a list of AutoCompleteData objects
    """
    sentences_indexes = search(prefix, trie_tree)[:k]
    lst_of_auto_complete_data = [
        AutoCompleteData(sentence_index, find_sentence_by_indexes(sentence_index, data_list), len(prefix)) for
        sentence_index in sentences_indexes if sentence_index]
    return lst_of_auto_complete_data


def search ( user_input: str, trie_tree, shift: int = 1 ) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param user_input: string of words that user input
    :param trie_tree: the trie tree of the database.
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of sentences that match the user input.
    """
    words = user_input.split()
    indexes = search_words(words, trie_tree, shift)
    return indexes


def search_word ( word: str, trie_tree ) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param trie_tree:
    :param word: word to search_test in Trie tree.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    return trie_tree.search(word)


def search_words ( words: List[str], trie_tree, shift: int = 1 ) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param trie_tree:
    :param words: list of words to search_test in Trie tree.
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    indexes = [search_word(word, trie_tree) for word in words]
    res = []
    if not indexes[-1]:
        for word_completion in find_word_completion(words[-1], trie_tree):
            indexes[-1] = search_word(word_completion, trie_tree)
            res += filter_by_indexes(indexes, shift)
    else:
        res += filter_by_indexes(indexes, shift)
    return res


def filter_by_indexes ( indexes: List[List[SentenceIndex]], shift: int = 1 ) -> List[SentenceIndex]:
    """
    function to filter the autocomplete sentences by indexes.
    :param indexes: list of lists of indexes of: (file_id, sentence_id, position)
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    res = indexes[0]
    if len(indexes) == 1:
        return res
    for i in range(1, len(indexes)):
        res = compare_indexes(res, indexes[i], shift + i - 1)
    return res


def compare_indexes ( indexes_of_first_word: List[SentenceIndex],
                      indexes_of_second_word: List[SentenceIndex], shift: int = 1 ) -> List[SentenceIndex]:
    """
    function to compare the indexes of two words.
    :param indexes_of_first_word: list of indexes of the first word.
    :param indexes_of_second_word: list of indexes of the second word.
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    # this is a refactor of the code to improve the run time.
    # by using a dictionary to group the indexes by the file_id and sentence_id. of the second word.
    grouped_indexes = defaultdict(list)
    for index in indexes_of_second_word:
        grouped_indexes[(index.file_id, index.sentence_id)].append(index.position)

    res = []
    # now i only need to iterate over the indexes of the first word.
    # (the first word is the one that has less indexes because it is usally already was comaperaed to all the other
    # words above it in the sentence)
    for index in indexes_of_first_word:
        if (index.file_id, index.sentence_id) in grouped_indexes:
            second_word_positions = grouped_indexes[(index.file_id, index.sentence_id)]
            for position in second_word_positions:
                second_word_position = position - shift
                if index.position == second_word_position:
                    res.append(index)
                elif index.position < second_word_position:
                    break

    return res


def find_word_completion ( word_start: str, trie_tree ) -> List[str]:
    """
    function to find the word completion.
    :param trie_tree:
    :param word_start: the start of the word.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    return trie_tree.search_prefix(word_start)
