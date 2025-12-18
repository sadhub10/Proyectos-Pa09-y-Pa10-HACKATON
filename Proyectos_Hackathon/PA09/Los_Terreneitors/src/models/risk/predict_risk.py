from __future__ import annotations
from typing import Dict, List, Any


# Pesos simples por etiqueta (puedes ajustarlos después)
DEFAULT_WEIGHTS: Dict[str, float] = {
    "Normal": 0.00,
    "Estrés": 0.35,
    "Ansiedad": 0.45,
    "Depresión": 0.65,
    "Ideación suicida": 1.00,
}


def score_from_prediction(prediction_es: str, confidence_01: float) -> float:
    """
    Calcula un score de riesgo 0..1.
    - prediction_es: etiqueta en español (Ansiedad, Depresión, etc.)
    - confidence_01: confianza en rango 0..1
    """
    base = float(DEFAULT_WEIGHTS.get(prediction_es, 0.0))
    c = max(0.0, min(1.0, float(confidence_01)))
    # Ponderación suave por confianza
    return base * (0.5 + 0.5 * c)


def risk_level(score_01: float) -> str:
    """
    Nivel cualitativo según score.
    """
    s = max(0.0, min(1.0, float(score_01)))
    if s >= 0.80:
        return "ALTO"
    if s >= 0.55:
        return "MEDIO"
    if s >= 0.30:
        return "BAJO"
    return "NORMAL"


def score_from_recent(history: List[Dict[str, Any]], window: int = 5) -> Dict[str, float | str]:
    """
    Calcula riesgo agregado usando las últimas N predicciones del historial.
    Espera items con:
      - prediction (español)
      - confidence (0..100) o (0..1)
    Devuelve:
      - risk_avg: promedio de riesgo
      - risk_last: último riesgo
      - level: nivel del promedio
    """
    if not history:
        return {"risk_avg": 0.0, "risk_last": 0.0, "level": "NORMAL"}

    recent = history[-window:] if len(history) > window else history

    risks = []
    for item in recent:
        pred = str(item.get("prediction", "Normal"))
        conf = item.get("confidence", 0.0)

        # admitir 0..100 o 0..1
        conf = float(conf) if conf is not None else 0.0
        conf_01 = conf / 100.0 if conf > 1.0 else conf

        risks.append(score_from_prediction(pred, conf_01))

    risk_last = float(risks[-1]) if risks else 0.0
    risk_avg = float(sum(risks) / len(risks)) if risks else 0.0

    return {
        "risk_avg": risk_avg,
        "risk_last": risk_last,
        "level": risk_level(risk_avg),
    }
