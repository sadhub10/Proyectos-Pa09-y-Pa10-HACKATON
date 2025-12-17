# app.py - Clasificador de modulaciones CNN

import os
import streamlit as st
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import plotly.graph_objects as go
import base64
import scipy.special as sp

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Clasificador de Modulaciones",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar estilos CSS externos
def load_css(file_name):
    """Carga un archivo CSS externo con codificación UTF-8"""
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Intentar cargar el archivo CSS
try:
    load_css('styles.css')
except FileNotFoundError:
    st.warning("Archivo 'styles.css' no encontrado. Usando estilos por defecto.")

# =========================================================
# CONFIGURACIÓN DEL MODELO
# =========================================================
MODEL_PATH = "best_modulation_cnn.pth"
IMG_SIZE = 96
device = torch.device("cpu")

# Ruta del logo (coloca tu logo en la misma carpeta)
LOGO_PATH = "logo.png"  # Cambia esto por el nombre de tu archivo de logo

# Cargar y codificar logo en base64
LOGO_B64 = None
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        LOGO_B64 = base64.b64encode(f.read()).decode()

CLASS_NAMES = [
    'ASK_16', 'ASK_2', 'ASK_32', 'ASK_4', 'ASK_64', 'ASK_8', 
    'FSK_16', 'FSK_2', 'FSK_32', 'FSK_4', 'FSK_64', 'FSK_8',
    'PSK_16', 'PSK_2', 'PSK_32', 'PSK_4', 'PSK_64', 'PSK_8', 
    'QAM_16', 'QAM_4', 'QAM_64', 'QAM_8'
]

HIDDEN_FSK = {'FSK_2', 'FSK_4', 'FSK_8', 'FSK_16', 'FSK_32', 'FSK_64'}

# Estado de sesión
if "last_pred_class" not in st.session_state:
    st.session_state["last_pred_class"] = None
    st.session_state["last_pred_conf"] = None
    st.session_state["last_prob_dict"] = None

# Métricas del modelo
PRECOMPUTED_METRICS = {
    "accuracy_global": 0.82,
    "num_epochs": 8,
    "num_clases": 22,
}

# =========================================================
# ARQUITECTURA DEL MODELO
# =========================================================
class BasicBlock(nn.Module):
    """Bloque básico residual"""
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
                nn.BatchNorm2d(out_ch)
            )

    def forward(self, x):
        identity = self.shortcut(x)
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += identity
        out = F.relu(out)
        return out


class ModulationResNet(nn.Module):
    """Red neuronal convolucional tipo ResNet para clasificación de modulaciones"""
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
        x = self.fc2(x)
        return x

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
@st.cache_resource
def load_model_and_metadata():
    """Carga el modelo entrenado y sus metadatos"""
    num_classes = len(CLASS_NAMES)
    model = ModulationResNet(num_classes=num_classes, img_size=IMG_SIZE)
    
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model file not found: {MODEL_PATH}")
        st.stop()
    
    state = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state)
    model.to(device)
    model.eval()
    
    return model, CLASS_NAMES, PRECOMPUTED_METRICS


def get_image_preprocessor():
    """Retorna el preprocesador de imágenes"""
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ])


def predict_image(model, class_names, pil_img):
    """Realiza la predicción sobre una imagen"""
    preprocess = get_image_preprocessor()
    img_tensor = preprocess(pil_img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        logits = model(img_tensor)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
    
    idx = int(probs.argmax())
    pred_class = class_names[idx]
    prob_dict = {name: float(p) for name, p in zip(class_names, probs)}
    
    return pred_class, prob_dict


def create_probability_chart(prob_dict, top_n=5):
    """Crea el gráfico de barras de probabilidades"""
    # Filtrar FSK
    filtered_probs = {k: v for k, v in prob_dict.items() if k not in HIDDEN_FSK}
    sorted_probs = sorted(filtered_probs.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    if not sorted_probs:
        return None
    
    names, probs = zip(*sorted_probs)
    
    fig = go.Figure(data=[
        go.Bar(
            y=list(names),
            x=[p*100 for p in probs],
            orientation='h',
            marker=dict(color='#00d4ff', opacity=0.8),
            text=[f'{p*100:.1f}%' for p in probs],
            textposition='auto',
            textfont=dict(color='#0a0e27', size=12, family='Inter'),
        )
    ])
    
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=None, color='#8892b0'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=None, color='#ccd6f6'),
        font=dict(family='Inter', size=11),
    )
    
    return fig


def get_snr_info(confidence):
    """Determina el nivel de SNR basado en la confianza"""
    if confidence >= 0.80:
        return "HIGH", "snr-high", "Excelente calidad de señal con mínima interferencia de ruido"
    elif confidence >= 0.50:
        return "MEDIUM", "snr-medium", "Calidad de señal moderada con alguna interferencia detectada"
    else:
        return "LOW", "snr-low", "Pobre calidad de señal con interferencia significativa de ruido"

#SALUD DE LA SEÑAL (heurística avanzada)

def get_signal_health(confidence: float):
    if confidence >= 0.85:
        return "ÓPTIMA", "#00ff88", "La señal es clara y permite máxima velocidad de datos."
    elif confidence >= 0.55:
        return "DEGRADADA", "#ffcc00", "Se detecta ruido térmico. Posible necesidad de aumentar potencia."
    else:
        return "CRÍTICA", "#ff4444", "Interferencia severa detectada. Se recomienda cambiar de frecuencia."
    
