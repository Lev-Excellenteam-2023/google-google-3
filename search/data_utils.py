from dataclasses import dataclass
from collections import namedtuple
from search.logic import get_file_name

SentenceIndex = namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __init__(self, sentence_index: SentenceIndex, sentence:str , score):
        self.completed_sentence = sentence
        self.source_text = get_file_name(sentence_index.file_id)
        self.offset = sentence_index.position
        self.score = score
