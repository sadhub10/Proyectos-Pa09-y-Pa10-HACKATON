import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# ==========================================
# CONFIGURACIÓN DE ENTORNO Y ESTILOS
# ==========================================
st.set_page_config(page_title="Sistema de Predicción Criminal", page_icon="🇵🇦", layout="wide")

# Inyección de CSS para identidad visual (Gradiente Dinámico)
st.markdown("""
    <style>
    /* Definición de keyframes para animación de fondo */
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Configuración del contenedor principal */
    .stApp {
        background: linear-gradient(-45deg, #4a0000, #080f5b, #700000, #000030);
        background-size: 400% 400%;
        animation: gradient-animation 15s ease infinite;
        color: white;
    }
    
    /* Optimización de tipografía para alto contraste */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 0px 0px 10px rgba(0,0,0, 0.8);
    }
    
    /* Estilización de métricas numéricas */
    div[data-testid="stMetricValue"] {
        color: #f0f2f6 !important;
        text-shadow: 0px 0px 5px black;
    }
    
    /* Normalización de inputs */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        color: black;
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
    """Carga y cachea el dataset histórico normalizado (Fuente de Verdad)."""
    try:
        # Se normalizan los nombres a mayúsculas para evitar duplicados por formato
        df = pd.read_excel('Dataset_Homicidios_Panama_2017_2024_NormalizadoFINAL.xlsx')
        df['PROVINCIA'] = df['PROVINCIA'].astype(str).str.upper().str.strip()
        return df
    except Exception as e: 
        st.error(f"Error crítico en carga de datos base: {e}")
        return None

@st.cache_data
def cargar_datos_contexto():
    """Carga variables exógenas (socioeconómicas) para enriquecimiento del modelo."""
    try:
        df = pd.read_csv('Datos_Contexto_Anual.csv')
        df['PROVINCIA'] = df['PROVINCIA'].astype(str).str.upper().str.strip()
        return df
    except Exception as e: 
        st.error(f"Error crítico en carga de contexto: {e}")
        return None

@st.cache_resource
def cargar_modelo():
    """Deserializa el modelo de Random Forest optimizado."""
    try:
        # Carga del modelo V4.0 (Socio-Metric Nexus - 9 Features)
        return joblib.load('modelo_homicidios_panama_socioeconomico_ULTRA.pkl')
    except Exception as e: 
        st.error(f"Fallo en inicialización del motor de inferencia: {e}")
        return None

# Inicialización de instancias de datos
df = cargar_datos_base()
df_contexto = cargar_datos_contexto()
modelo = cargar_modelo()

# Mapeo de meses para transformación numérica
MESES_NUM = {'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6, 
             'Julio':7, 'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}

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
        # LÓGICA DIRECTA: Extraer lista única del Excel base
        # Esto garantiza coincidencia exacta entre la selección y los datos
        provincias_disponibles = sorted(df['PROVINCIA'].unique())
        provincia = st.selectbox("Provincia", provincias_disponibles)

    st.markdown("---")
    
    # --- BLOQUE DE CONTEXTO SOCIOECONÓMICO (AUTOMÁTICO) ---
    # Búsqueda de registros en el dataset de contexto
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

    # --- BLOQUE DE VARIABLES TEMPORALES (LAG FEATURES) ---
    col_a, col_b = st.columns(2)
    
    # Determinación del periodo previo (t-1)
    mes_num = MESES_NUM[mes]
    if mes_num == 1:
        mes_ant, año_ant = 12, año - 1
    else:
        mes_ant, año_ant = mes_num - 1, año
        
    mes_nombres_inv = {v:k for k,v in MESES_NUM.items()}
    nombre_mes_ant = mes_nombres_inv[mes_ant]
    
    # Consulta de histórico para pre-llenado
    dato_hist = df[(df['AÑO'] == año_ant) & (df['MES'].str.upper() == nombre_mes_ant.upper()) & (df['PROVINCIA'] == provincia)]
    val_defecto = float(len(dato_hist)) if not dato_hist.empty else 0.0
    
    with col_a:
        lag1 = st.number_input(f"Homicidios en {nombre_mes_ant}", value=val_defecto, min_value=0.0)
    with col_b:
        prom3 = st.number_input("Promedio Trimestre Anterior", value=val_defecto, min_value=0.0)

    # --- MOTOR DE INFERENCIA ---
    if st.button("Calcular Riesgo Criminal", type="primary", use_container_width=True):
        
        # 1. Codificación de Categoría (Label Encoding en tiempo real)
        # Se usa la misma base categórica del entrenamiento para mantener consistencia
        cat_codes = pd.Categorical([provincia], categories=sorted(df['PROVINCIA'].unique())).codes
        prov_code = cat_codes[0]
        
        # 2. Cálculo de Volatilidad (Feature 9)
        # Estimación basada en la desviación absoluta entre el valor reciente y la tendencia trimestral
        volatilidad_estimada = abs(lag1 - prom3)
        
        # 3. Construcción del Vector de Entrada (9 Features)
        # Orden estricto: [AÑO, MES, PROV_CODE, LAG1, PROM3, VOLATILIDAD, POBLACION, DESEMPLEO, PANDILLAS]
        input_data = [[año, mes_num, prov_code, lag1, prom3, volatilidad_estimada, poblacion, desempleo, indice_pandilla]]
        
        # 4. Predicción
        pred = modelo.predict(input_data)[0]
        
        # 5. Visualización de Resultados
        st.markdown("### Resultados del Análisis Predictivo")
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicción Homicidios", f"{pred:.2f}")
        
        # Semáforo de Riesgo (KPI Visual)
        if pred < 2: 
            c2.metric("Nivel de Riesgo", "BAJO 🟢")
        elif pred < 8:
            c2.metric("Nivel de Riesgo", "MEDIO 🟡")
        else:
            c2.metric("Nivel de Riesgo", "ALTO 🔴")
            
        c3.metric("Tasa x 100k hab.", f"{(pred/poblacion)*100000:.2f}")

else:
    st.error("Error Crítico: No se han podido cargar los recursos necesarios (Dataset o Modelo). Verifique la integridad de los archivos.")