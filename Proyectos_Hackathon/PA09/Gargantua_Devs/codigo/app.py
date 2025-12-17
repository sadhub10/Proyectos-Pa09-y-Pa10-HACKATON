import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Análisis Homicidios Panamá (AI)", page_icon="🇵🇦", layout="wide")

# ==========================================
# 1. CARGA DE RECURSOS
# ==========================================
@st.cache_data
def cargar_datos_base():
    # Carga datos históricos de crímenes
    try:
        # CORRECCIÓN: Agregué 'FINAL' al nombre del archivo para que coincida con tu carpeta
        return pd.read_excel('Dataset_Homicidios_Panama_2017_2024_NormalizadoFINAL.xlsx')
    except Exception as e: 
        # Esto imprimirá el error real en la pantalla si falla, para que sepas qué es
        st.error(f"Error cargando Excel: {e}")
        return None

@st.cache_data
def cargar_datos_contexto():
    # Carga la "memoria socioeconómica" (CSV)
    try:
        # CORRECCIÓN: Usamos ruta relativa (solo el nombre) porque el archivo está AL LADO de app.py
        # Esto es mucho más seguro que poner "C:/Users/Oliver..."
        df = pd.read_csv('Datos_Contexto_Anual.csv')
        
        # Estandarizar provincias a mayúsculas para evitar errores de búsqueda
        df['PROVINCIA'] = df['PROVINCIA'].astype(str).str.upper().str.strip()
        return df
    except Exception as e: 
        st.error(f"Error cargando CSV Contexto: {e}")
        return None

@st.cache_resource
def cargar_modelo():
    try:
        # ACTUALIZACIÓN FINAL: Usamos el modelo ULTRA ROBUSTO (Gap < 2%)
        return joblib.load('modelo_homicidios_panama_socioeconomico_ULTRA.pkl')
    except Exception as e: 
        st.error(f"Error cargando Modelo ULTRA: {e}")
        return None

df = cargar_datos_base()
df_contexto = cargar_datos_contexto() # <--- Nuevo Dataset
modelo = cargar_modelo()

# Mapas auxiliares
MESES_NUM = {'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6, 
             'Julio':7, 'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}

# ==========================================
# 2. INTERFAZ: PREDICTOR AVANZADO
# ==========================================
st.title("🔮 Predictor de Riesgo Criminal (Modelo Socioeconómico)")
st.markdown("""
Este sistema utiliza Inteligencia Artificial integrando **Lag Features** (historia reciente) 
con **Variables Socioeconómicas** (Desempleo, Población, Pandillas) para una predicción precisa.
""")

if modelo is not None and df is not None and df_contexto is not None:
    
    # --- FILA 1: DATOS BÁSICOS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        año = st.number_input("📅 Año", 2024, 2030, 2025)
    with col2:
        mes = st.selectbox("📆 Mes", list(MESES_NUM.keys()))
    with col3:
        # Obtenemos provincias del archivo de contexto para asegurar coincidencia
        provincias_disp = sorted(df_contexto['PROVINCIA'].unique())
        provincia = st.selectbox("📍 Provincia", provincias_disp)

    st.markdown("---")
    
    # --- LÓGICA AUTOMÁTICA DE CONTEXTO ---
    # Buscamos los datos socioeconómicos automáticamente en el CSV
    # Si el año seleccionado es mayor al que tenemos en el CSV (ej 2026), usamos el último disponible (2025)
    año_busqueda = min(año, df_contexto['AÑO'].max())
    
    fila_contexto = df_contexto[
        (df_contexto['AÑO'] == año_busqueda) & 
        (df_contexto['PROVINCIA'] == provincia)
    ]
    
    if not fila_contexto.empty:
        poblacion = fila_contexto.iloc[0]['POBLACION_ESTIMADA']
        desempleo = fila_contexto.iloc[0]['TASA_DESEMPLEO']
        indice_pandilla = fila_contexto.iloc[0]['INDICE_PANDILLAS']
        
        st.info(f"🧠 **Contexto Automático Detectado ({año_busqueda}):** Población: {poblacion:,.0f} | Desempleo: {desempleo}% | Índice Pandillas: {indice_pandilla}/10")
    else:
        st.error("⚠️ No se encontraron datos socioeconómicos para esta zona. Se usarán valores por defecto.")
        poblacion, desempleo, indice_pandilla = 0, 0, 0

    # --- FILA 2: VARIABLES TEMPORALES (LAG) ---
    col_a, col_b = st.columns(2)
    
    # Lógica de "Retrovisor" (Buscar datos reales del mes anterior si existen)
    mes_num = MESES_NUM[mes]
    if mes_num == 1:
        mes_ant, año_ant = 12, año - 1
    else:
        mes_ant, año_ant = mes_num - 1, año
        
    # Buscar en histórico
    mes_nombres_inv = {v:k for k,v in MESES_NUM.items()}
    nombre_mes_ant = mes_nombres_inv[mes_ant]
    
    dato_hist = df[(df['AÑO'] == año_ant) & (df['MES'].str.upper() == nombre_mes_ant.upper()) & (df['PROVINCIA'] == provincia)]
    val_defecto = float(len(dato_hist)) if not dato_hist.empty else 0.0
    
    with col_a:
        lag1 = st.number_input(f"🔙 Homicidios en {nombre_mes_ant}", value=val_defecto, min_value=0.0)
    with col_b:
        prom3 = st.number_input("📉 Promedio Trimestre Anterior", value=val_defecto, min_value=0.0)

    # --- BOTÓN DE PREDICCIÓN ---
    if st.button("🚀 Calcular Riesgo", type="primary", use_container_width=True):
        
        # 1. Preparar códigos numéricos
        prov_code = pd.Categorical([provincia], categories=sorted(df['PROVINCIA'].unique())).codes[0]
        if prov_code == -1: prov_code = 0 # Fallback
        
        # 2. Vector de entrada (8 Variables)
        # [AÑO, MES, PROV_CODE, LAG1, PROM3, POBLACION, DESEMPLEO, PANDILLAS]
        input_data = [[año, mes_num, prov_code, lag1, prom3, poblacion, desempleo, indice_pandilla]]
        
        # 3. Predecir
        pred = modelo.predict(input_data)[0]
        
        # 4. Mostrar Resultado
        st.markdown("### 🎯 Resultados del Análisis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicción Homicidios", f"{pred:.2f}")
        
        # Nivel de Riesgo Dinámico
        if pred < 2: 
            c2.metric("Nivel de Riesgo", "BAJO 🟢")
        elif pred < 8:
            c2.metric("Nivel de Riesgo", "MEDIO 🟡")
        else:
            c2.metric("Nivel de Riesgo", "ALTO 🔴")
            
        c3.metric("Tasa x 100k hab.", f"{(pred/poblacion)*100000:.2f}")

else:
    st.warning("⚠️ Faltan archivos clave (Dataset original, CSV de Contexto o Modelo .pkl). Verifica tu carpeta.")