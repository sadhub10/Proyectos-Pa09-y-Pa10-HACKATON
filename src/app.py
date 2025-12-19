# =========================================================
# src/app.py - PyBrAIn | Digital Modulation Classifier (CNN)
# =========================================================


import base64
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

import streamlit as st
import streamlit.components.v1 as components
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms

from datetime import datetime
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


# =========================================================
# CONFIG APP
# =========================================================
st.set_page_config(
    page_title="PyBrAIn SignalIQ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# RUTAS (compatibles con tu estructura real)
# =========================================================
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent

ASSETS_DIR = ROOT_DIR / "assets"
NOTEBOOK_DIR = ROOT_DIR / "notebook"
LOGS_DIR = ROOT_DIR / "logs"
IMG_LOG_DIR = LOGS_DIR / "images"
CSV_LOG_PATH = LOGS_DIR / "history.csv"

CSS_PATH = ASSETS_DIR / "styles.css"
LOGO_PATH = ASSETS_DIR / "logo.png"
MODEL_PATH = NOTEBOOK_DIR / "modelo_senalesIA.pth"

LOGS_DIR.mkdir(exist_ok=True)
IMG_LOG_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# CSS
# =========================================================
def load_css():
    if CSS_PATH.exists():
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"No se encontró styles.css en: {CSS_PATH}")

load_css()

# =========================================================
# LOGO (base64)
# =========================================================
LOGO_B64 = None
if LOGO_PATH.exists():
    with open(LOGO_PATH, "rb") as f:
        LOGO_B64 = base64.b64encode(f.read()).decode("utf-8")

# =========================================================
# CLASES
# =========================================================
CLASS_NAMES = [
    'ASK_16', 'ASK_2', 'ASK_32', 'ASK_4', 'ASK_64', 'ASK_8',
    'FSK_16', 'FSK_2', 'FSK_32', 'FSK_4', 'FSK_64', 'FSK_8',
    'PSK_16', 'PSK_2', 'PSK_32', 'PSK_4', 'PSK_64', 'PSK_8',
    'QAM_16', 'QAM_4', 'QAM_64', 'QAM_8'
]

HIDDEN_FSK = {'FSK_2', 'FSK_4', 'FSK_8', 'FSK_16', 'FSK_32', 'FSK_64'}

IMG_SIZE = 96
MAX_ACTIVE_SIGNALS = 3
device = torch.device("cpu")

# =========================================================
# ESTADO DE SESIÓN
# =========================================================
if "last_pred_class" not in st.session_state:
    st.session_state["last_pred_class"] = None
    st.session_state["last_pred_conf"] = None
    st.session_state["last_prob_dict"] = None
    st.session_state["last_img_filename"] = None
    st.session_state["signal_queue"] = []

# =========================================================
# MODELO (ResNet-like)
# =========================================================
class BasicBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv1 = nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.conv2 = nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_ch)

        self.shortcut = nn.Sequential()
        if in_ch != out_ch:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, kernel_size=1),
                nn.BatchNorm2d(out_ch),
            )

    def forward(self, x):
        identity = self.shortcut(x)
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out = out + identity
        return F.relu(out)


class ModulationResNet(nn.Module):
    def __init__(self, num_classes: int, img_size: int = 96):
        super().__init__()
        self.conv_in = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn_in = nn.BatchNorm2d(32)

        self.block1 = BasicBlock(32, 64)
        self.pool1 = nn.MaxPool2d(2, 2)

        self.block2 = BasicBlock(64, 128)
        self.pool2 = nn.MaxPool2d(2, 2)

        self.block3 = BasicBlock(128, 256)
        self.pool3 = nn.MaxPool2d(2, 2)

        feat_dim = 256 * (img_size // 8) * (img_size // 8)
        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(feat_dim, 512)
        self.fc2 = nn.Linear(512, num_classes)

    def forward(self, x):
        x = F.relu(self.bn_in(self.conv_in(x)))
        x = self.pool1(self.block1(x))
        x = self.pool2(self.block2(x))
        x = self.pool3(self.block3(x))
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1(x)))
        return self.fc2(x)


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error(f"Model file not found: {MODEL_PATH}")
        st.stop()

    model = ModulationResNet(num_classes=len(CLASS_NAMES), img_size=IMG_SIZE)
    state = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model

