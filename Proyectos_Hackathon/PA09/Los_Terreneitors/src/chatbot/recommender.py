from __future__ import annotations
from typing import List, Dict

DEFAULT_RESOURCES: Dict[str, List[str]] = {
    "Normal": [
        "Escribe 3 cosas que salieron bien hoy (1 minuto).",
        "Camina 10 minutos o estira el cuerpo 3–5 minutos.",
        "Organiza mañana con 1 prioridad principal."
    ],
    "Estrés": [
        "Técnica 4-7-8: inhala 4s, sostén 7s, exhala 8s (3 rondas).",
        "Lista rápida: 3 tareas (urgente/importante) y delega o pospone 1.",
        "Pausa activa: 2 minutos de estiramiento de cuello/hombros."
    ],
    "Ansiedad": [
        "Grounding 5-4-3-2-1: 5 cosas que ves, 4 que sientes, 3 que oyes, 2 que hueles, 1 que saboreas.",
        "Respiración cuadrada: 4s inhala, 4s sostén, 4s exhala, 4s sostén (4 ciclos).",
        "Escribe la preocupación y al lado: '¿qué está bajo mi control hoy?'"
    ],
    "Depresión": [
        "Paso mínimo: ducha o lavarte la cara + cambiarte de ropa (si puedes).",
        "Una acción de conexión: enviar un mensaje a alguien de confianza.",
        "Actividad pequeña: 10 minutos de luz solar o caminar suave."
    ],
    "Ideación suicida": [
        "Contacta a alguien de confianza ahora mismo (familia/amigo).",
        "Busca ayuda profesional urgente o servicios de emergencia.",
        "Si estás en peligro inmediato, acude a emergencias."
    ],
}


def pick_recommendations(prediction_es: str, risk_level: str, n: int = 3) -> List[str]:
    """
    Retorna recomendaciones contextuales según emoción y riesgo.
    risk_level: NORMAL|BAJO|MEDIO|ALTO
    """
    base = DEFAULT_RESOURCES.get(prediction_es, DEFAULT_RESOURCES["Normal"])

    # Si riesgo es alto, prioriza seguridad / apoyo
    if risk_level == "ALTO" and prediction_es != "Ideación suicida":
        extra = [
            "Si sientes que la situación te supera, busca apoyo profesional o habla con alguien de confianza hoy.",
            "Reducir estímulos: baja brillo, hidrátate y haz una pausa de 3 minutos."
        ]
        merged = extra + base
    else:
        merged = base

    return merged[:n]


def crisis_message() -> str:
    return (
        "Si estás en crisis o sientes que podrías hacerte daño:\n\n"
        "- **Panamá:** llama al **169 (MINSA)**\n"
        "- **Internacional:** befrienders.org\n"
        "- Si estás en peligro inmediato, **acude a emergencias** o llama a un servicio local.\n\n"
        "No estás solo/a. Pedir ayuda es un paso valiente."
    )
