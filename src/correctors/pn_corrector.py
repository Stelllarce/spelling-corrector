from typing import List, Set
import re
from collections import Counter
from .utils import damerau_levenstein


def get_words(text: str) -> List[str]:
    """Return a list of words from the text given by using regex"""
    return re.findall(r'\w+', text.lower())


class PeterNorvigCorrector:
    """Spelling corrector utilizing Peter Norvig's approach"""
    def __init__(self, dataset_path: str, max_distance: int = 2) -> None:
        """
        Initialize the corrector with a dataset file path
        :param dataset_path: Path to the text file containing the training data
        :param max_distance: Maximum Damerau-Levenshtein distance to consider
        """
        with open(dataset_path, 'r', encoding='utf8') as file:
            text = file.read()
        self.words_dic: Counter = Counter(get_words(text))
        self.word_count: int = sum(self.words_dic.values())
        self.max_distance: int = max_distance

    def prob(self, word: str) -> float:
        """Return the probability of the word"""
        return self.words_dic[word] / self.word_count

    def correct(self, word: str) -> str:
        """Return the most probable spelling correction for the word"""
        return max(self.candidates(word), key=self.prob)

    def candidates(self, word: str) -> Set[str]:
        """Generate possible spelling corrections for the word"""
        candidates = self.known([word])
        if candidates:
            return candidates

        for distance in range(1, self.max_distance + 1):
            candidates = self.get_words_at_distance(word, distance)
            if candidates:
                return candidates

        return {word}

    def known(self, words: List[str]) -> Set[str]:
        """Return the subset of words that are actually in the dictionary"""
        return set(w for w in words if w in self.words_dic)

    def get_words_at_distance(self, word: str, distance: int) -> Set[str]:
        """Return all strings that have a
        specific Damerau-Levenshtein distance from word"""
        return self.known(w for w in self.words_dic.keys()
                          if damerau_levenstein(word, w) == distance)
