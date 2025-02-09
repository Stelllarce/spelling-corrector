from src.dataset.language_detector import SimpleLanguageDetector
from src.dataset.languages import alphabets


def test_detect_english():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # Test that words composed solely of English letters are detected as
    # 'en'.
    result = detector.detect("hello")
    assert result == "en"
    result = detector.detect("HeLLo")
    assert result == "en"
    result = detector.detect("world")
    assert result == "en"


def test_detect_bulgarian():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # Test that a Bulgarian word is detected as 'bg'.
    result = detector.detect("здравей")
    assert result == "bg"
    result = detector.detect("ЗДРАВЕЙ")
    assert result == "bg"


def test_detect_mixed():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # A word mixing English and Bulgarian letters should not be recognized.
    result = detector.detect("helloздравей")
    assert result is None


def test_detect_empty_string():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # For an empty string, all() returns True, so the detector will return
    # the first language in the dictionary. Assuming 'en' is first.
    result = detector.detect("")
    assert result == "en"


def test_detect_with_punctuation():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # Punctuation is ignored.
    result = detector.detect("hello!")
    assert result == "en"
    result = detector.detect("здравей,")
    assert result == "bg"


def test_detect_with_digits():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # Digits are ignored.
    result = detector.detect("hello2")
    assert result == "en"


def test_detect_with_space():
    detector = SimpleLanguageDetector(alphabets=alphabets)
    # Spaces are ignored.
    result = detector.detect("hello world")
    assert result == "en"


def test_empty_alphabets():
    # If an empty alphabets dictionary is provided, no word should be
    # recognized.
    detector = SimpleLanguageDetector(alphabets={})
    result = detector.detect("hello")
    assert result is None

    result = detector.detect("")
    assert result is None
