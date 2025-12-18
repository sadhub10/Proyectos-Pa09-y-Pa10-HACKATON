import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from src.data.logging import LOG_PATH
from src.models.risk.predict_risk import score_from_prediction, risk_level

st.set_page_config(page_title="Risk Prediction", layout="wide")
st.title("Predicción / Alertas")

# ================================
# JUSTIFICACIÓN / PARA QUÉ SIRVE
# ================================
with st.expander("¿Para qué sirve este módulo? (Justificación)", expanded=True):
    st.markdown(
        """
**¿Qué es “Risk Prediction” aquí?**  
No es un “modelo nuevo” necesariamente: es una **capa de interpretación y monitoreo** que convierte
las predicciones del clasificador (ej. Depresión, Ansiedad, Ideación suicida) + su confianza
en un **score de riesgo** que se puede **seguir en el tiempo**.

**Qué aporta este módulo:**
- **Alertas tempranas:** no solo “qué emoción” sino **qué tan crítico** puede ser el caso.
- **Tendencia temporal:** ver si el riesgo **sube, baja o se mantiene** en varios análisis.
- **Soporte para decisiones:** prioriza casos (ej. “Ideación suicida” con alta confianza).
- **Base del sistema escalable:** permite que el dashboard y el chatbot reaccionen de forma consistente
  (p. ej., activar recursos de crisis cuando el riesgo es alto).

**¿Por qué está separado si el dashboard ya muestra riesgo?**  
Este apartado funciona como **monitor/bitácora**:
- Ver el historial completo (sesión o CSV).
- Confirmar que el logging está funcionando.
- Visualizar la curva de riesgo y el último estado de forma clara.
        """
    )

st.divider()

# ================================
# 1) Primero intenta leer CSV (persistente)
# ================================
df = None
data_source = None

if LOG_PATH.exists():
    df = pd.read_csv(LOG_PATH)
    data_source = f"CSV: {LOG_PATH}"
else:
    # ================================
    # 2) Si no hay CSV, usa historial de la sesión (memoria)
    # ================================
    history = st.session_state.get("history", [])

    if history:
        df = pd.DataFrame(history)
        data_source = "Sesión actual (st.session_state.history)"

        # Normalizar columnas mínimas esperadas
        if "timestamp" not in df.columns:
            df["timestamp"] = list(range(1, len(df) + 1))

        # Tu dashboard guarda confidence en 0..100 (float)
        if "confidence" in df.columns:
            df["confidence_01"] = df["confidence"].astype(float) / 100.0
        else:
            df["confidence_01"] = 0.0

        # Calcular riesgo en base a prediction + confidence
        if "prediction" in df.columns:
            df["risk_score"] = df.apply(
                lambda r: score_from_prediction(str(r["prediction"]), float(r["confidence_01"])),
                axis=1
            )
            df["risk_level"] = df["risk_score"].apply(risk_level)
        else:
            df["risk_score"] = 0.0
            df["risk_level"] = "NORMAL"

    else:
        st.info(
            "Aún no hay registros.\n\n"
            "- Si quieres persistencia: genera el CSV desde el dashboard (logging).\n"
            "- Si quieres verlo por sesión: vuelve al dashboard y realiza 1 análisis sin recargar la app."
        )
        st.stop()

st.caption(f"Fuente de datos: {data_source}")

# ================================
# CONTROLES (opcional pero útil)
# ================================
col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
with col_f1:
    n_last = st.number_input("Mostrar últimos N registros", min_value=10, max_value=500, value=50, step=10)
with col_f2:
    only_high = st.checkbox("Solo riesgo ALTO/CRÍTICO", value=False)
with col_f3:
    show_debug = st.checkbox("Ver columnas (debug)", value=False)

df_view = df.copy()

if "risk_level" in df_view.columns and only_high:
    df_view = df_view[df_view["risk_level"].astype(str).isin(["ALTO", "CRÍTICO", "CRITICO"])].copy()

# ================================
# KPIs
# ================================
st.subheader("Resumen")
c1, c2, c3, c4 = st.columns(4)

total = int(len(df_view))
last_score = float(df_view["risk_score"].iloc[-1]) if "risk_score" in df_view.columns and total else 0.0
last_level = str(df_view["risk_level"].iloc[-1]) if "risk_level" in df_view.columns and total else "NORMAL"
max_score = float(df_view["risk_score"].max()) if "risk_score" in df_view.columns and total else 0.0

c1.metric("Registros", total)
c2.metric("Último riesgo", f"{last_score:.3f}")
c3.metric("Nivel actual", last_level)
c4.metric("Riesgo máximo", f"{max_score:.3f}")

# ================================
# TABLA
# ================================
st.subheader("Registros")
st.dataframe(df_view.tail(int(n_last)), use_container_width=True, hide_index=True)

if show_debug:
    st.caption(f"Columnas detectadas: {list(df_view.columns)}")

# ================================
# GRÁFICAS
# ================================
if "risk_score" in df_view.columns:
    st.subheader("Tendencia de Riesgo")
    fig = px.line(
        df_view,
        x="timestamp",
        y="risk_score",
        title="Riesgo a lo largo del tiempo"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Distribución por nivel
    if "risk_level" in df_view.columns:
        st.subheader("Distribución de niveles de riesgo")
        counts = df_view["risk_level"].astype(str).value_counts().reset_index()
        counts.columns = ["Nivel", "Cantidad"]
        fig2 = px.bar(counts, x="Nivel", y="Cantidad", title="Conteo por nivel de riesgo")
        st.plotly_chart(fig2, use_container_width=True)

    # Riesgo por emoción (si existe prediction)
    if "prediction" in df_view.columns:
        st.subheader("Riesgo promedio por emoción detectada")
        grp = (
            df_view.groupby("prediction", as_index=False)["risk_score"]
            .mean()
            .sort_values("risk_score", ascending=False)
        )
        fig3 = px.bar(grp, x="prediction", y="risk_score", title="Riesgo promedio por etiqueta")
        st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "Interpretación: un riesgo que sube de forma sostenida (aunque la emoción se repita) "
        "es una señal para activar alertas o recomendaciones más fuertes."
    )
else:
    st.warning("No encuentro la columna 'risk_score'. Revisa el logging del dashboard.")
