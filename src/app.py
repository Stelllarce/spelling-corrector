import time
import re
import concurrent.futures
import asyncio
from .file_manager import FileManager
from src.correctors.pn_corrector import PeterNorvigCorrector
from src.dataset.languages import alphabets
from tqdm import tqdm


def language_selector() -> str:
    """Select the language of the text to be corrected."""
    print("Select the language of the text: en, bg, de")
    language = input("Enter language: ")
    return language


def get_text_input() -> str | None:
    """Get text input from the user."""
    print("Enter text (press Enter twice to process, or '!exit' to quit):")
    text = ""
    while True:
        line = input()
        if line.strip() == "!exit":
            return None
        if line.strip() == "":
            return text.strip()
        text += line + " "


def input_correlates_to_language(language: str, text: str) -> bool:
    """Check if the input text matches the selected language."""
    clean_text = re.sub(r'[\'\’.\-,?!\":;\s\d]', '', text)
    return all(char.lower() in alphabets[language] for char in clean_text)


def process_text(text: str,
                 corrector: PeterNorvigCorrector,
                 display_corrected: bool = True) -> str:
    """Process the input text."""
    start_time = time.time()
    # Split text preserving punctuation
    words_with_punct = re.findall(r'\w+|[\'\’.\-,?!\":;\t\n]', text)
    # Correct only words, preserve punctuation
    corrected_words = []
    for word in tqdm(words_with_punct, desc="Processing text"):
        if re.match(r'\w+', word):
            corrected_words.append(corrector.correct(word))
        else:
            corrected_words.append(word)

    corrected_text = ' '.join(corrected_words)
    # Clean up extra spaces before punctuation
    corrected_text = re.sub(r'\s+([\'\’.\-,?!\":;])', r'\1', corrected_text)
    end_time = time.time()
    if display_corrected:
        print("\nOriginal text:", text)
        print("Corrected text:", corrected_text)
    print(f"\nProcessing time: {(end_time - start_time):.4f} seconds\n")
    return corrected_text


def setup_corrector(depth: str) -> tuple[str, PeterNorvigCorrector]:
    """Setup the corrector with the selected
        language and maximum edit distance."""
    while True:
        try:
            selected_language = language_selector()
            corrector = PeterNorvigCorrector(
                f"src/dataset/{selected_language}.txt", int(depth)
            )
            return selected_language, corrector
        except FileNotFoundError:
            print("The dataset file was not found or is not yet added.")
        except ValueError:
            print("The maximum edit distance must be an integer.")


async def process_file(file_path: str,
                       corrector: PeterNorvigCorrector) -> None:
    """Process the text from a file."""
    start_time = time.time()
    manager = FileManager(file_path)
    text = manager.read_file()

    def process_line(line: str) -> str:
        return process_text(line, corrector, display_corrected=False)

    lines = text.split('\n')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_line, line) for line in lines]
        corrected_lines = [future.result() for future in futures]

    corrected_text = '\n'.join(corrected_lines)
    name, ext = file_path.rsplit('.', 1)
    new_file = f"{name}_corrected.{ext}"
    out_manager = FileManager(new_file)
    out_manager.write_file(corrected_text)
    end_time = time.time()
    print(f"\nTotal processing time: {(end_time - start_time):.4f} seconds")
    print(f"Corrected file saved to {new_file}")


async def main():
    depth = input("Enter the maximum edit distance: ")
    selected_language, corrector = setup_corrector(depth)

    while True:
        print(
            "\nType '!change' to change language, "
            "'!file' to correct a file, or enter your text:")
        text = get_text_input()
        if text is None:
            return
        if text == "!change":
            selected_language, corrector = setup_corrector(depth)
            continue
        if text.startswith("!file "):
            file_name = text.split("!file ", 1)[1].strip()
            await process_file(file_name, corrector)  # Removed await
            continue
        if not input_correlates_to_language(selected_language, text):
            print("The text does not match the selected language.")
            continue
        if text:
            process_text(text, corrector)


if __name__ == '__main__':
    asyncio.run(main())
