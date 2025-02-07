from flask import Flask, request, jsonify
from src.correctors.pn_corrector import PeterNorvigCorrector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATASET_PATH = os.path.join("src", "dataset", "en.txt")

corrector = PeterNorvigCorrector(DATASET_PATH)


@app.route("/correct", methods=["GET"])
def correct_word():
    """API Endpoint: Returns spelling suggestions for a given word"""
    word = request.args.get("word", "").strip()

    if not word:
        return jsonify({"error": "No word provided"}), 400

    suggestions = corrector.candidates(word)

    return jsonify({"word": word, "suggestions": suggestions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
