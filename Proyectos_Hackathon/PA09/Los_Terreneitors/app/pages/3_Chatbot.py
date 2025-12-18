import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from src.inference.predict_text import predict_text_unified
from src.models.risk.predict_risk import score_from_prediction, risk_level
from src.chatbot.dialog_manager import ChatContext, ConversationState, build_response

st.set_page_config(page_title="Chatbot Emocional", layout="wide")
st.title("Chatbot Emocional")

st.sidebar.subheader("Motor de IA")
backend = st.sidebar.radio(
    "Selecciona el motor:",
    options=["baseline", "transformer"],
    index=1,
    format_func=lambda x: "Baseline (SVM + TF-IDF)" if x == "baseline" else "Transformer (DistilBERT)"
)
col1, col2 = st.sidebar.columns(2)
if col1.button("Limpiar chat", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.chat_state = ConversationState()
    st.rerun()
debug = col2.toggle("Debug", value=False)


st.sidebar.caption("El chatbot usa predicción + score de riesgo + estado de conversación.")

# Historial y estado (memoria)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [{"role": "user"/"assistant", "content": "...", "meta": {...}}]

if "chat_state" not in st.session_state:
    st.session_state.chat_state = ConversationState()


# Render chat
for m in st.session_state.chat_history:
    role = "user" if m["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(m["content"])
        if debug and m.get("meta"):
            with st.expander("Detalles (debug)"):
                st.json(m["meta"])

prompt = st.chat_input("Escribe tu mensaje...")

if prompt:
    user_text = prompt.strip()
    if not user_text:
        st.stop()

    # Mostrar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_text})

    # Inferencia
    with st.spinner("Analizando y generando respuesta..."):
        result = predict_text_unified(user_text, mode=backend)

        pred_es = result.get("prediction", "Normal")
        conf_raw = result.get("confidences_raw", {})
        conf_01 = max(conf_raw.values()) if conf_raw else 0.0

        risk = score_from_prediction(pred_es, conf_01)
        lvl = risk_level(risk)

        ctx = ChatContext(
            user_text=user_text,
            prediction_es=pred_es,
            confidence_01=conf_01,
            risk_score_01=risk,
            risk_level=lvl,
            backend=backend,
        )

        bot = build_response(ctx, st.session_state.chat_state)

        # Actualiza “memoria”
        st.session_state.chat_state = ConversationState(**bot["state"])

    st.session_state.chat_history.append({"role": "assistant", "content": bot["reply"], "meta": bot["meta"]})
    st.rerun()
