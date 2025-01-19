from src.correctors.utils import damerau_levenstein


def test_damerau_levenstein_same_string():
    assert damerau_levenstein("test", "test") == 0


def test_damerau_levenstein_deletion():
    assert damerau_levenstein("test", "tes") == 1


def test_damerau_levenstein_insertion():
    assert damerau_levenstein("tes", "test") == 1


def test_damerau_levenstein_substitution():
    assert damerau_levenstein("test", "tast") == 1


def test_damerau_levenstein_transposition():
    assert damerau_levenstein("test", "tset") == 1


def test_damerau_levenstein_multiple_operations():
    assert damerau_levenstein("abc", "yabd") == 2