model = load_model()

# =========================================================
# PREPROCESAMIENTO + PREDICCIÓN
# =========================================================
def get_preprocess():
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ])

def predict_image(pil_img: Image.Image):
    preprocess = get_preprocess()
    x = preprocess(pil_img).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    idx = int(np.argmax(probs))
    pred_class = CLASS_NAMES[idx]
    prob_dict = {name: float(p) for name, p in zip(CLASS_NAMES, probs)}
    return pred_class, prob_dict

# =========================================================
# SNR (heurística por confianza)
# =========================================================
def get_snr_info(confidence: float):
    """
    Analizador heurístico de calidad de señal.
    Devuelve estado, clase CSS y recomendación técnica.
    """
    if confidence >= 0.80:
        return {
            "label": "HIGH",
            "status": "OPERACIÓN ÓPTIMA",
            "css": "snr-high",
            "description": "Señal estable y confiable.",
            "recommendation": [
                "Mantener parámetros actuales",
                "Posible aumento de tasa de datos",
                "Ideal para modulaciones de mayor orden"
            ]
        }

    elif confidence >= 0.55:
        return {
            "label": "MEDIUM",
            "status": "OPERACIÓN LIMITADA",
            "css": "snr-medium",
            "description": "Señal funcional con interferencia moderada.",
            "recommendation": [
                "Considerar aumentar potencia de transmisión",
                "Reducir orden de modulación si el canal lo requiere",
                "Aplicar filtrado o corrección de errores"
            ]
        }

    else:
        return {
            "label": "LOW",
            "status": "OPERACIÓN CRÍTICA",
            "css": "snr-low",
            "description": "Señal inestable con alto nivel de ruido.",
            "recommendation": [
                "Cambiar frecuencia de operación",
                "Reducir drásticamente el orden de modulación",
                "Revisar canal, antena o interferencias externas"
            ]
        }



# =========================================================
# SALUD DE LA SEÑAL (heurística avanzada)
# =========================================================
def get_signal_health(confidence: float):
    if confidence >= 0.85:
        return "ÓPTIMA", "#00ff88", "La señal es clara y permite máxima velocidad de datos."
    elif confidence >= 0.55:
        return "DEGRADADA", "#ffcc00", "Se detecta ruido térmico. Posible necesidad de aumentar potencia."
    else:
        return "CRÍTICA", "#ff4444", "Interferencia severa detectada. Se recomienda cambiar de frecuencia."


# =========================================================
# CONSTRUCCIÓN DE OBJETO DE SEÑAL
# =========================================================
def build_signal_object(image_path, modulation, confidence, snr_label, signal_health, health_comment):
    """Construye un objeto de señal para almacenar en la cola."""
    # Calcular puntaje global basado en confianza y salud
    health_score = {"ÓPTIMA": 1.0, "DEGRADADA": 0.6, "CRÍTICA": 0.3}.get(signal_health, 0.5)
    global_score = (confidence + health_score) / 2
    
    return {
        "image_path": image_path,
        "modulation": modulation,
        "confidence": round(confidence * 100, 2),
        "snr": snr_label,
        "health": signal_health,
        "score": round(global_score * 100, 2),
        "timestamp": datetime.now(),
        "health_comment": health_comment
    }


# =========================================================
# COLA DE SEÑALES (ventana deslizante)
# =========================================================
def push_signal(signal_obj, max_size=3):
    st.session_state["signal_queue"].insert(0, signal_obj)
    if len(st.session_state["signal_queue"]) > max_size:
        st.session_state["signal_queue"].pop()


# =========================================================
# LOGGING (CSV + imagen con acrónimo)
# =========================================================
def ensure_history_csv():
    if not CSV_LOG_PATH.exists():
        df = pd.DataFrame(columns=[
            "timestamp",
            "modulation",
            "confidence_pct",
            "snr_level",
            "image_file",
        ])
        df.to_csv(CSV_LOG_PATH, index=False)
