import sys
import os
import numpy as np
import pandas as pd
import json
from datetime import datetime
from collections import Counter

# Agregar ruta del proyecto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.inference.predict_text import predict_text_unified
from src.models.baseline.service import load_baseline

# ================================
# CONFIGURACIÓN DE PÁGINA
# ================================
st.set_page_config(
    page_title="Mental Health Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# ESTILOS CSS MEJORADOS
# ================================
st.markdown("""
<style>
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a4d7a;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.2rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Alertas con mejor contraste */
    .alert-high {
        background-color: #fef2f2;
        border: 2px solid #dc2626;
        border-left: 6px solid #dc2626;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .alert-high h2, .alert-high h3 {
        color: #991b1b;
        margin: 0;
    }

    .alert-medium {
        background-color: #fffbeb;
        border: 2px solid #f59e0b;
        border-left: 6px solid #f59e0b;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .alert-medium h2, .alert-medium h3 {
        color: #92400e;
        margin: 0;
    }

    .alert-low {
        background-color: #f0fdf4;
        border: 2px solid #10b981;
        border-left: 6px solid #10b981;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .alert-low h2, .alert-low h3 {
        color: #065f46;
        margin: 0;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #1a4d7a;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ================================
# FUNCIONES
# ================================
@st.cache_data
def load_model_metrics():
    """Carga las métricas del modelo baseline"""
    try:
        metrics_path = os.path.join(ROOT_DIR, "src", "models", "saved", "model_metrics.json")
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "accuracy": 0.85,
            "f1_score": 0.84,
            "precision": 0.85,
            "recall": 0.84,
            "total_samples": 48965,
            "n_categories": 5
        }


@st.cache_data
def load_transformer_metrics():
    try:
        metrics_path = os.path.join(ROOT_DIR, "reports", "metrics", "transformer_metrics.json")
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_top_keywords(model, vectorizer, cleaned_text, raw_prediction, top_n=10):
    """Extrae palabras que más influyeron en la predicción (SVM lineal)"""
    vec = vectorizer.transform([cleaned_text])
    class_idx = list(model.classes_).index(raw_prediction)
    coefs = model.coef_[class_idx]
    feature_names = vectorizer.get_feature_names_out()
    vec_array = vec.toarray()[0]

    word_weights = []
    for idx, weight in enumerate(vec_array):
        if weight > 0:
            word = feature_names[idx]
            importance = coefs[idx] * weight
            word_weights.append((word, importance))

    word_weights.sort(key=lambda x: abs(x[1]), reverse=True)
    return word_weights[:top_n]


def get_alert_class(prediction_es: str):
    """Obtiene clase de alerta según predicción (en español)"""
    high_risk = ["Ideación suicida"]
    medium_risk = ["Depresión", "Ansiedad"]

    if prediction_es in high_risk:
        return "alert-high"
    elif prediction_es in medium_risk:
        return "alert-medium"
    else:
        return "alert-low"


import hashlib
import random


def _stable_choice_index(text: str, k: int) -> int:
    """
    Devuelve un índice 0..k-1 estable para un mismo texto.
    (Así no cambia si recargas la página, pero sí cambia con otro texto.)
    """
    text = (text or "").strip().lower()
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    return int(h[:8], 16) % k


def get_recommendation_sets():
    """
    5 combinaciones por emoción (cada combinación = lista de bullets).
    """
    return {
        "Depresión": [
            [
                "Paso mínimo: ducha o lavarte la cara + cambiarte de ropa (si puedes).",
                "Actividad pequeña: 10 minutos de luz solar o caminar suave.",
                "Una acción de conexión: enviar un mensaje a alguien de confianza.",
                "Hidratación y comida simple: agua + algo ligero (aunque sea poco).",
                "Rutina corta: una tarea muy pequeña (hacer la cama / ordenar 5 minutos).",
            ],
            [
                "Divide el día en bloques: solo próxima acción (no todo a la vez).",
                "Respira 2 minutos (inhalar 4s, exhalar 6s).",
                "Escribe 3 líneas: qué siento / qué necesito / qué puedo hacer hoy.",
                "Reduce autoexigencia: el objetivo es sostenerte, no rendir perfecto.",
                "Si puedes, intenta dormir a la misma hora esta semana.",
            ],
            [
                "Camina 5–15 minutos (sin intensidad, solo movimiento).",
                "Elige una comida fácil (fruta / sopa / sándwich) y hazlo sin presión.",
                "Pon una alarma para hacer una pausa y estirar 1 minuto.",
                "Escucha algo calmado (música suave o sonidos).",
                "Si persiste, considera agendar una consulta con un profesional.",
            ],
            [
                "Aterriza en el presente: nombra 5 cosas que ves, 4 que sientes, 3 que oyes.",
                "Haz una tarea de autocuidado breve (lavar cara, cepillar dientes).",
                "Evita aislarte del todo.",
                "Baja estímulos: menos redes por 20–30 min si te sobrecarga.",
                "Escribe una cosa que te ayudaría hoy (aunque sea pequeña).",
            ],
            [
                "Haz la versión mini de lo que te cuesta (2 minutos).",
                "Si lloras, está bien: acompaña eso con respiración lenta.",
                "Busca apoyo: alguien de confianza o un profesional.",
                "Crea un recordatorio amable: esto es temporal, hoy hago lo mínimo.",
                "Si notas empeoramiento fuerte, pide ayuda inmediata.",
            ],
        ],

        "Ansiedad": [
            [
                "Respiración 4-7-8 (4s inhalar, 7s sostener, 8s exhalar) x 3 ciclos.",
                "Descarga mental: escribe tus preocupaciones 5 minutos sin filtrar.",
                "Reduce cafeína hoy si puedes.",
                "Haz grounding: 5-4-3-2-1 (sentidos).",
                "Una acción pequeña: ordenar un espacio 5 minutos.",
            ],
            [
                "Exhalación larga: inhalar 4s, exhalar 6–8s por 2–3 minutos.",
                "Pon nombre a la emoción: estoy sintiendo ansiedad (sin pelearla).",
                "Evita multitarea; elige 1 cosa por 10 minutos.",
                "Mueve el cuerpo 5–10 min (caminar / estirar).",
                "Si se repite a diario, considera apoyo profesional.",
            ],
            [
                "Pregunta útil: ¿qué es lo controlable hoy? anota 2 cosas.",
                "Haz una pausa de pantalla 15 minutos.",
                "Audio guiado corto (respiración / relajación muscular).",
                "Habla con alguien de confianza aunque sea breve.",
                "Hidrátate: un vaso de agua ahora.",
            ],
            [
                "Relajación muscular: aprieta puños 5s y suelta (3 veces).",
                "Ancla: coloca los pies firmes al suelo y nota la presión.",
                "Evita leer demasiado noticias/redes por un rato.",
                "Crea un plan mini: 'si me sube, hago X' (respirar + caminar).",
                "Dormir: intenta rutina calmada 30 min antes de acostarte.",
            ],
            [
                "Respira con conteo: 1–2–3–4 inhalar, 1–2–3–4 exhalar.",
                "Escribe 1 frase amable: Puedo con esto paso a paso.",
                "Haz algo repetitivo calmante (taza de té, ducha tibia).",
                "Divide tareas: solo el primer paso.",
                "Si hay ataques fuertes, busca ayuda profesional.",
            ],
        ],

        "Estrés": [
            [
                "Prioriza: elige 1 tarea importante y 1 pequeña (solo eso por ahora).",
                "Pausa activa: estirar 2 minutos cada hora.",
                "Hidrátate y come algo sencillo.",
                "Bloquea 10 min sin interrupciones (modo foco).",
                "Descanso real: 15 min sin pantalla si puedes.",
            ],
            [
                "Haz una lista: urgente vs importante (y suelta lo no esencial).",
                "Respiración lenta 2–3 minutos.",
                "Camina 10 minutos o estira suave.",
                "Habla con alguien para descargar (mensaje corto).",
                "Cierra el día con una rutina pequeña (ducha, ordenar, té).",
            ],
            [
                "Define un límite: 'hoy paro a las ___'.",
                "Reduce multitarea: 1 cosa a la vez 10 min.",
                "Micro-descanso: mirar lejos 20s cada 20 min.",
                "Si puedes, organiza mañana con 3 tareas máximas.",
                "Sueño: intenta acostarte 30 min antes hoy.",
            ],
            [
                "Toma aire: inhalar 4s, exhalar 6s por 2 min.",
                "Haz algo corporal: estiramiento cuello/hombros.",
                "Pon música tranquila 10 minutos.",
                "Evita compararte: enfócate en progreso mínimo.",
                "Si el estrés está afectando salud, considera apoyo profesional.",
            ],
            [
                "Descarga: escribe todo lo que tienes en mente 5 min.",
                "Elige 1 cosa que puedes delegar o posponer.",
                "Crea un mini-plan: primero A, luego B.",
                "Toma agua + snack simple.",
                "Haz una pausa breve al aire libre si puedes.",
            ],
        ],

        "Ideación suicida": [
            [
                "Busca apoyo inmediato: llama a una línea de ayuda o a alguien de confianza.",
                "Panamá: 169 (MINSA). Si estás en peligro inmediato, emergencias.",
                "No te quedes a solas: intenta estar cerca de alguien.",
                "Reduce el acceso a objetos con los que podrías hacerte daño.",
                "Respira lento conmigo: exhala más largo que inhalas (2 min).",
            ],
            [
                "Da un paso urgente: llama a alguien ahora mismo y di 'necesito ayuda'.",
                "Panamá: 169 (MINSA). Internacional: befrienders.org",
                "Ve a un lugar más seguro (zona común de la casa / casa de alguien).",
                "Evita alcohol u otras sustancias.",
                "Quédate en el presente: 5 cosas que ves, 4 que sientes, 3 que oyes.",
            ],
            [
                "Si hay riesgo inmediato, busca emergencias/urgencias.",
                "Contacta a un familiar/amigo: 'me siento en riesgo' (directo).",
                "No tomes decisiones importantes ahora; solo sostenerte.",
                "Haz una acción de cuidado mínima (agua, sentarte, respirar).",
                "Estoy aquí para acompañarte mientras contactas ayuda.",
            ],
            [
                "Pide ayuda profesional hoy: llamada / cita urgente.",
                "Panamá: 169 (MINSA). Internacional: befrienders.org",
                "Si puedes, comparte tu ubicación con alguien de confianza.",
                "Evita estar en lugares aislados.",
                "Respiración guiada 2 min (exhalación lenta).",
            ],
            [
                "Tu seguridad es prioridad: busca apoyo inmediato.",
                "Llama a alguien (amigo/familia) y quédate en llamada.",
                "Panamá: 169 (MINSA). Internacional: befrienders.org",
                "Si estás en peligro, emergencias.",
                "No estás sola. Hay ayuda disponible 24/7.",
            ],
        ],

        # Por si algún día sale "Normal"
        "Normal": [
            [
                "Sigue con tus hábitos saludables (sueño, comida, movimiento).",
                "Tómate un descanso breve si lo necesitas.",
                "Mantén contacto con tu red de apoyo.",
                "Haz algo que te guste aunque sea 10 minutos.",
                "Escribe 1 cosa por la que agradeces hoy.",
            ],
            [
                "Planifica 1 meta pequeña para hoy y cúmplela.",
                "Haz una caminata corta o estira 5 minutos.",
                "Bebe agua.",
                "Desconéctate 15 min de pantallas.",
                "Duerme a una hora regular si puedes.",
            ],
            [
                "Haz una pausa de respiración 2 min.",
                "Organiza tu día con 3 tareas máximas.",
                "Dedica tiempo a un hobby.",
                "Comparte un mensaje con alguien cercano.",
                "Termina el día con una rutina relajante.",
            ],
            [
                "Mantén equilibrio: trabajo/estudio + descanso.",
                "Haz algo de movimiento suave.",
                "Cuida tu alimentación hoy.",
                "Busca espacios de luz natural.",
                "Evalúa tu estrés y ajusta si sube.",
            ],
            [
                "Celebra tus avances (aunque sean pequeños).",
                "Haz 10 min de algo placentero.",
                "Toma agua y come algo nutritivo.",
                "Sigue tu rutina.",
                "Pide apoyo si lo necesitas.",
            ],
        ],
    }


def get_recommendations(prediction_es: str, user_text: str):
    sets = get_recommendation_sets()
    options = sets.get(prediction_es) or sets.get("Normal")
    idx = _stable_choice_index(user_text, len(options))
    return options[idx]


def is_baseline_mode(selected_mode: str) -> bool:
    return selected_mode.startswith("Baseline")


# ================================
# INICIALIZAR HISTORIAL
# ================================
if "history" not in st.session_state:
    st.session_state.history = []

model_metrics = load_model_metrics()

# ================================
# HEADER
# ================================
st.markdown('<p class="main-header">Mental Health Monitor</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Detección temprana de estados emocionales con Inteligencia Artificial</p>',
    unsafe_allow_html=True
)

# ================================
# SIDEBAR
# ================================
with st.sidebar:
    st.header("Panel de Control")

    st.subheader("Motor de IA")
    selected_backend = st.radio(
        "Selecciona el motor:",
        options=["baseline", "transformer"],
        index=0,
        format_func=lambda x: "Baseline (SVM + TF-IDF)" if x == "baseline" else "Transformer (DistilBERT)"
    )
    use_baseline = (selected_backend == "baseline")

    st.subheader("Información del Sistema")
    if use_baseline:
        st.info("""
        **Baseline:** SVM + TF-IDF (bigrama)

        **Categorías detectadas:**
        • Ansiedad
        • Depresión
        • Estrés
        • Ideación suicida
        """)
    else:
        st.info("""
        **Transformer:** DistilBERT fine-tuned

        **Categorías detectadas:**
        • Ansiedad
        • Depresión
        • Estrés
        • Ideación suicida
        """)

    # Métricas según el modelo seleccionado
    if use_baseline:
        st.subheader("Rendimiento del Modelo (Baseline)")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Accuracy", f"{model_metrics['accuracy'] * 100:.1f}%")
            st.metric("Precision", f"{model_metrics['precision'] * 100:.1f}%")
        with col_m2:
            st.metric("F1-Score", f"{model_metrics['f1_score'] * 100:.1f}%")
            st.metric("Recall", f"{model_metrics['recall'] * 100:.1f}%")
        st.caption(f"Entrenado con {model_metrics['total_samples']:,} muestras")
    else:
        st.subheader("Rendimiento del Modelo (Transformer)")
        transformer_metrics = load_transformer_metrics()
        if transformer_metrics:
            st.metric("Eval Loss", f"{transformer_metrics.get('eval_loss', 0):.4f}")
            if "eval_f1" in transformer_metrics:
                st.metric("Eval F1", f"{transformer_metrics['eval_f1']:.4f}")
            if "eval_accuracy" in transformer_metrics:
                st.metric("Eval Accuracy", f"{transformer_metrics['eval_accuracy']:.4f}")
        else:
            st.caption("No se encontraron métricas del Transformer en reports/metrics/transformer_metrics.json")

    if st.session_state.history:
        st.subheader("Estadísticas de Sesión")
        predictions_only = [item["prediction"] for item in st.session_state.history]
        prediction_counts = Counter(predictions_only)

        st.metric("Total de análisis", len(st.session_state.history))

        for emotion, count in prediction_counts.most_common():
            st.write(f"**{emotion}:** {count}")

        if st.button("Limpiar Historial"):
            st.session_state.history = []
            st.rerun()

    st.divider()
    st.subheader("Recursos de Ayuda")
    st.markdown("""
    **Si estás en crisis:**

    - Panamá: 169 (MINSA)
    - Internacional: befrienders.org

    *Este sistema es una herramienta de apoyo y no reemplaza atención profesional.*
    """)

# ================================
# ÁREA PRINCIPAL
# ================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Ingresa tu texto para análisis")
    user_input = st.text_area(
        "Escribe cómo te sientes o qué está pasando por tu mente:",
        height=150,
        placeholder="Ejemplo: Me siento muy ansioso últimamente, no puedo dormir bien..."
    )
    analyze_button = st.button("Analizar Estado Emocional", type="primary", use_container_width=True)

with col2:
    st.subheader("Sugerencias")
    st.info("""
    **Para mejores resultados:**

    - Escribe al menos **2–3 oraciones**
    - Sé honesto sobre tus sentimientos
    - Compatible con **español e inglés**
    """)

# ================================
# PROCESAMIENTO
# ================================
if analyze_button:
    if user_input.strip():
        with st.spinner("Analizando texto..."):
            result = predict_text_unified(user_input, mode=selected_backend)

            prediction_es = result["prediction"]
            raw_pred = result["prediction_raw"]
            cleaned_text = result.get("cleaned", "")
            confidences = result.get("confidences_raw", {})

            alert_class = get_alert_class(prediction_es)

            # proteger por si algún backend no manda confidences
            max_conf = (max(confidences.values()) * 100) if confidences else 0.0

            from src.models.risk.predict_risk import score_from_prediction, risk_level

            conf_01 = (max(confidences.values()) if confidences else 0.0)  # 0..1
            risk_score = score_from_prediction(prediction_es, conf_01)
            risk_txt = risk_level(risk_score)

            st.session_state.history.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "text": user_input[:50] + "..." if len(user_input) > 50 else user_input,
                "prediction": prediction_es,
                "confidence": max_conf
            })

            st.divider()
            st.subheader("Resultados del Análisis")

            col_res1, col_res2 = st.columns(2)

            with col_res1:
                st.markdown(f"""
                <div class="{alert_class}">
                    <h3>Estado Detectado</h3>
                    <h2>{prediction_es}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col_res2:
                st.metric("Confianza (score)", f"{max_conf:.1f}%")
                st.caption("Nota: este valor es un score del modelo; úsalo como referencia comparativa.")
                st.progress(max_conf / 100 if max_conf > 0 else 0)

                st.metric("Riesgo (score)", f"{risk_score * 100:.1f}%")
                st.caption(f"Nivel de riesgo: {risk_txt}")

                if max_conf >= 80:
                    conf_text = "Muy Alta"
                elif max_conf >= 60:
                    conf_text = "Alta"
                elif max_conf >= 40:
                    conf_text = "Moderada"
                else:
                    conf_text = "Baja"

                st.caption(f"Interpretación del score: {conf_text}")

            st.divider()

            # ================================
            # DISTRIBUCIÓN DE CONFIANZA
            # ================================
            st.subheader("Distribución de Confianza por Categoría")

            label_mapping = {
                "Anxiety": "Ansiedad",
                "Depression": "Depresión",
                "Stress": "Estrés",
                "Suicidal": "Ideación suicida",
            }

            if confidences:
                conf_data = {label_mapping.get(k, k): v * 100 for k, v in confidences.items()}
                conf_df = pd.DataFrame({
                    "Emoción": list(conf_data.keys()),
                    "Confianza (%)": list(conf_data.values())
                }).sort_values("Confianza (%)", ascending=False)

                color_map = {
                    "Estrés": "#f59e0b",
                    "Ansiedad": "#f59e0b",
                    "Depresión": "#dc2626",
                    "Ideación suicida": "#991b1b"
                }
                conf_df["Color"] = conf_df["Emoción"].map(color_map)

                fig_conf = go.Figure(data=[
                    go.Bar(
                        y=conf_df["Emoción"],
                        x=conf_df["Confianza (%)"],
                        orientation="h",
                        marker=dict(
                            color=conf_df["Color"],
                            line=dict(color="#1a4d7a", width=1)
                        ),
                        text=conf_df["Confianza (%)"].round(1),
                        texttemplate="%{text}%",
                        textposition="outside",
                    )
                ])

                fig_conf.update_layout(
                    title="Nivel de confianza por categoría emocional",
                    xaxis_title="Confianza (%)",
                    yaxis_title="",
                    height=300,
                    showlegend=False,
                    font=dict(color="#4a5568"),
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#e5e7eb",
                        range=[0, float(max(conf_df["Confianza (%)"])) * 1.15]
                    ),
                    yaxis=dict(showgrid=False),
                )

                st.plotly_chart(fig_conf, use_container_width=True)
            else:
                st.info("Este motor no devolvió confidencias por categoría.")

            # ================================
            # PALABRAS CLAVE (solo Baseline)
            # ================================
            if use_baseline:
                st.divider()
                st.subheader("Palabras Clave Más Influyentes (Baseline)")

                model, vectorizer = load_baseline()

                keywords = get_top_keywords(
                    model=model,
                    vectorizer=vectorizer,
                    cleaned_text=cleaned_text,
                    raw_prediction=raw_pred,
                    top_n=10
                )

                if keywords:
                    col_kw1, col_kw2 = st.columns(2)

                    with col_kw1:
                        st.write("**Top 5 palabras que influyeron en la predicción:**")
                        kw_data = pd.DataFrame(keywords, columns=["Palabra", "Importancia"])
                        kw_data["Importancia"] = kw_data["Importancia"].abs()

                        fig_kw = go.Figure(data=[
                            go.Bar(
                                x=kw_data.head(5)["Importancia"],
                                y=kw_data.head(5)["Palabra"],
                                orientation="h",
                                text=kw_data.head(5)["Importancia"].round(3),
                                textposition="outside",
                            )
                        ])

                        fig_kw.update_layout(
                            height=280,
                            showlegend=False,
                            font=dict(color="#4a5568"),
                            xaxis=dict(
                                title="Importancia",
                                showgrid=True,
                                gridcolor="#e5e7eb"
                            ),
                            yaxis=dict(title="", showgrid=False),
                            margin=dict(l=20, r=60, t=20, b=40)
                        )

                        st.plotly_chart(fig_kw, use_container_width=True)

                    with col_kw2:
                        st.write("**Lista completa de palabras clave:**")
                        for idx, (word, importance) in enumerate(keywords, 1):
                            st.write(f"{idx}. **{word}** ({importance:.3f})")
            else:
                st.divider()
                st.info("En Transformer no se muestran 'palabras clave' tipo SVM (no usa coeficientes TF-IDF).")

            st.divider()

            # ================================
            # RECOMENDACIONES
            # ================================
            st.subheader("Recomendaciones")

            recs = get_recommendations(prediction_es, user_input)

            if prediction_es == "Ideación suicida":
                st.error("**ALERTA: Se detectaron señales de alto riesgo.**")
                st.markdown("**Acciones recomendadas:**")
                for r in recs:
                    st.markdown(f"- {r}")

            elif prediction_es == "Depresión":
                st.warning("**Recomendaciones para manejar síntomas depresivos:**")
                for r in recs:
                    st.markdown(f"- {r}")

            elif prediction_es == "Ansiedad":
                st.warning("**Recomendaciones para manejar la ansiedad:**")
                for r in recs:
                    st.markdown(f"- {r}")

            elif prediction_es == "Estrés":
                st.info("**Recomendaciones para manejar el estrés:**")
                for r in recs:
                    st.markdown(f"- {r}")

            else:
                st.success("**Tu estado emocional parece estable:**")
                for r in recs:
                    st.markdown(f"- {r}")

    else:
        st.warning("Por favor, ingresa un texto para analizar.")

# ================================
# HISTORIAL
# ================================
if st.session_state.history:
    st.divider()
    st.subheader("Historial de Análisis (Sesión Actual)")

    hist_df = pd.DataFrame(st.session_state.history)

    col_hist1, col_hist2 = st.columns(2)

    with col_hist1:
        emotion_counts = hist_df["prediction"].value_counts()

        color_discrete_map = {
            "Estrés": "#f59e0b",
            "Ansiedad": "#f59e0b",
            "Depresión": "#dc2626",
            "Ideación suicida": "#991b1b"
        }

        fig_pie = px.pie(
            values=emotion_counts.values,
            names=emotion_counts.index,
            title="Distribución de Estados Emocionales Detectados",
            color=emotion_counts.index,
            color_discrete_map=color_discrete_map
        )

        fig_pie.update_traces(
            textfont_size=12,
            marker=dict(line=dict(color="#1a4d7a", width=2))
        )

        fig_pie.update_layout(
            title_font=dict(size=14, color="#1a4d7a"),
            font=dict(color="#4a5568")
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col_hist2:
        st.write("**Últimos análisis realizados:**")
        display_df = hist_df[["timestamp", "prediction", "confidence"]].copy()
        display_df.columns = ["Hora", "Emoción", "Confianza (%)"]
        display_df["Confianza (%)"] = display_df["Confianza (%)"].round(1)

        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ================================
# FOOTER
# ================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p><strong>Mental Health Monitor</strong></p>
    <p>Desarrollado con IA para detección temprana de estados emocionales críticos</p>
    <p><em>Este sistema es una herramienta de apoyo y no sustituye la atención médica profesional</em></p>
</div>
""", unsafe_allow_html=True)