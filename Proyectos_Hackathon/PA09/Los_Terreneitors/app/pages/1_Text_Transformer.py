import streamlit as st
import pandas as pd
import plotly.express as px
from src.models.transformers.predict_transformer import predict_transformer_with_confidence

st.set_page_config(page_title="Transformer (DistilBERT)", layout="wide")
st.title("Transformer (DistilBERT)")

# ================================
# JUSTIFICACIÓN / PARA QUÉ SIRVE
# ================================
with st.expander("¿Para qué sirve este módulo? (Justificación)", expanded=True):
    st.markdown(
        """
**¿Por qué usar un Transformer (DistilBERT) y no solo el baseline?**

Un Transformer es útil porque entiende el texto **con contexto**, no solo por palabras sueltas.  
Esto ayuda cuando la emoción depende del **sentido de la frase**, la negación, o expresiones comunes.

**Qué aporta este módulo:**
- **Comprensión contextual:** diferencia frases como “no estoy bien” vs “estoy bien”, o “ya no puedo más” aunque no diga “depresión”.
- **Mejor generalización:** suele funcionar mejor con textos “nuevos” (formas diferentes de expresar lo mismo).
- **Menos dependencia de keywords:** no se basa tanto en bigramas/palabras exactas.
- **Base para escalabilidad:** es el paso natural hacia un sistema más “inteligente” (y luego integrar riesgos y chatbot).

**¿Por qué está separado si el dashboard ya muestra predicción?**
Este apartado sirve como **laboratorio/inspector**:
- Ver **confidencias por clase** de manera clara.
- Probar frases rápidas sin ruido del dashboard.
- Diagnosticar casos donde el modelo confunde clases (ej: Depresión vs Ideación suicida).
        """
    )

st.divider()

# ================================
# INPUT
# ================================
text = st.text_area("Escribe un texto:", height=140, placeholder="Ej: No puedo dormir y siento mucha ansiedad...")

col_a, col_b = st.columns([1, 1])
with col_a:
    analyze = st.button("Analizar", use_container_width=True)
with col_b:
    show_debug = st.checkbox("Mostrar detalles técnicos (debug)", value=False)

# ================================
# OUTPUT
# ================================
if analyze:
    if not text.strip():
        st.warning("Escribe un texto antes de analizar.")
        st.stop()

    with st.spinner("Analizando con DistilBERT..."):
        result = predict_transformer_with_confidence(text)

    prediction = result.get("prediction", "N/A")
    confidences = result.get("confidences_raw", {})

    st.subheader("Resultado")
    st.success(f"Predicción: **{prediction}**")

    if confidences:
        # Tabla
        df = pd.DataFrame(
            [{"Etiqueta": k, "Confianza": float(v)} for k, v in confidences.items()]
        ).sort_values("Confianza", ascending=False)

        # Métrica principal
        top_label = df.iloc[0]["Etiqueta"]
        top_conf = float(df.iloc[0]["Confianza"])
        st.metric("Confianza más alta", f"{top_conf*100:.1f}%", help=f"Clase top: {top_label}")

        # Gráfica (más útil que JSON)
        st.subheader("Confidencias por clase")
        fig = px.bar(
            df,
            x="Etiqueta",
            y="Confianza",
            title="Distribución de confianza (Transformer)"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Explicación corta (por qué se ve esto aquí)
        st.info(
            "Este gráfico ayuda a entender si el modelo está **seguro** o si hay **ambigüedad** "
            "(por ejemplo, dos clases con valores parecidos)."
        )
    else:
        st.warning("El modelo no devolvió confidencias por clase.")

    if show_debug:
        st.subheader("Detalles (debug)")
        st.json({
            "prediction_raw": result.get("prediction_raw"),
            "text_en": result.get("text_en"),
            "cleaned": result.get("cleaned"),
            "confidences_raw": result.get("confidences_raw"),
        })

# ================================
# NOTA FINAL
# ================================
st.caption(
    "Nota: Las 'confidencias' son una aproximación (softmax sobre logits). Úsalas como referencia comparativa, "
    "no como probabilidad calibrada."
)