# =========================================================
# REPORTE PDF
# =========================================================
def generate_pdf_report(signals):
    if not signals:
        return None

    filename = f"reporte_senales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = LOGS_DIR / filename

    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "PyBrAIn – Reporte de Análisis de Señales")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 25

    for i, s in enumerate(signals, 1):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"Señal {i}")
        y -= 15

        c.setFont("Helvetica", 10)
        c.drawString(60, y, f"Modulación: {s['modulation']}")
        y -= 12
        c.drawString(60, y, f"Confianza: {s['confidence']} %")
        y -= 12
        c.drawString(60, y, f"SNR: {s['snr']}")
        y -= 12
        c.drawString(60, y, f"Estado: {s['health']}")
        y -= 12
        c.drawString(60, y, f"Comentario: {s.get('health_comment', 'N/A')}")
        y -= 20

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return file_path


def save_uploaded_image(pil_img: Image.Image, modulation: str) -> str:
    """Guarda imagen con acrónimo de la señal detectada"""
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Extraer familia (ASK, PSK, QAM, FSK)
    acronym = modulation.split("_")[0] if "_" in modulation else modulation
    filename = f"{acronym}_{ts}.png"
    out_path = IMG_LOG_DIR / filename
    pil_img.save(out_path)
    return filename

def append_history_row(modulation: str, confidence: float, snr_level: str, image_file: str):
    ensure_history_csv()
    row = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modulation": modulation,
        "confidence_pct": round(confidence * 100, 2),
        "snr_level": snr_level,
        "image_file": image_file,
    }
    df_old = pd.read_csv(CSV_LOG_PATH)
    df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
    df_new.to_csv(CSV_LOG_PATH, index=False)

def read_history():
    ensure_history_csv()
    return pd.read_csv(CSV_LOG_PATH)

# =========================================================
# UI
# =========================================================
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

