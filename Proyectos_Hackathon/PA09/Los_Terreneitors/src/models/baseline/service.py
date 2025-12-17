import numpy as np
import joblib
from functools import lru_cache
from pathlib import Path

from src.features.vectorizer import load_vectorizer
from src.data.preprocess import clean_text

# service.py está en: project/src/models/baseline/service.py
# project root = parents[3]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "src" / "models" / "saved" / "best_model.pkl"

clinical_states = {
    "Anxiety": "Ansiedad",
    "Depression": "Depresión",
    "Stress": "Estrés",
    "Suicidal": "Ideación suicida"
}

@lru_cache(maxsize=512)
def _cached_translate(text: str) -> str:
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text

def translate_if_needed(text: str) -> str:
    text = "" if text is None else str(text).strip()
    if not text:
        return text
    return _cached_translate(text)

@lru_cache(maxsize=1)
def load_baseline():
    """
    Carga modelo + vectorizador una sola vez por ejecución.
    """
    model = joblib.load(MODEL_PATH)
    vectorizer = load_vectorizer()
    return model, vectorizer

def predict_with_confidence(text: str):
    model, vectorizer = load_baseline()

    text_en = translate_if_needed(text)
    cleaned = clean_text(text_en)
    vec = vectorizer.transform([cleaned])

    raw_pred = model.predict(vec)[0]

    decision_values = model.decision_function(vec)[0]
    exp_values = np.exp(decision_values - np.max(decision_values))
    probs = exp_values / exp_values.sum()

    confidence_dict = {label: float(prob) for label, prob in zip(model.classes_, probs)}
    clinical_pred = clinical_states.get(raw_pred, raw_pred)

    return {
        "prediction_raw": raw_pred,
        "prediction": clinical_pred,
        "text_en": text_en,
        "cleaned": cleaned,
        "confidences_raw": confidence_dict
    }
