import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# ==========================================
# CONFIGURACIÓN DE ENTORNO Y ESTILOS
# ==========================================
st.set_page_config(page_title="Sistema de Predicción Criminal", page_icon="🇵🇦", layout="wide")

# Inyección de CSS para identidad visual (Gradiente Dinámico y Texto Blanco)
st.markdown("""
    <style>
    /* 1. ANIMACIÓN DE FONDO */
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #4a0000, #080f5b, #700000, #000030, #4a0000);
        background-size: 400% 400%;
        animation: gradient-animation 20s ease-in-out infinite;
    }
    
    /* 2. TEXTOS GENERALES (Títulos, Párrafos, Etiquetas) - TODO BLANCO */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, span, div {
        color: white !important;
        text-shadow: 0px 0px 5px rgba(0,0,0, 0.5); /* Sombra suave para leer mejor */
    }
    
    /* 3. INPUTS Y CAJAS DE TEXTO (Números y Selecciones) */
    /* Fuerza el color blanco en lo que escribe el usuario */
    .stNumberInput input {
        color: white !important;
        -webkit-text-fill-color: white !important;
        caret-color: white !important; /* El cursor también blanco */
    }
    
    /* El texto seleccionado en los desplegables */
    .stSelectbox div[data-baseweb="select"] div {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }
    
    /* 4. MÉTRICAS (Números Grandes) */
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px black;
    }
    div[data-testid="stMetricLabel"] {
        color: #e0e0e0 !important; /* Un blanco un pelín gris para diferenciar la etiqueta */
    }
    
    /* 5. FONDOS DE RIESGO (Semáforo) */
    .low-risk {
        background: linear-gradient(-45deg, #007AFF, #00BFFF, #007AFF) !important;
        background-size: 400% 400%;
        animation: gradient-animation 20s ease-in-out infinite !important;
    }
    .medium-risk {
        background: linear-gradient(-45deg, #FF9500, #FFCC00, #FF9500) !important;
        background-size: 400% 400%;
        animation: gradient-animation 20s ease-in-out infinite !important;
    }
    .high-risk {
        background: linear-gradient(-45deg, #FF3B30, #FF6347, #FF3B30) !important;
        background-size: 400% 400%;
        animation: gradient-animation 20s ease-in-out infinite !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. GESTIÓN DE RECURSOS Y DATOS (ETL)
# ==========================================
def obtener_ruta_recurso(nombre_archivo):
    """Resuelve la ruta absoluta de los recursos para compatibilidad entre entornos."""  
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_recursos = os.path.join(directorio_actual, '..', 'recursos')
    if not os.path.exists(ruta_recursos):
        return nombre_archivo
    return os.path.join(ruta_recursos, nombre_archivo)

@st.cache_data
def cargar_datos_base():
    try:
        archivo = obtener_ruta_recurso('Dataset_Homicidios_Panama_2017_2024_NormalizadoFINAL.xlsx')
        if not os.path.exists(archivo): archivo = 'Dataset_Homicidios_Panama_2017_2024_NormalizadoFINAL.xlsx'
        
        df = pd.read_excel(archivo)
        df['PROVINCIA'] = df['PROVINCIA'].astype(str).str.upper().str.strip()
        return df
    except Exception as e: 
        st.error(f"Error crítico en carga de datos base: {e}")
        return None

@st.cache_data
def cargar_datos_contexto():
    try:
        archivo = obtener_ruta_recurso('Datos_Contexto_Anual_MEJORADO.csv')
        if not os.path.exists(archivo): archivo = 'Datos_Contexto_Anual_MEJORADO.csv'

        df = pd.read_csv(archivo)
        df['PROVINCIA'] = df['PROVINCIA'].astype(str).str.upper().str.strip()
        return df
    except Exception as e: 
        st.error(f"Error crítico en carga de contexto: {e}")
        return None

@st.cache_resource
def cargar_modelo():
    try:
        archivo = obtener_ruta_recurso('modelo_homicidios_panama_socioeconomico_ULTRA.pkl')
        if not os.path.exists(archivo): archivo = 'modelo_homicidios_panama_socioeconomico_ULTRA.pkl'
        return joblib.load(archivo)
    except Exception as e: 
        st.error(f"Fallo en inicialización del motor de inferencia: {e}")
        return None

# Inicialización de instancias de datos
df = cargar_datos_base()
df_contexto = cargar_datos_contexto()
modelo = cargar_modelo()

# Mapeo de meses
MESES_NUM = {'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6, 
             'Julio':7, 'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}
MESES_INV = {v: k for k, v in MESES_NUM.items()}

# ==========================================
# 2. INTERFAZ DE USUARIO E INFERENCIA
# ==========================================
st.title("Predictor de Riesgo Criminal (Modelo Socioeconómico)")
st.markdown("""
Sistema de **Inteligencia Artificial** basado en arquitectura híbrida: integra inercia temporal (Lag Features) 
con indicadores estructurales (Desempleo, Población, Actividad de Pandillas).
""")

if modelo is not None and df is not None and df_contexto is not None:
    
    # --- BLOQUE DE PARAMETRIZACIÓN ---
    col1, col2, col3 = st.columns(3)
    with col1:
        año = st.number_input("Año Objetivo", 2024, 2030, 2025)
    with col2:
        mes = st.selectbox("Mes", list(MESES_NUM.keys()))
    with col3:
        provincias_disponibles = sorted(df['PROVINCIA'].unique())
        # CAMBIO REALIZADO AQUÍ: Etiqueta cambiada a "Area geografica"
        provincia = st.selectbox("Area geografica", provincias_disponibles)

    st.markdown("---")
    
    # --- BLOQUE DE CONTEXTO SOCIOECONÓMICO ---
    año_busqueda = min(año, df_contexto['AÑO'].max())
    
    fila_contexto = df_contexto[
        (df_contexto['AÑO'] == año_busqueda) & 
        (df_contexto['PROVINCIA'] == provincia)
    ]
    
    if not fila_contexto.empty:
        poblacion = fila_contexto.iloc[0]['POBLACION_ESTIMADA']
        desempleo = fila_contexto.iloc[0]['TASA_DESEMPLEO']
        indice_pandilla = fila_contexto.iloc[0]['INDICE_PANDILLAS']
        st.info(f"Contexto Demográfico Detectado ({año_busqueda}): Población: {poblacion:,.0f} | Desempleo: {desempleo}% | Índice Pandillas: {indice_pandilla}/10")
    else:
        st.warning(f"Aviso: No se encontraron datos socioeconómicos específicos para '{provincia}' en el año {año_busqueda}. Se usarán valores predeterminados.")
        poblacion, desempleo, indice_pandilla = 0, 0, 0

    # --- CÁLCULO INTELIGENTE DE HISTÓRICOS ---
    col_a, col_b = st.columns(2)
    mes_num_actual = MESES_NUM[mes]
    
    # 1. Calcular LAG 1 (Mes Anterior exacto)
    if mes_num_actual == 1:
        mes_lag1, año_lag1 = 12, año - 1
    else:
        mes_lag1, año_lag1 = mes_num_actual - 1, año
    nombre_mes_lag1 = MESES_INV[mes_lag1]
    
    data_lag1 = df[(df['AÑO'] == año_lag1) & (df['MES'].str.upper() == nombre_mes_lag1.upper()) & (df['PROVINCIA'] == provincia)]
    val_lag1 = float(len(data_lag1))

    # 2. Calcular PROMEDIO TRIMESTRAL (Últimos 3 meses reales)
    homicidios_trimestre = []
    for i in range(1, 4):
        target_mes = mes_num_actual - i
        target_año = año
        if target_mes <= 0:
            target_mes += 12
            target_año -= 1
        nombre_mes_target = MESES_INV[target_mes]
        data_mes = df[(df['AÑO'] == target_año) & (df['MES'].str.upper() == nombre_mes_target.upper()) & (df['PROVINCIA'] == provincia)]
        homicidios_trimestre.append(len(data_mes))
    
    val_prom3 = sum(homicidios_trimestre) / 3.0

    with col_a:
        lag1 = st.number_input(f"Homicidios en {nombre_mes_lag1} (Mes Anterior)", value=val_lag1, min_value=0.0)
    with col_b:
        prom3 = st.number_input("Promedio Trimestre Anterior (Calculado)", value=val_prom3, min_value=0.0)

    # --- MOTOR DE INFERENCIA ---
    if st.button("Calcular Riesgo Criminal", type="primary", use_container_width=True):
        
        cat_codes = pd.Categorical([provincia], categories=sorted(df['PROVINCIA'].unique())).codes
        prov_code = cat_codes[0]
        volatilidad_estimada = abs(lag1 - prom3)
        input_data = [[año, mes_num_actual, prov_code, lag1, prom3, volatilidad_estimada, poblacion, desempleo, indice_pandilla]]
        pred = modelo.predict(input_data)[0]
        
        st.markdown("### Resultados del Análisis Predictivo")
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicción Homicidios", f"{pred:.2f}")
        
        risk_class = ""
        if pred < 2: 
            c2.metric("Nivel de Riesgo", "BAJO 🟢")
            risk_class = "low-risk"
        elif pred < 8:
            c2.metric("Nivel de Riesgo", "MEDIO 🟡")
            risk_class = "medium-risk"
        else:
            c2.metric("Nivel de Riesgo", "ALTO 🔴")
            risk_class = "high-risk"
            
        c3.metric("Tasa x 100k hab.", f"{(pred/poblacion)*100000:.2f}")
        
        if risk_class:
            st.markdown(f'<script>document.querySelector(".stApp").className = "stApp {risk_class}";</script>', unsafe_allow_html=True)

else:
    st.error("Error Crítico: No se han podido cargar los recursos necesarios. Verifique archivos de datos y modelo.")
