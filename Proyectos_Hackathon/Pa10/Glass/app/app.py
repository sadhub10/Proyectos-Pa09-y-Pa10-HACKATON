import streamlit as st
import datetime
import random
from PIL import Image

st.set_page_config(
    page_title="Healthy Station",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


def mock_analysis(image_uploader):
    """
    Función simulada que devuelve un diagnóstico aleatorio.
    Simula un pequeño retraso para emular el procesamiento.
    """
    st.toast(f"Analizando imagen: {image_uploader.name}...")
    with st.spinner("Procesando con modelo de IA..."):
        # aquí modelo:
        # from model_pneumonia import analyze_chest_xray
        # result = analyze_chest_xray(image_uploader.getvalue())
        import time
        time.sleep(2)

        # Resultados aleatorios para la demo
    diagnoses = ["Condición Normal", "Neumonía Detectada", "Tumor Cerebral Detectado", "Anomalía Leve",
                 "Requiere Revisión Adicional"]
    confidences = [random.randint(85, 99) for _ in diagnoses]
    recommendations = [
        "No se requiere acción inmediata. Monitoreo regular.",
        "Consulta urgente con un especialista recomendada.",
        "Se recomienda una biopsia y consulta con neuro-oncología.",
        "Observación y seguimiento en 6 meses.",
        "Repetir el estudio con contraste y consultar especialista."
    ]

    chosen_index = random.randint(0, len(diagnoses) - 1)

    return {
        "diagnosis": diagnoses[chosen_index],
        "confidence": f"{confidences[chosen_index]}%",
        "recommendation": recommendations[chosen_index],
        "raw_image": image_uploader.getvalue()
    }


#  Sesión
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_analysis_id" not in st.session_state:
    st.session_state.selected_analysis_id = None


# Callback
def select_analysis(analysis_id):
    st.session_state.selected_analysis_id = analysis_id


def go_home():
    st.session_state.selected_analysis_id = None


# Historial
with st.sidebar:
    st.title("🩺 Healthy Station")
    st.markdown("---")

    if st.button("➕ Nuevo Análisis", use_container_width=True):
        go_home()

    st.markdown("### Historial")
    if not st.session_state.history:
        st.caption("No hay análisis previos.")
    else:

        for analysis in reversed(st.session_state.history):
            analysis_id = analysis["id"]
            label = f"**{analysis['type']}** ({analysis['date'].strftime('%H:%M:%S')})"
            if st.button(label, key=f"hist_{analysis_id}", use_container_width=True):
                select_analysis(analysis_id)

    st.markdown("---")

# Vista Principal

# Menú desplegable/Pruebas
with st.expander("Información del Paciente", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Nombre del Paciente", "John Doe")
        patient_id = st.text_input("Cédula o ID", "123-456-789")
    with col2:
        patient_height = st.number_input("Altura (cm)", min_value=50, max_value=250, value=175)
        patient_weight = st.number_input("Peso (kg)", min_value=10, max_value=300, value=70)

    patient_info = {
        "name": patient_name,
        "id": patient_id,
        "height": patient_height,
        "weight": patient_weight
    }

# Lógica de Vistas

selected_analysis = None
if st.session_state.selected_analysis_id:
    try:
        selected_analysis = next(
            item for item in st.session_state.history if item["id"] == st.session_state.selected_analysis_id)
    except StopIteration:
        go_home()

    # VISTA RESULTADO
if selected_analysis:
    st.header(f"Resultados del Análisis: {selected_analysis['type']}")
    st.caption(f"Análisis realizado el {selected_analysis['date'].strftime('%d de %B, %Y a las %H:%M:%S')}")
    st.markdown("---")

    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        st.subheader("Datos del Paciente")
        st.write(f"**Nombre:** {selected_analysis['patient']['name']}")
        st.write(f"**Cédula/ID:** {selected_analysis['patient']['id']}")
        st.write(f"**Altura:** {selected_analysis['patient']['height']} cm")
        st.write(f"**Peso:** {selected_analysis['patient']['weight']} kg")
        st.markdown("---")
        st.subheader("Diagnóstico por IA")
        st.metric("Resultado", selected_analysis['result']['diagnosis'])
        st.metric("Confianza del Modelo", selected_analysis['result']['confidence'])
        st.write(f"**Recomendación:** {selected_analysis['result']['recommendation']}")

    with res_col2:
        st.subheader("Imagen Analizada")
        st.image(selected_analysis['result']['raw_image'], use_column_width=True, caption="Radiografía procesada")

# VISTA ANÁLISIS
else:
    st.header("Iniciar Nuevo Análisis Médico")
    st.markdown("Seleccione el tipo de análisis que desea realizar y cargue la imagen correspondiente.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Análisis de Tórax")
        chest_uploader = st.file_uploader(
            "Cargar radiografía de tórax",
            type=["png", "jpg", "jpeg"],
            key="chest_uploader"
        )
        if chest_uploader:
            result = mock_analysis(chest_uploader)
            analysis_id = datetime.datetime.now().timestamp()
            new_analysis = {
                "id": analysis_id,
                "type": "Análisis de Tórax",
                "date": datetime.datetime.now(),
                "patient": patient_info,
                "result": result
            }
            st.session_state.history.append(new_analysis)
            select_analysis(analysis_id)
            st.rerun()

    with col2:
        st.subheader("Análisis Cerebral")
        brain_uploader = st.file_uploader(
            "Cargar resonancia magnética cerebral",
            type=["png", "jpg", "jpeg"],
            key="brain_uploader"
        )
        if brain_uploader:
            result = mock_analysis(brain_uploader)
            analysis_id = datetime.datetime.now().timestamp()
            new_analysis = {
                "id": analysis_id,
                "type": "Análisis Cerebral",
                "date": datetime.datetime.now(),
                "patient": patient_info,
                "result": result
            }
            st.session_state.history.append(new_analysis)
            select_analysis(analysis_id)
            st.rerun()