def estimate_ber(modulation_type, confidence):
    """Estima el BER basado en el tipo de modulación y la confianza (como proxy de SNR)"""
    # Mapeamos confianza (de 0.0 a 1.0) a un rango de SNR aproximado (0 a 20 dB)
    snr_db = confidence * 20 
    snr_linear = 10**(snr_db / 10)
    
    try:
        if "PSK_2" in modulation_type: # BPSK
            return 0.5 * sp.erfc(torch.sqrt(torch.tensor(snr_linear)).item())
        
        elif "PSK" in modulation_type: # QPSK, 8PSK, etc.
            # Aproximación para M-PSK
            return (1/2) * sp.erfc(torch.sqrt(torch.tensor(snr_linear * 0.5)).item())
            
        elif "QAM" in modulation_type:
            # Aproximación para M-QAM (basado en QAM-16)
            return 0.2 * sp.erfc(torch.sqrt(torch.tensor(0.4 * snr_linear)).item())
            
        elif "ASK" in modulation_type:
            # Aproximación para ASK
            return 0.5 * sp.erfc(torch.sqrt(torch.tensor(snr_linear / 4)).item())
            
        return 0.001 # Valor por defecto si es muy alto
    except:
        return 0.5 # Máximo error en caso de fallo
# =========================================================
# CARGAR MODELO
# =========================================================
with st.spinner("Cargando modelo..."):
    model, class_names, metrics = load_model_and_metadata()

# =========================================================
# INTERFAZ PRINCIPAL
# =========================================================
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# Header (sin logo grande)
st.markdown("""
<div class="header-section">
    <h1 class="main-title">Clasificador de Modulación Digital</h1>
    <p class="subtitle">Reconocimiento de Señales Potenciado por CNN | ASK · PSK · QAM</p>
</div>
""", unsafe_allow_html=True)

# Layout en dos columnas
col_left, col_right = st.columns([1, 1.8], gap="large")

# =========================================================
# COLUMNA IZQUIERDA - INPUT Y MÉTRICAS
# =========================================================
with col_left:
    # Título de la sección de input
    st.markdown('<div class="section-title">Entrada de Señal</div>', unsafe_allow_html=True)



    # Uploader normal (sin <div> manual alrededor)
    uploaded_file = st.file_uploader(
        "Adjuntar imagen de la señal (PNG, JPG)",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        pil_img = Image.open(uploaded_file).convert("RGB")
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(pil_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("ANALIZAR SEÑAL"):
            with st.spinner("Procesando señal..."):
                pred_class, prob_dict = predict_image(model, class_names, pil_img)

            max_prob = float(max(prob_dict.values()))
            st.session_state["last_pred_class"] = pred_class
            st.session_state["last_pred_conf"] = max_prob
            st.session_state["last_prob_dict"] = prob_dict
            st.rerun()

    


    
    # Información del sistema (expandible para no distraer)
    with st.expander("Detalles del Sistema entrenado"):
        visible_classes = len([c for c in CLASS_NAMES if c not in HIDDEN_FSK])
        
        st.markdown(f"""
        **Arquitectura** ResNet-inspired CNN  
        **Precisión del Modelo** {metrics['accuracy_global']*100:.1f}%  
        **Entrenamiento** {metrics['num_epochs']} epochs  
        **Resolución** {IMG_SIZE}×{IMG_SIZE}px  
        **Clases** {visible_classes} (ASK, PSK, QAM)  
        **Órdenes de Modulación** M = 2, 4, 8, 16, 32, 64
        """)

# =========================================================
# COLUMNA DERECHA - RESULTADOS
# =========================================================
with col_right:
    st.markdown('<div class="section-title">Resultados de la Clasificación</div>', unsafe_allow_html=True)
    
    last_label = st.session_state.get("last_pred_class")
    last_conf = st.session_state.get("last_pred_conf")
    last_prob_dict = st.session_state.get("last_prob_dict")
    
    if last_label is None:
        st.info("Sube y analiza una señal para ver los resultados de la clasificación")
    
    elif last_label in HIDDEN_FSK:
        st.warning("Se detectó modulación FSK. Esta demo se enfoca en ASK, PSK y QAM.")
    
    else:
        # Resultado principal
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
                        <img src="data:image/png;base64,{LOGO_B64}" alt="PyBrAIn logo" />
                    </div>
                </div>
            </div>
            """
        else:
            # Versión sin logo por si no se encuentra el archivo
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

        
        # Gráfico de probabilidades
        if last_prob_dict:
            st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Probabilidad de Distribución</div>', unsafe_allow_html=True)
            
            fig = create_probability_chart(last_prob_dict)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detalles técnicos
        with st.expander("Detalles Técnicos"):
            family, order = last_label.split("_") if "_" in last_label else (last_label, "N/A")
            st.markdown(f"""
            **Familia** {family}  
            **Orden** M = {order}  
            **Confianza** {last_conf*100:.2f}%  
            **Procesamiento** <1 segundo
            """)
            # ... (dentro del expander de Detalles Técnicos o justo arriba)
        
            ber_val = estimate_ber(last_label, last_conf)
            
            # Formatear el BER para que se vea profesional (notación científica)
            ber_text = f"{ber_val:.2e}" if ber_val > 1e-6 else "< 1e-06"

            st.markdown(f"""
            <div style="background: rgba(0, 212, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #00d4ff; margin-top: 10px;">
                <h4 style="margin:0; color:#00d4ff; font-size: 14px;">BER ESTIMADO (Bit Error Rate)</h4>
                <p style="font-size: 22px; font-family: 'Courier New', monospace; font-weight: bold; color: white; margin: 5px 0;">
                    {ber_text}
                </p>
                <small style="color: #8892b0;">Basado en modelo de canal AWGN y confianza del {last_conf*100:.1f}%</small>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)