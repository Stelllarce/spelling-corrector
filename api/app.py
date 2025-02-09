import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.correctors.pn_corrector import PeterNorvigCorrector
from src.dataset.language_detector import SimpleLanguageDetector


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


detector = SimpleLanguageDetector()

SUPPORTED_LANGUAGES = {
    "en": os.path.join("src", "dataset", "en.txt"),
    "bg": os.path.join("src", "dataset", "bg.txt")
}

correctors = {}


def get_corrector_for_lang(lang: str) -> Optional[PeterNorvigCorrector]:
    """
    Return a PeterNorvigCorrector instance for the given language.
    """
    if lang not in SUPPORTED_LANGUAGES:
        return None
    if lang not in correctors:
        dataset_path = SUPPORTED_LANGUAGES[lang]
        correctors[lang] = PeterNorvigCorrector(dataset_path, max_distance=3)
    return correctors[lang]


@app.get("/correct")
async def correct_word(
    word: str = Query(..., description="The word to check")
) -> dict:
    """
    API Endpoint: Returns spelling suggestions for a given word.
    Query parameters:
      - word: the word to check.
    """
    word = word.strip()
    if not word:
        raise HTTPException(status_code=400, detail="No word provided")
    lang = detector.detect(word)
    if lang is None or lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400, detail="Language not recognized"
        )
    corrector = get_corrector_for_lang(lang)
    suggestions = corrector.candidates(word)[:5]
    print(f"Word: {word}, Language: {lang}, Suggestions: {suggestions}")
    return {"word": word, "suggestions": suggestions}


class UpdateRequest(BaseModel):
    word: str
    correction: str


@app.post("/update")
async def update_correction(data: UpdateRequest) -> dict:
    """
    API Endpoint: Updates the cache with the correction confirmed by the
    user.
    Expects a JSON body with:
      - word: the word typed by the user.
      - correction: the user-chosen correction.
    """
    word = data.word.strip()
    correction = data.correction.strip()
    if not word or not correction:
        raise HTTPException(
            status_code=400, detail="No word or correction provided"
        )
    lang = detector.detect(word)
    if lang is None or lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400, detail="Language not recognized"
        )
    corrector = get_corrector_for_lang(lang)
    corrector.update_cache(word, correction)
    return {"message": "Cache updated."}


if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=5000, reload=True)
