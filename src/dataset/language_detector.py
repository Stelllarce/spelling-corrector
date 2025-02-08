from typing import Optional
from .languages import alphabets as preloaded_alphabets


class SimpleLanguageDetector:
    """ A simple language detector that uses provided alphabets. """

    def __init__(self, alphabets: dict = None) -> None:
        # Use the provided alphabets or default to English and Bulgarian.
        self.alphabets = alphabets \
            if alphabets is not None \
            else preloaded_alphabets

    # Future work may require to change this
    # to support more romanic and slavic languages.
    # Right now it works because the alphabets have no union characters.
    def detect(self, word: str) -> Optional[str]:
        """
        Detect the language of the input text.
        All characters in a single word must belong to the same alphabet.
        This works well when the languages
        differ significantly in alphabet characters.

        :param text: The text to analyze.
        :return: The detected language
        or None if the language is not recognized.
        """
        for lang, alphabet in self.alphabets.items():
            if all(char in alphabet for char in word):
                return lang
        return None
