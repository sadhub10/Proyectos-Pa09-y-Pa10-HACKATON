import streamlit as st
import requests

st.set_page_config(
    page_title="Healthy Station",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "view" not in st.session_state:
    st.session_state.view = "new"

if "selected_id" not in st.session_state:
    st.session_state.selected_id = None

def go_new_patient():
    st.session_state.view = "new"
    st.session_state.selected_id = None


def go_patient_file(cedula):
    st.session_state.view = "file"
    st.session_state.selected_id = cedula

def show_form_create_new_patient():
    with st.expander("➕ Crear nuevo expediente", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Nombre del Paciente")
            st.text_input("Cédula")

        with col2:
            st.text_input("Altura (cm)")
            st.text_input("Peso (kg)")

            st.button("Crear Expediente")


def show_file_patient(cedula):
    with st.spinner("Cargando expediente..."):
        response = requests.get(
            f"http://localhost:8001/paciente/{cedula}"
        )

    if response.status_code != 200:
        st.error(response.json().get("detail", "Error"))
        return

    paciente = response.json()

    with st.expander("Información del Paciente", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                "Nombre del Paciente",
                value=paciente["name"],
                disabled=True
            )
            st.text_input(
                "Cédula",
                value=paciente["cedula"],
                disabled=True
            )

        with col2:
            st.text_input(
                "Altura (cm)",
                value=paciente["altura"],
                disabled=True
            )
            st.text_input(
                "Peso (kg)",
                value=paciente["peso"],
                disabled=True
            )

    with st.expander("➕ Nuevo chequeo", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.button("Análisis de neumonía")
            st.file_uploader(
                "Cargar radiografía de tórax",
                type=["png", "jpg", "jpeg"],
                key="chest_uploader"
            )

        with col2:
            st.button("Análisis de tumor cerebral")
            st.file_uploader(
                "Cargar resonancia magnética cerebral",
                type=["png", "jpg", "jpeg"],
                key="brain_uploader"
            )

if st.session_state.view == "new":
    show_form_create_new_patient()

elif st.session_state.view == "file":
    show_file_patient(st.session_state.selected_id)

with st.sidebar:
    st.title("🩺 Healthy Station")
    st.markdown("---")

    st.button("➕ Nuevo expediente", on_click=go_new_patient)

    st.markdown("### Expedientes")

    response = requests.get("http://localhost:8001/paciente")

    if response.status_code == 200:
        expedientes = response.json()

        for paciente in expedientes:
            st.button(
                paciente["name"],
                key=f"pac_{paciente['cedula']}",
                on_click=go_patient_file,
                args=(paciente["cedula"],)
            )
    else:
        st.error("No se pudieron cargar los expedientes")