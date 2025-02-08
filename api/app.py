from flask import Flask, request, jsonify
from src.correctors.pn_corrector import PeterNorvigCorrector
from flask_cors import CORS
import os
from src.dataset.language_detector import SimpleLanguageDetector
from typing import Optional

detector = SimpleLanguageDetector()

app = Flask(__name__)
CORS(app)

SUPPORTED_LANGUAGES = {
    "en": os.path.join("src", "dataset", "en.txt"),
    "bg": os.path.join("src", "dataset", "bg.txt")
}

correctors = {}


def get_corrector_for_lang(lang: str) -> Optional[PeterNorvigCorrector]:
    """ Return a PeterNorvigCorrector instance for the given language. """
    if lang not in SUPPORTED_LANGUAGES:
        return None
    if lang not in correctors:
        dataset_path = SUPPORTED_LANGUAGES[lang]
        correctors[lang] = PeterNorvigCorrector(dataset_path)
    return correctors[lang]


@app.route("/correct", methods=["GET"])
def correct_word():
    """
    API Endpoint: Returns spelling suggestions for a given word.
    Query parameters:
      - word: the word to check (required)
    """
    word = request.args.get("word", "").strip()
    if not word:
        return jsonify({"error": "No word provided"}), 400

    # This line is here if I ever implement a grammar model
    # sample_text = request.args.get("text", "").strip() or word

    lang = detector.detect(word)
    if lang is None or lang not in SUPPORTED_LANGUAGES:
        return jsonify({"error": "Language not recognized"}), 400

    corrector = get_corrector_for_lang(lang)
    suggestions = corrector.candidates(word)[:5]
    print(f"Word: {word}, Language: {lang}, Suggestions: {suggestions}")
    return jsonify({
        "word": word,
        "suggestions": suggestions
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
