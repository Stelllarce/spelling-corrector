import sys
import pytest

from src.file_manager import FileManager
import src.app as app
from src.app import (
    language_selector,
    get_text_input,
    input_correlates_to_language,
    process_text,
    process_file,
    interactive_loop,
    main,
)


# A dummy corrector for testing purposes.
class DummyCorrector:
    def correct(self, word: str) -> str:
        # For testing, simply return the word unchanged.
        return word


def test_input_correlates_to_language_valid():
    valid_text = "Hello, world! 123"
    # Punctuation, whitespace, and digits are ignored.
    assert input_correlates_to_language("en", valid_text)


def test_input_correlates_to_language_invalid():
    invalid_text = "Hello, Привет!"
    assert not input_correlates_to_language("en", invalid_text)


def test_process_text_without_display(capsys):
    text = "Hello, worl."
    dummy = DummyCorrector()
    corrected = process_text(text, dummy, display_corrected=False)
    captured = capsys.readouterr().out
    assert "Original text:" not in captured
    assert corrected == "Hello, worl."


def test_process_text_with_display(capsys):
    text = "Hello, worl."
    dummy = DummyCorrector()
    process_text(text, dummy)
    captured = capsys.readouterr().out

    assert "Original text:" in captured
    assert "Corrected text:" in captured
    assert "Processing time:" in captured


def test_language_selector(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "en")
    lang = language_selector()
    assert lang == "en"


def test_get_text_input_normal(monkeypatch):
    # Simulate user entering two lines followed by a blank line.
    inputs = iter(["Hello", "world", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = get_text_input()
    # Expecting the two lines to be concatenated with a space.
    assert result == "Hello world"


def test_get_text_input_exit(monkeypatch):
    # Simulate immediate exit command.
    inputs = iter(["!exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = get_text_input()
    assert result is None


def test_interactive_loop(monkeypatch):
    # Simulate an interactive session with a !change branch.
    inputs = iter(["!change", "", "bg", "hello", "", "!exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    call_log = []

    def fake_process_text(text, corrector, display_corrected=True):
        call_log.append(text)
        return text

    monkeypatch.setattr(app, "process_text", fake_process_text)
    # Force PeterNorvigCorrector to always return our dummy.
    monkeypatch.setattr(app,
                        "PeterNorvigCorrector",
                        lambda path, d: DummyCorrector())
    # Force the language validation to always pass.
    monkeypatch.setattr(app,
                        "input_correlates_to_language",
                        lambda lang, text: True)
    dummy = DummyCorrector()
    interactive_loop(dummy, "en", 2)
    # Verify that "hello" was processed.
    assert "hello" in call_log


def test_interactive_loop_invalid_text(monkeypatch, capsys):
    # Simulate an input that fails language validation.
    inputs = iter(["invalid text", "", "!exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr(app,
                        "input_correlates_to_language",
                        lambda lang, text: False)
    dummy = DummyCorrector()
    interactive_loop(dummy, "en", 2)
    captured = capsys.readouterr().out
    assert "The text does not match the selected language." in captured


def test_interactive_loop_change_file_not_found(monkeypatch, capsys):
    # Simulate the !change branch where
    # PeterNorvigCorrector raises FileNotFoundError.
    inputs = iter(["!change", "", "en", "!exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    def raise_file_not_found(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(app, "PeterNorvigCorrector", raise_file_not_found)
    dummy = DummyCorrector()
    interactive_loop(dummy, "en", 2)
    captured = capsys.readouterr().out
    assert "The dataset file was not found or is not yet added." in captured


@pytest.mark.asyncio
async def test_process_file_valid(tmp_path, monkeypatch):
    input_text = "Hello world"
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_text, encoding="utf-8")
    dummy = DummyCorrector()
    monkeypatch.setattr(app, "FileManager", FileManager)
    # Force language validation to pass.
    monkeypatch.setattr(app,
                        "input_correlates_to_language",
                        lambda lang, text: True)
    await process_file(
        str(input_file),
        dummy,
        language="en",
        output_dir=str(tmp_path),
        output_name="result",
    )
    # Expected output file name is "result" with the original extension.
    output_file = tmp_path / "result.txt"
    assert output_file.exists()
    expected_output = process_text("Hello world",
                                   dummy,
                                   display_corrected=False)
    actual_output = output_file.read_text(encoding="utf-8")
    assert actual_output == expected_output


@pytest.mark.asyncio
async def test_process_file_default_naming(tmp_path, monkeypatch):
    # Test branch where output_name is not provided.
    input_text = "Hello world"
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_text, encoding="utf-8")
    dummy = DummyCorrector()
    monkeypatch.setattr(app, "FileManager", FileManager)
    monkeypatch.setattr(app,
                        "input_correlates_to_language",
                        lambda lang, text: True)
    await process_file(
        str(input_file),
        dummy,
        language="en",
        output_dir=str(tmp_path),
        output_name=None,
    )
    # Expected default naming: original file name with "_corrected" appended.
    output_file = tmp_path / "input_corrected.txt"
    assert output_file.exists()
    expected_output = process_text("Hello world",
                                   dummy,
                                   display_corrected=False)
    actual_output = output_file.read_text(encoding="utf-8")
    assert actual_output == expected_output


@pytest.mark.asyncio
async def test_process_file_invalid(tmp_path, monkeypatch):
    # Test the branch where language validation fails.
    input_text = "Hello Привет"
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_text, encoding="utf-8")
    dummy = DummyCorrector()
    monkeypatch.setattr(app, "FileManager", FileManager)
    monkeypatch.setattr(app,
                        "input_correlates_to_language",
                        lambda lang, text: False)
    with pytest.raises(SystemExit) as excinfo:
        await process_file(str(input_file), dummy, language="en")
    assert excinfo.value.code == 1


def test_main_interactive(monkeypatch):
    # Simulate interactive mode by not passing a file.
    test_args = ["app.py", "-d", "2", "-l", "en"]
    monkeypatch.setattr(sys, "argv", test_args)
    called_flag = {"called": False}

    def dummy_interactive_loop(corrector, language, max_edit_distance):
        called_flag["called"] = True

    monkeypatch.setattr(app, "interactive_loop", dummy_interactive_loop)
    monkeypatch.setattr(app,
                        "PeterNorvigCorrector",
                        lambda path, d: DummyCorrector())
    main()
    assert called_flag["called"]


def test_main_file_mode(monkeypatch, tmp_path):
    # Simulate file mode by passing a valid file.
    input_file = tmp_path / "input.txt"
    input_file.write_text("Hello world", encoding="utf-8")
    test_args = ["app.py", "-d", "2", "-l", "en", "-f", str(input_file)]
    monkeypatch.setattr(sys, "argv", test_args)
    called_flag = {"called": False}

    def dummy_asyncio_run(coro):
        called_flag["called"] = True

    monkeypatch.setattr(app.asyncio, "run", dummy_asyncio_run)
    monkeypatch.setattr(app,
                        "PeterNorvigCorrector",
                        lambda path, d: DummyCorrector())
    main()
    assert called_flag["called"]


def test_main_file_not_found(monkeypatch, capsys):
    # Simulate the branch where PeterNorvigCorrector raises FileNotFoundError.
    test_args = ["app.py", "-d", "2", "-l", "en"]
    monkeypatch.setattr(sys, "argv", test_args)

    def raise_file_not_found(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(app, "PeterNorvigCorrector", raise_file_not_found)
    main()
    captured = capsys.readouterr().out
    assert "The dataset file for the selected language was not found." \
        in captured
