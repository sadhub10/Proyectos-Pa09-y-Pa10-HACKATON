from src.models.baseline.service import predict_with_confidence

def predict_text(text: str) -> str:
    """
    Wrapper compatible con Fase 1.
    Devuelve la predicción clínica (en español).
    """
    if text is None:
        return "Normal"

    text = str(text).strip()
    if not text:
        return "Normal"

    try:
        result = predict_with_confidence(text)
        return result.get("prediction", "Normal")
    except Exception:
        return "Normal"
