import time
import re
from correctors.pn_corrector import PeterNorvigCorrector
from dataset.languages import alphabets
from tqdm import tqdm


def language_selector() -> str:
    print("Select the language of the text:")
    print("1. en")
    print("2. bg")
    print("3. de")
    language = input("Enter the number of the language: ")
    return language


def get_text_input() -> str | None:
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
    # Remove punctuation before checking language
    clean_text = re.sub(r'[.,?!":;\s]', '', text)
    for char in clean_text:
        if char.lower() not in alphabets[language]:
            return False
    return True


def process_text(text: str, corrector: PeterNorvigCorrector) -> str:
    start_time = time.time()
    # Split text preserving punctuation
    words_with_punct = re.findall(r'\w+|[.,?!":;]', text)
    # Correct only words, preserve punctuation
    corrected_words = []
    for word in tqdm(
        list(
            filter(
                lambda x: re.match(r'\w+', x), words_with_punct
                )),
            desc="Processing text"
            ):

        if re.match(r'\w+', word):
            corrected_words.append(corrector.correct(word))
        else:
            corrected_words.append(word)

    corrected_text = ' '.join(corrected_words)
    # Clean up extra spaces before punctuation
    corrected_text = re.sub(r'\s+([.,?!":;])', r'\1', corrected_text)
    end_time = time.time()
    print("\nOriginal text:", text)
    print("Corrected text:", corrected_text)
    print(f"Processing time: {(end_time - start_time):.4f} seconds\n")
    return corrected_text


def setup_corrector(depth: str) -> tuple[str, PeterNorvigCorrector]:
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


def main():
    depth = input("Enter the maximum edit distance: ")
    selected_language, corrector = setup_corrector(depth)

    while True:
        print("\nType '!change' to change language or enter your text:")
        text = get_text_input()
        if text is None:
            return
        if text == "!change":
            selected_language, corrector = setup_corrector(depth)
            continue
        if not input_correlates_to_language(selected_language, text):
            print("The text does not match the selected language.")
            continue
        if text:
            process_text(text, corrector)


if __name__ == '__main__':
    main()
