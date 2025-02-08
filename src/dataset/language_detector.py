from typing import Optional

class CustomLanguageDetector:
    """
    A simple language detector that uses provided alphabets.
    
    It counts the occurrences of each character that appears in each language’s alphabet
    and returns the language with the highest count.
    """
    
    def __init__(self, alphabets: dict = None) -> None:
        # Use the provided alphabets or default to English and Bulgarian.
        if alphabets is None:
            self.alphabets = {
                'en': 'abcdefghijklmnopqrstuvwxyz',
                'bg': 'абвгдежзийклмнопрстуфхцчшщъьюя',
            }
        else:
            self.alphabets = alphabets

    def detect(self, text: str) -> Optional[str]:
        """
        Detect the language of the input text.
        
        :param text: The text to analyze.
        :return: The language code with the most matching characters,
                 or None if no alphabetic characters are found.
        """
        text = text.lower()
        counts = {lang: 0 for lang in self.alphabets}
        
        # Count occurrences of characters for each language.
        for char in text:
            for lang, alphabet in self.alphabets.items():
                if char in alphabet:
                    counts[lang] += 1
        
        # If no characters were found in any of the alphabets, return None.
        if sum(counts.values()) == 0:
            return None
        
        # Return the language code with the maximum count.
        detected = max(counts, key=counts.get)
        return detected