st.markdown("""
<div class="header-section">
  <h1 class="main-title"> Signal IQ</h1>
  <p class="subtitle">CNN Supervisada (End-to-End) | ASK · PSK · QAM</p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.8], gap="large")

# -----------------------------
# IZQUIERDA: UPLOAD + ACCIONES
# -----------------------------
with col_left:
    st.markdown('<div class="section-title">Entrada de Señal</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Adjuntar imagen de la señal (PNG, JPG)",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
        key="uploader",
    )

    pil_img = None
    if uploaded_file is not None:
        pil_img = Image.open(uploaded_file).convert("RGB")
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(pil_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    analyze_clicked = st.button("ANALIZAR SEÑAL", disabled=(pil_img is None))

    last_label = st.session_state.get("last_pred_class")
    last_conf = st.session_state.get("last_pred_conf")
    last_prob_dict = st.session_state.get("last_prob_dict")
    last_img_filename = st.session_state.get("last_img_filename")

    # Detalles sistema
    with st.expander("Detalles del Sistema entrenado"):
        st.markdown(f"""
        **Modelo** CNN tipo ResNet (bloques residuales)  
        **Tamaño de entrada** {IMG_SIZE}×{IMG_SIZE}px (grayscale)  
        **Clases** {len(CLASS_NAMES)} (incluye FSK; demo puede ocultarlas)  
        **Salida** Softmax multiclase  
        """)

     
     # Detalles técnicos
    with st.expander("Detalles Técnicos"):
        family, order = last_label.split("_") if "_" in last_label else (last_label, "N/A")
        st.markdown(f"""
        **Familia** {family}  
        **Orden** M = {order}  
        **Confianza** {last_conf*100:.2f}%  
        **Imagen guardada** {last_img_filename if last_img_filename else "N/A"}  
        """)

   

# -----------------------------
# DERECHA: RESULTADO + LOGS
# -----------------------------
with col_right:
    st.markdown('<div class="section-title">Resultados</div>', unsafe_allow_html=True)

    if analyze_clicked and pil_img is not None:
        with st.spinner("Procesando señal..."):
            pred_class, prob_dict = predict_image(pil_img)
        max_prob = float(max(prob_dict.values()))

        snr_info = get_snr_info(max_prob)
        snr_level = snr_info['label']
        health_label, _, health_comment = get_signal_health(max_prob)

        img_filename = save_uploaded_image(pil_img, pred_class)

        signal_obj = build_signal_object(
            image_path=img_filename,
            modulation=pred_class,
            confidence=max_prob,
            snr_label=snr_level,
            signal_health=health_label,
            health_comment=health_comment
        )

        push_signal(signal_obj, MAX_ACTIVE_SIGNALS)

        st.session_state["last_pred_class"] = pred_class
        st.session_state["last_pred_conf"] = max_prob
        st.session_state["last_prob_dict"] = prob_dict
        st.session_state["last_img_filename"] = img_filename

        append_history_row(pred_class, max_prob, snr_level, img_filename)

    last_label = st.session_state.get("last_pred_class")
    last_conf = st.session_state.get("last_pred_conf")
    last_prob_dict = st.session_state.get("last_prob_dict")
    last_img_filename = st.session_state.get("last_img_filename")

    last_label = st.session_state.get("last_pred_class")
    last_conf = st.session_state.get("last_pred_conf")
    last_prob_dict = st.session_state.get("last_prob_dict")
    last_img_filename = st.session_state.get("last_img_filename")

    if last_label is None:
        st.info("Sube una imagen y presiona **ANALIZAR SEÑAL** para ver resultados.")
    elif last_label in HIDDEN_FSK:
        st.warning("Se detectó modulación FSK. Esta demo se enfoca en ASK, PSK y QAM.")
    else:
        snr_info = get_snr_info(last_conf)
        snr_level = snr_info['label']
        snr_class = snr_info['css']
        snr_desc = snr_info['description']

        # RESULT BOX + LOGO DENTRO (AGRANDADO)
        if LOGO_B64:
            result_html = f"""
            <div class="result-box">
              <div class="result-inner">
                <div class="result-text">
                  <div class="result-label">MODULACIÓN DETECTADA</div>
                  <div class="prediction">{last_label}</div>
                  <div class="confidence">
                    Confianza: <span class="confidence-value">{last_conf*100:.1f}%</span>
                  </div>
                </div>
                <div class="result-logo">
                <img src="data:image/png;base64,{LOGO_B64}" alt="logo" class="logo-small" />
                </div>
              </div>
            </div>
            """
        else:
            result_html = f"""
            <div class="result-box">
              <div class="result-label">MODULACIÓN DETECTADA</div>
              <div class="prediction">{last_label}</div>
              <div class="confidence">
                Confianza: <span class="confidence-value">{last_conf*100:.1f}%</span>
              </div>
            </div>
            """
        st.markdown(result_html, unsafe_allow_html=True)

        # SNR badge
        snr_info = get_snr_info(last_conf)

        css_class = snr_info['css']
        label = snr_info['label']
        status = snr_info['status']
        description = snr_info['description']
        
        snr_css = """
<style>
.snr-container {
  margin-top: 16px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.snr-card {
  margin-top: 14px;
  padding: 16px;
  border-radius: 14px;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.06),
    rgba(255,255,255,0.015)
  );
  border: 1px solid rgba(255,255,255,0.18);
  color: #e5e7eb;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.snr-badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.snr-high {
  background: rgba(0,255,136,0.15);
  color: #00ff88;
  border: 1px solid rgba(0,255,136,0.4);
}

.snr-medium {
  background: rgba(255,204,0,0.15);
  color: #ffcc00;
  border: 1px solid rgba(255,204,0,0.4);
}

.snr-low {
  background: rgba(255,68,68,0.15);
  color: #ff4444;
  border: 1px solid rgba(255,68,68,0.4);
}

