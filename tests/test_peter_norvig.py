import pytest
from src.correctors.pn_corrector import (
    PeterNorvigCorrector,
    preserve_case,
)


@pytest.fixture
def create_temp_dataset(tmp_path):
    dataset_content = (
        "this is a sample dataset for testing testing"
    )
    dataset_file = tmp_path / "db.txt"
    dataset_file.write_text(dataset_content, encoding="utf8")
    return str(dataset_file)


def test_corrector_init(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    assert corrector.max_distance == 2


def test_corrector_prob(create_temp_dataset):
    # Test the probability of a word in the dataset.
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    p = corrector.prob("testing")
    assert 0 < p <= 1


def test_corrector_correct_known_word(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    # "this" is in the dataset.
    assert corrector.correct("this") == "this"


def test_corrector_candidates(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    cands = corrector.candidates("datset")
    # Expect "dataset" to be among the candidates.
    assert "dataset" in cands


def test_corrector_short_word(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    # Words with less than 3 characters are not corrected.
    assert corrector.correct("it") == "it"
    assert corrector.correct("a") == "a"


def test_corrector_no_candidates(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    # For a word with no similar candidates in the dataset, the word
    # itself is returned as the only candidate.
    cands = corrector.candidates("zzzz")
    assert cands == ["zzzz"]


def test_update_cache(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    # Update cache for a word not in the cache yet.
    corrector.update_cache("hello", "hello_corr")
    assert corrector._correction_cache["hello"] == "hello_corr"
    assert corrector._candidates_cache["hello"] == ["hello_corr"]

    # Prepopulate candidates and update cache again.
    corrector._candidates_cache["hello"] = ["other", "hello_corr"]
    corrector.update_cache("hello", "hello_corr")
    assert corrector._candidates_cache["hello"][0] == "hello_corr"


def test_preserve_case():
    # Test upper-case preservation.
    assert preserve_case("HELLO", "hello") == "HELLO"
    # Test title-case preservation.
    assert preserve_case("Hello", "hello") == "Hello"
    # Test lower-case preservation.
    assert preserve_case("hello", "hello") == "hello"


def test_corrector_cached_result(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    # Manually update the correction cache.
    corrector._correction_cache["hello"] = "hello_corr"
    # Since "Hello" is title case, the result should be capitalized.
    result = corrector.correct("Hello")
    assert result == "Hello_corr"
