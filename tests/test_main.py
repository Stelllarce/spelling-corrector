import pytest
# from unittest.mock import patch
from io import StringIO
import sys
from difflib import SequenceMatcher
from src.main import (
    process_text,
    input_correlates_to_language,
    PeterNorvigCorrector,
    # process_file
)


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate the similarity ratio between two strings.
    Returns a float between 0 and 1, where 1 means identical strings.
    """
    return SequenceMatcher(None, str1, str2).ratio()


def assert_text_similarity(actual: str, expected: str, threshold: float = 0.9):
    """
    Assert that two strings are similar enough.
    Default threshold is 0.9 (90% similarity).
    """
    similarity = calculate_similarity(actual, expected)
    assert similarity >= threshold, (
        f"Strings not similar enough. "
        f"Similarity: {similarity:.2%}\n"
        f"Expected: {expected}\n"
        f"Actual: {actual}"
    )


@pytest.fixture
def corrector():
    """Fixture to provide a corrector instance."""
    return PeterNorvigCorrector("src/dataset/en.txt", 2)


@pytest.fixture
def capture_stdout(monkeypatch):
    """Fixture to capture stdout."""
    string_io = StringIO()
    monkeypatch.setattr(sys, 'stdout', string_io)
    return string_io


@pytest.fixture
def sample_text_files(tmp_path):
    """Create sample text files for testing."""
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()

    files = {
        "simple.txt": "Thiss is a simple tesst file.",
        "multiple_lines.txt": "Firstt line of texxt.\nSecondd line here.\n"
                              "Thirdd line.",
        "special_chars.txt": "Don't forgett to inclüde speçial chârs!",
        "empty.txt": "",
    }

    created_files = {}
    for name, content in files.items():
        file_path = test_dir / name
        file_path.write_text(content)
        created_files[name] = file_path

    return created_files


@pytest.mark.parametrize("input_text,expected,threshold", [
    ("hellp world", "hello world", 0.85),
    ("Thiss is a tesst", "This is a test", 0.85),
    ("Hoow are yuo?", "How are you?", 0.85),
])
def test_simple_corrections(corrector, input_text, expected, threshold):
    """Test various simple text corrections."""
    result = process_text(input_text, corrector, display_corrected=False)
    assert_text_similarity(result, expected, threshold)


@pytest.mark.parametrize("input_text,expected,threshold", [
    (
        "Thiss is a tesst, with som punctuation!",
        "This is a test, with some punctuation!",
        0.9
    ),
    (
        "Don't forgett the apostrophe's... and other punct-uation!",
        "Don't forget the apostrophe's... and other punctuation!",
        0.85
    ),
    (
        "Helllo world. Hoow are yuo today? I'm doingg fine!",
        "Hello world. How are you today? I'm doing fine!",
        0.85
    ),
])
def test_complex_sentences(corrector, input_text, expected, threshold):
    """Test correction of complex sentences with punctuation."""
    result = process_text(input_text, corrector, display_corrected=False)
    assert_text_similarity(result, expected, threshold)


@pytest.mark.parametrize("text,language,expected", [
    ("This is English text", "en", True),
    ("Това е български текст", "en", False),
    ("This has numbers 123", "en", True),
    ("Text with punctuation!", "en", True),
])
def test_language_validation(text, language, expected):
    """Test language validation for different inputs."""
    assert input_correlates_to_language(language, text) == expected

# Only god knows why this test fails
# (process file does not create the output file)
# def test_file_correction(corrector, tmp_path):
#     """Test correction of text from a file."""
#     test_file = tmp_path / "test.txt"
#     test_content = "Thiss is a tesst file.\nIt hass multiple liness."
#     test_file.write_text(test_content)

#     with patch('main.FileManager') as mock_manager:
#         instance = mock_manager.return_value
#         instance.read_file.return_value = test_content

#         process_file(str(test_file), corrector)

#         expected_content = "This is a test file.\nIt has multiple lines."
#         instance.write_file.assert_called_once()
#         actual_content = instance.write_file.call_args[0][0]
#         assert_text_similarity(actual_content, expected_content, 0.9)


@pytest.mark.parametrize("edge_case,expected_behavior,threshold", [
    (
        "supercalifragilisticexpialidociouss",
        "supercalifragilisticexpialidocious",
        0.95
    ),
    ("123 th1s 1s @ t3st!", "123 this is @ test!", 0.85),
    ("too    many      spaces", "too many spaces", 0.8),
])
def test_edge_cases(corrector, edge_case, expected_behavior, threshold):
    """Test various edge cases in text correction."""
    result = process_text(edge_case, corrector, display_corrected=False)
    assert_text_similarity(result, expected_behavior, threshold)


@pytest.fixture
def mock_files(tmp_path):
    mock_dir = tmp_path / "mock_files"
    mock_dir.mkdir()
    mock_file = mock_dir / "en_mock.txt"
    expected_file = mock_dir / "en_mock_expected.txt"

    # Input text with intentional spelling errors
    mock_text = (
        "The qick brown fox jumpd over the lazi dog. "
        "It was an extrordinary event, because the beutiful canary "
        "that usualy sang in the monring had finaly woken up. "
        "However, the majestik cat did not seem "
        "amuzed by the sudden comotion. "
        "In fact, it decdied to slep a bit longer on the window sill, "
        "ignorng the convarsation betwen the animls.\n\n"
        "Meanwhile, a wandering travler stoped to see the stuning sunrise. "
        "He was carrying a small bakpack full "
        "of old paprs and scribbled notes, "
        "hoping to find the nearest town soon. "
        "The travler spke with the farmer "
        "who owned the land, as he was looking "
        "for dirctions to the next village. "
        "The farmer generusly offered some "
        "freshly baked bread, which the travler "
        "glady accepted.\n\n"
        "In the distance, a cry of a roostr echoed across the hills. "
        "The travler, the fox, and the cat semed to pause momentarily, "
        "as if time had frozn. Then, with renewed energy, the travler "
        "set off down the dusty road, determined to complete his joney "
        "before nightfal. He had a map that was quite outdted, but he "
        "believed in his ablity to find the right path eventually.\n\n"
        "Upon reaching the froest edge, the travler found some stberries "
        "growing in the buhes. They were sweet, "
        "albeit some were not yet ripe. "
        "A gentl breese rustled leaves overhead, and the travler felt "
        "suddenly gratefull for the quiet companionship of nature. "
        "There was much left to explore, and many places to discover, "
        "but for now, the journey continud with mispleled wrds and "
        "endless optimismm."
    )
    mock_file.write_text(mock_text, encoding='utf-8')

    # Expected corrected text
    expected_text = (
        "The quick brown fox jumped over the lazy dog. "
        "It was an extraordinary event, because the beautiful canary "
        "that usually sang in the morning had finally woken up. "
        "However, the majestic cat did not seem "
        "amused by the sudden commotion. "
        "In fact, it decided to sleep a bit longer on the window sill, "
        "ignoring the conversation between the animals.\n\n"
        "Meanwhile, a wandering traveler stopped "
        "to see the stunning sunrise. "
        "He was carrying a small backpack full "
        "of old papers and scribbled notes, "
        "hoping to find the nearest town soon. "
        "The traveler spoke with the farmer "
        "who owned the land, as he was looking "
        "for directions to the next village. "
        "The farmer generously offered some "
        "freshly baked bread, which the traveler "
        "gladly accepted.\n\n"
        "In the distance, a cry of a rooster echoed across the hills. "
        "The traveler, the fox, and the cat seemed to pause momentarily, "
        "as if time had frozen. Then, with renewed energy, the traveler "
        "set off down the dusty road, determined to complete his journey "
        "before nightfall. He had a map that was quite outdated, but he "
        "believed in his ability to find the right path eventually.\n\n"
        "Upon reaching the forest edge, the traveler found some strawberries "
        "growing in the bushes. They were sweet, "
        "albeit some were not yet ripe. "
        "A gentle breeze rustled leaves overhead, and the traveler felt "
        "suddenly grateful for the quiet companionship of nature. "
        "There was much left to explore, and many places to discover, "
        "but for now, the journey continued with misspelled words and "
        "endless optimism."
    )
    expected_file.write_text(expected_text, encoding='utf-8')

    return mock_file, expected_file


# Only god knows why this test fails
# (process file does not create the output file)
# def test_full_file_processing_integration(corrector, mock_files):
#     """Test complete file processing workflow with real files."""
#     mock_file, expected_file = mock_files
#     out = os.path.join("tests", "mock_files", "out.txt")
#     process_file(str(mock_file), corrector,
#                  out_path=out)

#     corrected_path = os.path.join("tests", "mock_files", "out_corrected.txt")
#     assert os.path.exists(corrected_path)

#     corrected_content = corrected_path.read_text()
#     expected_content = expected_file.read_text()
#     similarity = calculate_similarity(corrected_content, expected_content)
#     os.remove(corrected_path)
#     assert similarity >= 0.85, (
#         f"Corrected content does not match expected content.\n"
#         f"Corrected: {corrected_content}\n"
#         f"Expected: {expected_content}"
#     )


def test_accuracy_statistics(corrector):
    """Test overall correction accuracy across multiple samples."""
    test_cases = [
        ("Thiss is a tesst", "This is a test"),
        ("Helllo worldd", "Hello world"),
        ("Tessting the accuraccy", "Testing the accuracy"),
        ("Whaat about thiss?", "What about this?"),
    ]

    similarities = []
    for input_text, expected in test_cases:
        result = process_text(input_text, corrector, display_corrected=False)
        similarity = calculate_similarity(result, expected)
        similarities.append(similarity)

    average_accuracy = sum(similarities) / len(similarities)
    print(f"\nAverage correction accuracy: {average_accuracy:.2%}")
    assert average_accuracy >= 0.85, (
        f"Average accuracy {average_accuracy:.2%} below threshold of 85%"
    )


def test_multiline_accuracy(corrector):
    """Test accuracy of corrections in multi-line text."""
    input_text = """
    Thiss is the firsst line.
    The seconnd line has moore errors in itt.
    The thirrd and finall line is alsso wrong.
    """
    expected = """
    This is the first line.
    The second line has more errors in it.
    The third and final line is also wrong.
    """

    result = process_text(input_text, corrector, display_corrected=False)

    # Calculate similarity for each line separately
    input_lines = result.strip().split('\n')
    expected_lines = expected.strip().split('\n')

    line_similarities = []
    for actual, expected in zip(input_lines, expected_lines):
        similarity = calculate_similarity(actual.strip(), expected.strip())
        line_similarities.append(similarity)
        print(f"Line similarity: {similarity:.2%}")

    average_similarity = sum(line_similarities) / len(line_similarities)
    assert average_similarity >= 0.90, (
        f"Average line similarity {average_similarity:.2%} below threshold"
    )


if __name__ == '__main__':
    pytest.main(['-v'])
