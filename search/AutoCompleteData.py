from dataclasses import dataclass
from collections import namedtuple

SentenceIndex = namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])
get_sentence = lambda sentence_index: f'{sentenceIndex.source_text[sentenceIndex.offֵset:]}'
get_file_name = lambda file_id: f'{file_id}.txt'


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __init__(self, sentence_index: SentenceIndex, score):
        self.completed_sentence = get_sentence(sentence_index)
        self.source_text = get_file_name(sentence_index.file_id)
        self.offset = sentence_index.position
        self.score = score
