from dataclasses import dataclass
from collections import namedtuple

SentenceIndex = namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])
get_sentence = lambda sentenceIndex: f'{sentenceIndex.source_text[sentenceIndex.offֵset:]}'
get_file_name = lambda file_id: f'{file_id}.txt'

@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offֵset: int
    score: int

    def __init__(self,sentenceIndex:SentenceIndex,score):
        self.completed_sentence = get_sentence(sentenceIndex)
        self.source_text = get_file_name(sentenceIndex.file_id)
        self.offֵset = sentenceIndex.position
        self.score = score
