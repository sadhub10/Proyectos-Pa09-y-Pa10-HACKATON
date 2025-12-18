import joblib
from pathlib import Path
from src.features.audio_features import extract_audio_features

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "audio_model.pkl"
SCALER_PATH = BASE_DIR / "audio_scaler.pkl"

def predict_audio_with_confidence(audio_path: str):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    features = extract_audio_features(audio_path)
    features = scaler.transform([features])

    probs = model.predict_proba(features)[0]
    labels = model.classes_

    confidences = {
        labels[i]: float(probs[i])
        for i in range(len(labels))
    }

    pred = labels[probs.argmax()]

    return {
        "prediction": pred,
        "confidences_raw": confidences
    }
