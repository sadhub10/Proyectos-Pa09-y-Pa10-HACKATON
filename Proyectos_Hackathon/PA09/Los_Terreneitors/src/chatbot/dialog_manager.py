from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Tuple
import unicodedata
import re

from src.chatbot.policies import get_policy, CRISIS_LABELS
from src.chatbot.recommender import pick_recommendations, crisis_message


def _norm(text: str) -> str:
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text


# ================================
# CRISIS OVERRIDE (por texto)
# ================================
_CRISIS_PATTERNS = [
    r"\bterminar mi vida\b",
    r"\bquitarme la vida\b",
    r"\bme quiero morir\b",
    r"\bno quiero vivir\b",
    r"\bsuicid\w*\b",          # suicida, suicidio, suicidal
    r"\bmatarm(e|i)\b",
    r"\bhacerme dano\b",
    r"\bkill myself\b",
    r"\bend my life\b",
]

def _is_crisis_text(text: str) -> bool:
    t = _norm(text)
    if not t:
        return False
    return any(re.search(p, t) for p in _CRISIS_PATTERNS)


def _clamp01(x: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    return max(0.0, min(1.0, x))


def _parse_onset_answer(text: str) -> str:
    t = _norm(text)

    if "recient" in t or "hoy" in t or "ayer" in t or "hace poco" in t:
        return "reciente"

    if "varios" in t and ("dia" in t or "dias" in t):
        return "dias"

    if "dia" in t or "dias" in t:
        return "dias"

    if "semana" in t or "semanas" in t:
        return "semanas"

    if "mes" in t or "meses" in t or "mucho tiempo" in t:
        return "meses"

    return ""


def _parse_yes_no(text: str) -> str:
    """
    Devuelve: "yes" | "no" | ""
    """
    t = _norm(text)
    if not t:
        return ""
    if any(w in t for w in ["si", "sí", "claro", "ok", "estoy bien", "seguro", "segura", "estoy a salvo"]):
        return "yes"
    if any(w in t for w in ["no", "no estoy", "peligro", "no seguro", "no segura", "mal", "no a salvo"]):
        return "no"
    return ""


@dataclass
class ConversationState:
    last_prediction: str = "Normal"
    last_question: str = ""
    pending_slot: str = ""      # "safety" | "onset" | "trigger" | "support" | ""
    onset: str = ""             # "reciente" | "dias" | "semanas" | "meses" | ""
    trigger: str = ""           # texto libre (detonante)
    support: str = ""           # texto libre (apoyo)
    safety: str = ""            # "yes" | "no" | ""   (solo si hubo crisis)
    mentioned_sleep: bool = False
    mentioned_energy: bool = False
    mentioned_crying: bool = False


@dataclass
class ChatContext:
    user_text: str
    prediction_es: str
    confidence_01: float
    risk_score_01: float
    risk_level: str
    backend: str = "transformer"

def _update_state(state: ConversationState, prediction_es: str, user_text: str) -> Tuple[ConversationState, bool]:
    """
    Retorna (nuevo_estado, slot_filled?)
    """
    t = _norm(user_text)

    mentioned_sleep = state.mentioned_sleep or ("dorm" in t or "insom" in t)
    mentioned_energy = state.mentioned_energy or ("sin energia" in t or "cansad" in t or "agotad" in t)
    mentioned_crying = state.mentioned_crying or ("llor" in t)

    slot_filled = False
    onset = state.onset
    trigger = state.trigger
    support = state.support
    safety = state.safety
    pending = state.pending_slot

    if pending == "safety":
        parsed = _parse_yes_no(user_text)
        if parsed:
            safety = parsed
            pending = ""
            slot_filled = True

    elif pending == "onset":
        parsed = _parse_onset_answer(user_text)
        if parsed:
            onset = parsed
            pending = ""
            slot_filled = True

    elif pending == "trigger":
        if user_text.strip():
            trigger = user_text.strip()
            pending = ""
            slot_filled = True

    elif pending == "support":
        if user_text.strip():
            support = user_text.strip()
            pending = ""
            slot_filled = True

    return (
        ConversationState(
            last_prediction=prediction_es,
            last_question=state.last_question,
            pending_slot=pending,
            onset=onset,
            trigger=trigger,
            support=support,
            safety=safety,
            mentioned_sleep=mentioned_sleep,
            mentioned_energy=mentioned_energy,
            mentioned_crying=mentioned_crying,
        ),
        slot_filled,
    )


def _next_step_and_question(state: ConversationState, crisis: bool) -> Tuple[str, str]:
    """
    Devuelve (pending_slot, question)
    """

    # En crisis: primero seguridad, no onset
    if crisis:
        if not state.safety:
            return "safety", "Antes de seguir: ¿estás en un lugar seguro ahora mismo? (sí / no)"
        # si ya dijo "no", insistimos en recursos (sin preguntar onset)
        if state.safety == "no":
            return "safety", "Gracias por decirlo. ¿Puedes contactar a alguien ahora mismo o ir a un lugar con otra persona? (sí / no)"
        # si dijo "sí", seguimos con una pregunta suave y útil
        return "", "Gracias. Para entender mejor (en tu escenario de prueba): ¿esto ha sido un pensamiento pasajero o te ha pasado varias veces?"

    # No crisis: flujo normal por slots
    if not state.onset:
        return "onset", "¿Ha sido así por varios días o empezó recientemente?"

    if state.onset in {"reciente", "dias"} and not state.trigger:
        return "trigger", "¿Hubo algo que lo detonó recientemente (un evento, estrés fuerte, cambios)?"

    if state.onset in {"semanas", "meses"} and not state.support:
        return "support", "¿Has podido hablar con alguien de confianza o con un profesional sobre esto?"

    return "", "¿Qué parte de esto te está afectando más ahora mismo?"


def build_response(ctx: ChatContext, state: Optional[ConversationState] = None) -> Dict[str, Any]:
    state = state or ConversationState()

    forced_crisis = _is_crisis_text(ctx.user_text)
    prediction_es = "Ideación suicida" if forced_crisis else ctx.prediction_es
    crisis = forced_crisis or (prediction_es in CRISIS_LABELS)

    policy = get_policy(prediction_es)

    conf = _clamp01(ctx.confidence_01)
    risk = _clamp01(ctx.risk_score_01)
    if forced_crisis:
        risk = max(risk, 0.90)

    state2, slot_filled = _update_state(state, prediction_es, ctx.user_text)
    pending, question = _next_step_and_question(state2, crisis=crisis)
    state2.pending_slot = pending
    state2.last_question = question

    same_label = (state.last_prediction == prediction_es)

    # 1) Respuesta corta si solo está llenando un slot (no repetir sugerencias)
    if slot_filled and same_label:
        bridge = "Gracias por aclararlo."
        if state.pending_slot == "onset":
            if state2.onset == "dias":
                bridge = "Gracias, entonces lleva **varios días**."
            elif state2.onset == "reciente":
                bridge = "Gracias, entonces empezó **recientemente**."
            elif state2.onset == "semanas":
                bridge = "Gracias, entonces ya lleva **semanas**."
            elif state2.onset == "meses":
                bridge = "Gracias, entonces ya lleva **meses**."
        elif state.pending_slot == "safety":
            if state2.safety == "yes":
                bridge = "Gracias por confirmarlo. Me alegra que estés en un lugar seguro."
            elif state2.safety == "no":
                bridge = "Gracias por decirlo. Tu seguridad es lo primero."

        reply = f"{bridge}\n\n{question}"

        if crisis and state2.safety == "no":
            reply += "\n\n" + crisis_message()

        return {
            "reply": reply,
            "recommendations": [],
            "crisis": bool(crisis),
            "state": asdict(state2),
            "meta": {
                "backend": ctx.backend,
                "prediction": prediction_es,
                "confidence_01": conf,
                "risk_score_01": risk,
                "risk_level": ctx.risk_level,
                "policy_style": policy.style,
                "forced_crisis": bool(forced_crisis),
            }
        }

    # 2) Mensaje principal más conversacional (sin “Según el análisis…” arriba)
    tone_map = {
        "Normal": "Gracias por compartirlo.",
        "Estrés": "Se nota que has estado bajo mucha carga.",
        "Ansiedad": "Siento que estés pasando por esto.",
        "Depresión": "Lo siento, suena realmente pesado.",
        "Ideación suicida": "Gracias por decirlo. Tu seguridad es lo más importante."
    }
    tone = tone_map.get(prediction_es, "Gracias por contarlo.")

    # 3) Sugerencias: menos cantidad, y presentadas como “mientras me respondes…”
    if crisis:
        recs = pick_recommendations("Ideación suicida", ctx.risk_level, n=3)
        reply = (
            f"{tone}\n\n"
            f"{question}\n\n"
            f"Por favor busca apoyo inmediato:\n"
            f"{crisis_message()}\n\n"
            f"Si te sirve ahora mismo (paso a paso):\n- " + "\n- ".join(recs)
        )
    else:
        recs = pick_recommendations(prediction_es, ctx.risk_level, n=2)  # <- 2 en vez de 3
        reply = (
            f"{tone}\n\n"
            f"{question}\n\n"
            f"Si te sirve mientras me respondes:\n- " + "\n- ".join(recs)
        )

    return {
        "reply": reply,
        "recommendations": recs,
        "crisis": bool(crisis),
        "state": asdict(state2),
        "meta": {
            "backend": ctx.backend,
            "prediction": prediction_es,
            "confidence_01": conf,
            "risk_score_01": risk,
            "risk_level": ctx.risk_level,
            "policy_style": policy.style,
            "forced_crisis": bool(forced_crisis),
        }
    }

