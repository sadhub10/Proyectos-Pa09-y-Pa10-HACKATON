from pathlib import Path
from functools import lru_cache
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = PROJECT_ROOT / "src" / "models" / "transformers" / "checkpoints" / "distilbert"

LABELS = ["Anxiety", "Depression", "Stress", "Suicidal"]

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
def load_transformer():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"No encontré el modelo en {MODEL_DIR}. "
            f"Entrena primero con src/models/transformers/train_transformer.py"
        )

    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
    return model, tokenizer

def _softmax(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x)
    ex = np.exp(x)
    return ex / ex.sum()

def predict_transformer_with_confidence(text: str):
    import torch

    model, tokenizer = load_transformer()

    text_en = translate_if_needed(text)
    if not text_en:
        return {
            "prediction_raw": "Normal",
            "prediction": "Normal",
            "text_en": "",
            "cleaned": "",
            "confidences_raw": {},
        }

    inputs = tokenizer(
        text_en,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    with torch.no_grad():
        logits = model(**inputs).logits[0].cpu().numpy()

    probs = _softmax(logits)
    pred_idx = int(np.argmax(probs))
    raw_pred = LABELS[pred_idx]

    confidence_dict = {LABELS[i]: float(probs[i]) for i in range(len(LABELS))}
    clinical_pred = clinical_states.get(raw_pred, raw_pred)

    return {
        "prediction_raw": raw_pred,
        "prediction": clinical_pred,
        "text_en": text_en,
        "cleaned": text_en,
        "confidences_raw": confidence_dict
    }
