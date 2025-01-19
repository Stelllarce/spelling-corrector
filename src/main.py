from correctors.peter_norvig import PeterNorvigCorrector
import time


def main():
    depth = input("Enter the maximum edit distance: ")
    corrector = PeterNorvigCorrector("dataset/db.txt", int(depth))
    while True:
        print("Enter text (press Enter twice to process, or '!exit' to quit):")
        text = ""
        while True:
            line = input()
            if line.strip() == "!exit":
                return
            if line.strip() == "":
                break
            text += line + " "
        if text.strip():
            start_time = time.time()
            words = text.split()
            corrected_words = [corrector.correct(word) for word in words]
            corrected_text = " ".join(corrected_words)
            end_time = time.time()
            print("\nOriginal text:", text)
            print("Corrected text:", corrected_text)
            print(f"Processing time: {(end_time - start_time):.4f} seconds\n")


if __name__ == '__main__':
    main()
