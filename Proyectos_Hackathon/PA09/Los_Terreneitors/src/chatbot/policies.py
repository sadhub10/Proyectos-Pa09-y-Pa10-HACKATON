from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ChatPolicy:
    label: str
    style: str
    do: List[str]
    avoid: List[str]


POLICIES: Dict[str, ChatPolicy] = {
    "Normal": ChatPolicy(
        label="Normal",
        style="cálido, positivo y preventivo",
        do=[
            "reforzar hábitos saludables",
            "sugerir autocuidado ligero",
            "invitar a describir contexto si desea"
        ],
        avoid=[
            "alarmar sin motivo",
            "dar diagnósticos"
        ],
    ),
    "Estrés": ChatPolicy(
        label="Estrés",
        style="práctico, orientado a manejo del día",
        do=[
            "validar carga y cansancio",
            "sugerir pausas y priorización",
            "proponer una técnica breve de respiración"
        ],
        avoid=[
            "minimizar ('no es nada')",
            "dar consejos médicos"
        ],
    ),
    "Ansiedad": ChatPolicy(
        label="Ansiedad",
        style="calmado, contenedor y estructurado",
        do=[
            "normalizar la sensación",
            "proponer grounding / respiración",
            "reducir incertidumbre con pasos pequeños"
        ],
        avoid=[
            "preguntas demasiado invasivas",
            "prometer resultados"
        ],
    ),
    "Depresión": ChatPolicy(
        label="Depresión",
        style="empático, suave y de acompañamiento",
        do=[
            "validar emoción y fatiga",
            "sugerir activación conductual pequeña",
            "recomendar apoyo social/profesional si persiste"
        ],
        avoid=[
            "frases tipo 'échale ganas'",
            "culpabilizar"
        ],
    ),
    "Ideación suicida": ChatPolicy(
        label="Ideación suicida",
        style="directo, seguro y de contención",
        do=[
            "priorizar seguridad inmediata",
            "recomendar ayuda profesional urgente",
            "invitar a contactar a alguien de confianza"
        ],
        avoid=[
            "dejarlo solo con ejercicios",
            "dar instrucciones peligrosas"
        ],
    ),
}


CRISIS_LABELS = {"Ideación suicida"}


def get_policy(prediction_es: str) -> ChatPolicy:
    return POLICIES.get(prediction_es, POLICIES["Normal"])

import re

_CRISIS_PATTERNS = [
    r"\bterminar mi vida\b",
    r"\bquitarme la vida\b",
    r"\bsuicid\w*\b",          # suicida, suicidio
    r"\bno quiero vivir\b",
    r"\bme quiero morir\b",
    r"\bhacerme daño\b",
    r"\bmatarm(e|i)\b",
    r"\bend my life\b",
    r"\bkill myself\b",
    r"\bsuicid\w*\b",
]

def is_crisis_text(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return False
    return any(re.search(p, t) for p in _CRISIS_PATTERNS)

