from typing import List, Set
import re
from collections import Counter
from .utils import damerau_levenstein
from typing import Generator


def read_line_by_line_buffered(
    file_path: str,
    buffer_size: int = 1024 * 1024
) -> Generator[str, None, None]:
    with open(file_path, 'r', encoding='utf8') as file:
        while True:
            lines = file.readlines(buffer_size)
            if not lines:
                break
            for line in lines:
                yield line.strip()


def get_words(text: str) -> List[str]:
    """Return a list of words from the text given by using regex"""
    return re.findall(r'\w+', text.lower())


def preserve_case(original: str, corrected: str) -> str:
    """Preserve the case style of the original word."""
    if original.isupper():
        return corrected.upper()
    if original.istitle():
        return corrected.capitalize()
    return corrected.lower()


class PeterNorvigCorrector:
    """Spelling corrector utilizing Peter Norvig's approach"""
    def __init__(self, dataset_path: str, max_distance: int = 3) -> None:
        """
        Initialize the corrector with a dataset file path
        :param dataset_path: Path to the text file containing the training data
        :param max_distance: Maximum Damerau-Levenshtein distance to consider
        """

        self.words_dict: Counter = Counter(
            get_words(
                '\n'.join(
                    list(
                        read_line_by_line_buffered(dataset_path)
                        )
                    )
                )
            )
        self.word_count: int = sum(self.words_dict.values())
        self.max_distance: int = max_distance
        self._correction_cache: dict = {}

    def prob(self, word: str) -> float:
        """Return the probability of the word"""
        return self.words_dict[word] / self.word_count

    def correct(self, word: str) -> str:
        """Return the most probable spelling correction for the word"""
        # Words with less than 3 characters are not corrected, because
        # without grammar model is nearly impossible to be accurate
        if len(word) < 3:
            return word

        lower_word = word.lower()
        if lower_word in self._correction_cache:
            return preserve_case(word, self._correction_cache[lower_word])
        elif word in self.words_dict:
            return word

        correction = max(self.candidates(word), key=self.prob)
        self._correction_cache[lower_word] = correction
        return preserve_case(word, correction)

    def candidates(self, word: str) -> List[str]:
        """Generate possible spelling corrections for the word"""
        candidates = self.__known([word])
        if candidates:
            return sorted(candidates,
                          key=lambda w: (self.prob(w), w),
                          reverse=True)

        for distance in range(1, self.max_distance + 1):
            candidates = self.__get_words_at_distance(word, distance)
            if candidates:
                return sorted(candidates,
                              key=lambda w: (self.prob(w), w),
                              reverse=True)

        return [word]

    def __known(self, words: List[str]) -> Set[str]:
        """Return the subset of words that are actually in the dictionary"""
        return set(w for w in words if w in self.words_dict)

    def __get_words_at_distance(self, word: str, distance: int) -> Set[str]:
        """Return all strings that have a
        specific Damerau-Levenshtein distance from word"""
        return self.__known(w for w in self.words_dict.keys()
                            if damerau_levenstein(word, w) == distance)