/* Texto principal del estado */
.snr-status {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #f8fafc;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Descripción */
.snr-description {
  font-size: 0.9rem;
  color: #cbd5e1;
  line-height: 1.4;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Título de recomendaciones */
.snr-title {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  color: #e5e7eb;
  margin-bottom: 6px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Lista */
ul {
  margin: 0;
  padding-left: 18px;
  font-size: 0.88rem;
  line-height: 1.45;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

li {
  margin-bottom: 6px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
</style>
"""

        recommendations_html = "".join(f"<li>{r}</li>" for r in snr_info["recommendation"])

        snr_html = f"""
{snr_css}
<div class="snr-container">
  <div class="snr-card">

    <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
      <div class="snr-badge {css_class}">
        {label}
      </div>
      <div class="snr-status">
        {status}
      </div>
    </div>

    <div class="snr-description">
      {description}
    </div>

    <div style="border-top:1px solid rgba(255,255,255,0.15); padding-top:10px; margin-top:10px;">
      <div class="snr-title">
        Recomendaciones del Analizador PyBrAIn
      </div>
      <ul>
        {recommendations_html}
      </ul>
    </div>

  </div>
</div>
"""
        components.html(snr_html, height=260)

        # Distribución de probabilidades (top 8, sin FSK) - ALTURA AUMENTADA
        if last_prob_dict:
            filtered = {k: v for k, v in last_prob_dict.items() if k not in HIDDEN_FSK}
            top = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:8]
            if top:
                dfp = pd.DataFrame(top, columns=["Clase", "Probabilidad"])
                dfp["Probabilidad (%)"] = (dfp["Probabilidad"] * 100).round(2)
                dfp = dfp.drop(columns=["Probabilidad"]).set_index("Clase")

                st.markdown('<div class="section-title" style="margin-top: 1.25rem;">Distribución de Probabilidades</div>', unsafe_allow_html=True)
                st.bar_chart(dfp, height=350)

     
    # -----------------------------
    # COMPARACIÓN DE SEÑALES
    # -----------------------------
    signal_queue = st.session_state.get("signal_queue", [])
    if signal_queue:
        st.markdown('<div class="section-title">Comparación de Señales </div>', unsafe_allow_html=True)

        df_compare = pd.DataFrame(signal_queue)
        df_compare = df_compare[["modulation", "confidence", "snr", "health", "score"]]
        df_compare = df_compare.rename(columns={
            "modulation": "Modulación",
            "confidence": "Confianza (%)",
            "snr": "SNR",
            "health": "Estado",
            "score": "Puntaje Global"
        })

        st.dataframe(df_compare, use_container_width=True)

        st.bar_chart(
            df_compare.set_index("Modulación")["Confianza (%)"]
        )
        

        pdf_path = generate_pdf_report(signal_queue)
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "GENERAR REPORTE PDF",
                    f,
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    use_container_width=True
                )


    # -----------------------------
    # HISTORIAL (TABLA + DESCARGA)
    # -----------------------------
    st.markdown('<div class="section-title" style="margin-top: 1.75rem;">Historial de Predicciones</div>', unsafe_allow_html=True)

    history_df = read_history()
    if history_df.empty:
        st.info("Aún no hay registros. Analiza una señal para comenzar el historial.")
    else:
        # Mostrar últimos 20 primero
        show_df = history_df.tail(20).copy()

        # Link visual de archivo (nombre) - solo texto, la imagen está en logs/images/
        show_df = show_df.rename(columns={
            "timestamp": "Fecha/Hora",
            "modulation": "Modulación",
            "confidence_pct": "Confianza (%)",
            "snr_level": "SNR",
            "image_file": "Archivo Imagen",
        })

        st.dataframe(show_df, use_container_width=True, height=280)
        c1, c2 = st.columns(2)

        with c1:
            st.download_button(
                "DESCARGAR CSV",
                data=history_df.to_csv(index=False).encode("utf-8"),
                file_name="history.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with c2:
            if st.button("LIMPIAR HISTORIAL", use_container_width=True):
                pd.DataFrame(columns=[
                    "timestamp", "modulation", "confidence_pct",
                    "snr_level", "image_file"
                ]).to_csv(CSV_LOG_PATH, index=False)
                st.success("Historial limpiado.")
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)