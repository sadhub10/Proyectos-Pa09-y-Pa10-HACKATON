import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO
import tempfile
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="AI Safety Inspector",
    page_icon="🦺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para una interfaz moderna
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .safe-badge {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
    }
    
    .warning-badge {
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
    }
    
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar el modelo
@st.cache_resource
def load_model():
    """Carga el modelo YOLOv8 preentrenado"""
    try:
        # Intentar cargar modelo personalizado si existe
        if os.path.exists('best.pt'):
            model = YOLO('best.pt')
            st.sidebar.success("✅ Modelo personalizado cargado")
        else:
            # Usar modelo preentrenado de YOLO
            model = YOLO('yolov8n.pt')
            st.sidebar.info("ℹ️ Usando modelo YOLOv8 base")
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
        return None

def detect_ppe(image, model, conf_threshold):
    """Detecta equipos de protección en la imagen"""
    # Convertir PIL a formato OpenCV
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Realizar detección
    results = model(img_bgr, conf=conf_threshold)
    
    # Procesar resultados
    detections = []
    annotated_image = img_array.copy()
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Obtener coordenadas y clase
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())
            
            # Obtener nombre de la clase
            class_name = model.names[cls]
            
            detections.append({
                'class': class_name,
                'confidence': float(conf),
                'bbox': [int(x1), int(y1), int(x2), int(y2)]
            })
            
            # Dibujar en la imagen
            color = (0, 255, 0) if 'helmet' in class_name.lower() or 'vest' in class_name.lower() else (255, 0, 0)
            cv2.rectangle(annotated_image, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
            
            # Etiqueta
            label = f"{class_name}: {conf:.2f}"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated_image, (int(x1), int(y1) - 25), (int(x1) + w, int(y1)), color, -1)
            cv2.putText(annotated_image, label, (int(x1), int(y1) - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return annotated_image, detections

def analyze_safety(detections):
    """Analiza el cumplimiento de seguridad"""
    safety_items = {
        'helmet': False,
        'vest': False,
        'person': False
    }
    
    for det in detections:
        class_name = det['class'].lower()
        if 'helmet' in class_name or 'hardhat' in class_name or 'head' in class_name:
            safety_items['helmet'] = True
        if 'vest' in class_name or 'jacket' in class_name or 'safety' in class_name:
            safety_items['vest'] = True
        if 'person' in class_name:
            safety_items['person'] = True
    
    # Calcular score de seguridad
    if safety_items['person']:
        required = ['helmet', 'vest']
        compliant = sum([safety_items[item] for item in required])
        safety_score = (compliant / len(required)) * 100
    else:
        safety_score = 100  # No hay personas, no hay riesgo
    
    return safety_score, safety_items

# Header
st.markdown('<h1 class="main-header">🦺 AI Construction Safety Inspector</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050155.png", width=100)
    st.markdown("## ⚙️ Configuración")
    
    confidence = st.slider(
        "Umbral de Confianza",
        min_value=0.1,
        max_value=1.0,
        value=0.3,
        step=0.05,
        help="Ajusta la sensibilidad de detección"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Sobre el Proyecto")
    st.info("""
    **AI Safety Inspector** utiliza visión por computadora para:
    
    - 🎯 Detectar EPP (Equipo de Protección Personal)
    - ✅ Verificar cumplimiento de normas
    - 📈 Generar reportes de seguridad
    - 🚨 Identificar riesgos en tiempo real
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 EPP Detectado")
    st.markdown("""
    - 🪖 Cascos de seguridad
    - 🦺 Chalecos reflectivos
    - 👷 Trabajadores
    - 🏗️ Y más...
    """)

# Cargar modelo
model = load_model()

if model is None:
    st.error("⚠️ No se pudo cargar el modelo. Por favor verifica la instalación.")
    st.stop()

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📸 Inspección", "📊 Dashboard", "ℹ️ Guía"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Subir Imagen")
        uploaded_file = st.file_uploader(
            "Arrastra o selecciona una imagen",
            type=['jpg', 'jpeg', 'png'],
            help="Sube una foto del sitio de construcción"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagen Original", use_container_width=True)
            
            if st.button("🔍 Analizar Seguridad", use_container_width=True):
                with st.spinner("Analizando imagen..."):
                    # Detectar
                    annotated_img, detections = detect_ppe(image, model, confidence)
                    
                    # Analizar seguridad
                    safety_score, safety_items = analyze_safety(detections)
                    
                    # Guardar en session state
                    st.session_state['annotated'] = annotated_img
                    st.session_state['detections'] = detections
                    st.session_state['safety_score'] = safety_score
                    st.session_state['safety_items'] = safety_items
    
    with col2:
        if 'annotated' in st.session_state:
            st.markdown("### 🎯 Resultado del Análisis")
            st.image(st.session_state['annotated'], caption="Detecciones", use_container_width=True)
            
            # Métricas de seguridad
            score = st.session_state['safety_score']
            
            if score >= 80:
                st.markdown(f'<div class="safe-badge">✅ SEGURO ({score:.0f}%)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-badge">⚠️ RIESGO DETECTADO ({score:.0f}%)</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Detalles de detección
            st.markdown("### 📋 Detecciones")
            for i, det in enumerate(st.session_state['detections']):
                with st.expander(f"🎯 {det['class']} - {det['confidence']*100:.1f}%"):
                    st.write(f"**Confianza:** {det['confidence']*100:.1f}%")
                    st.write(f"**Ubicación:** {det['bbox']}")

with tab2:
    if 'detections' in st.session_state:
        st.markdown("### 📊 Dashboard de Seguridad")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Objetos Detectados", len(st.session_state['detections']))
        
        with col2:
            score = st.session_state['safety_score']
            st.metric("Score de Seguridad", f"{score:.0f}%", 
                     delta=f"{score-50:.0f}%" if score >= 50 else f"{score-50:.0f}%")
        
        with col3:
            helmet = "✅" if st.session_state['safety_items']['helmet'] else "❌"
            st.metric("Casco", helmet)
        
        with col4:
            vest = "✅" if st.session_state['safety_items']['vest'] else "❌"
            st.metric("Chaleco", vest)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de detecciones por tipo
            detection_counts = {}
            for det in st.session_state['detections']:
                cls = det['class']
                detection_counts[cls] = detection_counts.get(cls, 0) + 1

                df_counts = pd.DataFrame({
                        "Tipo de Objeto": list(detection_counts.keys()),
                        "Cantidad": list(detection_counts.values())
                        })

                fig = px.bar(
                        df_counts,
                         x="Tipo de Objeto",
                         y="Cantidad",
                         color="Cantidad",
                         title="🎯 Detecciones por Tipo",
                        color_continuous_scale="Viridis"
                         )

                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Gráfico de confianza
            confidences = [det['confidence'] for det in st.session_state['detections']]
            classes = [det['class'] for det in st.session_state['detections']]
            
            # Gráfico de confianza (FIX DEFINITIVO)
            confidences = [det['confidence'] for det in st.session_state['detections']]
            classes = [det['class'] for det in st.session_state['detections']]

            df_conf = pd.DataFrame({
                    "Detección": list(range(len(confidences))),
                    "Confianza": confidences,
                    "Clase": classes
                    })

            fig = px.scatter(
                df_conf,
                x="Detección",
                y="Confianza",
                color="Clase",
                title="📊 Nivel de Confianza por Detección",
                labels={
                    "Detección": "Detección #",
                    "Confianza": "Confianza"
                    }
                )

            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)


        
        # Gauge de seguridad
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=st.session_state['safety_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Score Global de Seguridad"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightcoral"},
                    {'range': [50, 80], 'color': "lightyellow"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Reporte descargable
        st.markdown("### 📄 Generar Reporte")
        if st.button("📥 Descargar Reporte PDF", use_container_width=True):
            st.info("Función de exportación a PDF disponible con librerías adicionales (reportlab)")
    else:
        st.info("👆 Sube y analiza una imagen primero para ver las estadísticas")

with tab3:
    st.markdown("## 📖 Guía de Uso")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Cómo Usar
        
        1. **Subir Imagen**: En la pestaña 'Inspección', sube una foto del sitio
        2. **Ajustar Sensibilidad**: Usa el slider en el sidebar
        3. **Analizar**: Haz clic en 'Analizar Seguridad'
        4. **Revisar**: Verifica las detecciones y el score
        5. **Dashboard**: Explora las métricas en la pestaña Dashboard
        
        ### 🎯 Mejores Prácticas
        
        - Usa imágenes con buena iluminación
        - Asegura que las personas sean visibles
        - Múltiples ángulos dan mejor análisis
        - Umbral de confianza: 0.3-0.5 recomendado
        """)
    
    with col2:
        st.markdown("""
        ### 🏭 Aplicaciones Industriales
        
        - **Construcción**: Cumplimiento de EPP
        - **Manufactura**: Seguridad en planta
        - **Minería**: Verificación de equipos
        - **Logística**: Control de almacenes
        
        ### 🛠️ Tecnologías Usadas
        
        - **YOLOv8**: Detección de objetos
        - **Streamlit**: Interfaz web
        - **OpenCV**: Procesamiento de imágenes
        - **Plotly**: Visualizaciones interactivas
        
        ### 📈 Próximas Mejoras
        
        - Detección en video en tiempo real
        - Alertas automáticas
        - Integración con bases de datos
        - Reconocimiento facial (privacidad)
        """)
    
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
    <strong>💡 Consejo Pro:</strong> Para mejores resultados, entrena el modelo con un dataset específico 
    de tu industria. El dataset de Kaggle "Hard Hat Detection" es perfecto para esto.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>AI Safety Inspector</strong> | Desarrollado con ❤️ para mejorar la seguridad laboral</p>
    <p>Powered by YOLOv8 + Streamlit | Hackathon 2025</p>
</div>
""", unsafe_allow_html=True)
