import argparse
import asyncio
import concurrent.futures
import os
import re
import sys
import time

from tqdm import tqdm
from .file_manager import FileManager
from src.correctors.pn_corrector import PeterNorvigCorrector
from src.dataset.languages import alphabets


def language_selector() -> str:
    """Select the language of the text to be corrected interactively."""
    print("Select the language of the text: en, bg")
    language = input("Enter language: ").strip()
    return language


def get_text_input() -> str | None:
    """
    Get text input from the user.
    Press Enter twice to process the input.
    Enter '!exit' to quit.
    """
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
    """
    Check if text corresponds to the selected language.
    Punctuation, whitespace and digits are ignored.
    """
    # Remove punctuation, whitespace, and digits.
    clean_text = re.sub(r'[\'\’.\-,?!":;\s\d]', '', text)
    return all(char.lower() in alphabets[language] for char in clean_text)


def process_text(text: str,
                 corrector: PeterNorvigCorrector,
                 display_corrected: bool = True) -> str:
    """
    Process (spell-correct) the input text.
    Splits the text preserving punctuation, corrects only the words, and then
    cleans up extra spaces before punctuation.
    """
    start_time = time.time()

    # Split text preserving punctuation.
    words_with_punct = re.findall(r'\w+|[\'\’.\-,?!":;\t\n]', text)

    # Correct only words, while preserving punctuation.
    corrected_words = []
    for word in tqdm(words_with_punct, desc="Processing text"):
        if re.match(r'\w+', word):
            corrected_words.append(corrector.correct(word))
        else:
            corrected_words.append(word)

    corrected_text = ' '.join(corrected_words)
    # Remove extra spaces before punctuation.
    corrected_text = re.sub(r'\s+([\'\’.\-,?!":;])', r'\1', corrected_text)

    end_time = time.time()
    if display_corrected:
        print("\nOriginal text:", text)
        print("Corrected text:", corrected_text)
    print(f"\nProcessing time: {(end_time - start_time):.4f} seconds\n")
    return corrected_text


async def process_file(file_path: str,
                       corrector: PeterNorvigCorrector,
                       language: str,
                       output_dir: str | None = None,
                       output_name: str | None = None) -> None:
    """
    Process a file containing text to be corrected.

    Before processing, check that every character in the file (ignoring
    punctuation, whitespace and digits) belongs to the selected language.
    If a disallowed character is found, the process is aborted with an error.

    If output_dir and/or output_name are provided the output file will be saved
    accordingly (keeping the original file extension).
    """
    start_time = time.time()
    manager = FileManager(file_path)
    text = manager.read_file()

    # Check if the content corresponds to the selected language.
    if not input_correlates_to_language(language, text):
        print("Error: The file contains characters that do not correspond",
              "to the selected language.")
        sys.exit(1)

    def process_line(line: str) -> str:
        return process_text(line, corrector, display_corrected=False)

    lines = text.split('\n')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_line, line) for line in lines]
        corrected_lines = [future.result() for future in futures]

    corrected_text = '\n'.join(corrected_lines)

    # Determine the output file name
    base = os.path.basename(file_path)
    if '.' in base:
        name_part, ext = base.rsplit('.', 1)
        ext = '.' + ext
    else:
        name_part = base
        ext = ''
    if output_name:
        out_filename = output_name + ext
    else:
        out_filename = name_part + "_corrected" + ext

    if output_dir:
        out_filename = os.path.join(output_dir, out_filename)

    manager.write_file(corrected_text, new_path=out_filename)
    end_time = time.time()
    print(f"\nTotal processing time: {(end_time - start_time):.4f} seconds")
    print(f"Corrected file saved to {out_filename}")


def interactive_loop(corrector: PeterNorvigCorrector,
                     language: str,
                     max_edit_distance: int) -> None:
    """
    Run an interactive loop where the user may enter text to be corrected.
    The user may also change the language interactively by entering '!change'.
    """
    while True:
        text = get_text_input()
        if text is None:
            break
        if text.strip() == "!change":
            language = language_selector()
            try:
                corrector = PeterNorvigCorrector(f"src/dataset/{language}.txt",
                                                 max_edit_distance)
            except FileNotFoundError:
                print("The dataset file was not found or is not yet added.")
            continue
        if not input_correlates_to_language(language, text):
            print("The text does not match the selected language.")
            continue
        if text:
            process_text(text, corrector)


def main() -> None:
    """
    The application supports two modes:
      - File mode: if an input file is specified via the -f/--file flag,
        the file will be processed and the corrected output will be saved.

      - Interactive mode: if no file is specified, the user can enter text
        to be corrected interactively.
    """
    desc = (
        "Spell Correction Application. "
        "Start the program by specifying the maximum edit distance"
    )
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-d", "--max-edit-distance",
        type=int,
        required=True,
        help="Maximum edit distance for corrections."
    )
    parser.add_argument(
        "-l", "--language",
        type=str,
        choices=["en", "bg"],
        default="en",
        help="Language of the text (default: en)."
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to the input file to be processed."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output directory path for the corrected file."
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        help="Name for the output file (without extension)."
    )

    args = parser.parse_args()

    try:
        corrector = PeterNorvigCorrector(f"src/dataset/{args.language}.txt",
                                         args.max_edit_distance)
    except FileNotFoundError:
        print("The dataset file for the selected language was not found.")
        return

    if args.file:
        asyncio.run(process_file(args.file, corrector, args.language,
                                 output_dir=args.output,
                                 output_name=args.name))
    else:
        interactive_loop(corrector, args.language, args.max_edit_distance)


if __name__ == '__main__':
    main()
