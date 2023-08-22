import  argparse
from typing import List
import dotenv

from trie import Trie
from read_to_trie import read_files
from search.search_completions import get_best_k_completion


def user_input():
    """
    Get the user input.
    :return: the user input.
    """
    string = input("Enter your text:")
    return string


def init_db() -> (Trie, List):
    """
    Initialize the database with the data from the files and return the trie and the data list
    :return: trie tree of the words, data list of the files.
    """
    trie_tree = Trie()
    path_to_data = dotenv.get_key(dotenv.find_dotenv(), "PATH_TO_DATA")
    data_list = []
    read_files(trie_tree, path_to_data, data_list, 0)
    return trie_tree, data_list


def init():
    """
    Initialize the search engine and return the trie and the data list.
    :return: trie tree of the words, data list of the files.
    """
    print("Welcome to the search engine!")
    print("Loading the database...")
    trie_tree, data_list = init_db()
    print("The search engine is ready to use!")
    return trie_tree, data_list



def main():
    parser = argparse.ArgumentParser(description="CLI interface for the project.")
    trie_tree, data_list = init()
    while True:
        # string = user_input()
        string = "introduction to"
        if string == "exit":
            break
        else:
            res = get_best_k_completion(string, trie_tree, 5)
            print(res)



if __name__ == "__main__":
    main()
