import pytest
from src.correctors.peter_norvig import PeterNorvigCorrector


@pytest.fixture
def create_temp_dataset(tmp_path):
    dataset_content = "this is a sample dataset for testing testing"
    dataset_file = tmp_path / "db.txt"
    dataset_file.write_text(dataset_content)
    return str(dataset_file)


def test_corrector_init(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    assert corrector.max_distance == 2


def test_corrector_prob(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    p = corrector.prob("testing")
    assert 0 < p <= 1


def test_corrector_correct_known_word(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    assert corrector.correct("this") == "this"


def test_corrector_candidates(create_temp_dataset):
    corrector = PeterNorvigCorrector(create_temp_dataset, max_distance=2)
    cands = corrector.candidates("datset")
    assert "dataset" in cands
