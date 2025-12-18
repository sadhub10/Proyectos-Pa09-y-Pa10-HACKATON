import streamlit as st
import tempfile
from src.inference.predict_audio import predict_audio_unified

st.set_page_config(page_title="Audio Analysis", layout="centered")
st.title("Fase 2 - Análisis Emocional por Audio")

uploaded = st.file_uploader("Sube un archivo WAV", type=["wav"])

if uploaded:
    st.audio(uploaded)

    if st.button("Analizar Audio"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded.read())
            audio_path = tmp.name

        result = predict_audio_unified(audio_path)

        st.subheader("Resultado")
        st.write(f"**Predicción:** {result['prediction']}")

        st.subheader("Confianzas")
        st.json(result["confidences_raw"])
