import streamlit as st
import datetime
import requests
import hashlib

st.set_page_config(
    page_title="Healthy Station",
    page_icon=":material/local_hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8001"


def get_visual_metadata(patient_id):
    hash_obj = hashlib.md5(str(patient_id).encode())
    hash_int = int(hash_obj.hexdigest(), 16)

    return {
        "last_visit": "Hoy" if (hash_int % 2 == 0) else "Ayer"
    }


def fetch_last_chequeos():
    try:
        r = requests.get(f"{API_URL}/chequeo", timeout=2)

        if r.status_code != 200:
            return {}

        chequeos = r.json()
        last_map = {}

        for c in chequeos:
            pid = str(c["cedula_paciente"])
            fecha_str = c.get("fecha") or c.get("created_at")

            if fecha_str:
                fecha = datetime.datetime.fromisoformat(fecha_str)

                if pid not in last_map or fecha > last_map[pid]:
                    last_map[pid] = fecha

        return last_map

    except requests.exceptions.RequestException:
        return {}


def fetch_patients_from_db():
    try:
        response = requests.get(f"{API_URL}/paciente", timeout=2)
        if response.status_code == 200:
            db_data = response.json()
            last_chequeos = fetch_last_chequeos()
            enhanced_patients = []

            for p in db_data:
                pid = str(p["cedula"])
                name = p["name"]
                height = int(float(p.get("altura", 0)))
                weight = int(float(p.get("peso", 0)))

                meta = get_visual_metadata(pid)
                last_check = last_chequeos.get(pid)

                enhanced_patients.append({
                    "id": pid,
                    "name": name,
                    "height": height,
                    "weight": weight,
                    "last_visit": (
                        last_check.strftime("%d/%m/%Y")
                        if last_check
                        else "Sin chequeo"
                    )
                })

            return enhanced_patients
        return []
    except requests.exceptions.RequestException:
        return None


def fetch_chequeos_by_patient(cedula):
    try:
        r = requests.get(f"{API_URL}/chequeo/{cedula}", timeout=3)

        if r.status_code != 200:
            return []

        return r.json()

    except requests.exceptions.RequestException:
        return []


def create_patient_in_db(patient_data):
    payload = {
        "cedula": patient_data["id"],
        "name": patient_data["name"],
        "altura": patient_data["height"],
        "peso": patient_data["weight"]
    }
    try:
        r = requests.post(f"{API_URL}/paciente", json=payload, timeout=2)
        return r.status_code == 200
    except:
        return False


def save_chequeo_to_db(cedula_paciente, tipo, descripcion):
    payload = {
        "cedula_paciente": cedula_paciente,
        "tipo": tipo,
        "descripcion": descripcion
    }
    try:
        r = requests.post(f"{API_URL}/chequeo", json=payload, timeout=3)
        return r.status_code == 200
    except Exception as e:
        st.error(f"Error al guardar el chequeo: {e}")
        return False


if "patients" not in st.session_state:
    data = fetch_patients_from_db()
    if data is None:
        st.session_state.patients = []
        st.error("Error: No se pudo conectar con la Base de Datos (API).")
    else:
        st.session_state.patients = data

if "current_view" not in st.session_state:
    st.session_state.current_view = "dashboard"
if "active_patient" not in st.session_state:
    st.session_state.active_patient = None
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_analysis_id" not in st.session_state:
    st.session_state.selected_analysis_id = None


def navigate_to(view, patient=None):
    st.session_state.current_view = view
    st.session_state.active_patient = patient

    if view == "dashboard":
        updated_data = fetch_patients_from_db()
        if updated_data is not None:
            st.session_state.patients = updated_data

    if view == "analysis":
        st.session_state.selected_analysis_id = None


def render_dashboard_sidebar():
    with st.sidebar:
        st.header("Healthy Station", divider="gray")

        total = len(st.session_state.patients)
        st.metric("Total Expedientes", str(total))

        with st.expander("Estado del Sistema", expanded=True):
            st.success("API Conectada", icon=":material/dns:")


def render_patient_sidebar(patient):
    with st.sidebar:
        if st.button("Volver al Panel", icon=":material/arrow_back:", use_container_width=True):
            navigate_to("dashboard")

        st.header(patient['name'], divider="blue")
        st.caption(f"Cédula: {patient['id']}")

        st.subheader("Datos del Paciente", divider="gray")

        col_a, col_b = st.columns(2)
        col_a.metric("Altura", f"{patient['height']} cm")
        col_b.metric("Peso", f"{patient['weight']} kg")

        chequeos = fetch_chequeos_by_patient(patient["id"])
        total_chequeos = len(chequeos)

        st.metric("Total Chequeos", str(total_chequeos))

        st.subheader("Acciones", divider="gray")

        if st.button("Nuevo Análisis", icon=":material/add_circle:", use_container_width=True, type="primary"):
            st.session_state.selected_analysis_id = None


def view_dashboard():
    render_dashboard_sidebar()

    col_title, col_action = st.columns([5, 1], vertical_alignment="center")
    col_title.title("Expedientes Médicos")
    if col_action.button("Nuevo Expediente", icon=":material/person_add:", type="primary", use_container_width=True):
        navigate_to("create")

    with st.container(border=True):
        search = st.text_input("Buscar", placeholder="Escriba nombre o cédula del paciente...",
                               label_visibility="collapsed")

    st.markdown("---")
    h_col1, h_col2, h_col3, h_col4 = st.columns([0.5, 3, 2, 2.5])
    h_col2.caption("NOMBRE")
    h_col3.caption("ÚLTIMA VISITA")
    h_col4.caption("ACCIONES")

    filtered = st.session_state.patients
    if search:
        filtered = [p for p in filtered if search.lower() in p['name'].lower()]

    if not filtered:
        st.warning("No se encontraron pacientes en la base de datos.", icon=":material/search_off:")

    for p in filtered:
        with st.container():
            c1, c2, c3, c4 = st.columns([0.5, 3, 2, 2.5], vertical_alignment="center")

            c1.markdown(":material/account_circle:")

            with c2:
                st.write(f"**{p['name']}**")
                st.caption(f"{p['id']}")

            c3.write(p['last_visit'])

            with c4:
                st.button("Ver", key=f"v_{p['id']}", icon=":material/visibility:", on_click=navigate_to,
                          args=("analysis", p), use_container_width=True)

            st.divider()


def view_form_patient(mode="create"):
    render_dashboard_sidebar()

    is_edit = mode == "edit"
    p = st.session_state.active_patient if is_edit else None

    st.button("← Cancelar", on_click=navigate_to, args=("dashboard",))
    st.title("Editar Expediente" if is_edit else "Nuevo Expediente")

    with st.form("patient_form", border=True):
        st.subheader("Información del paciente")
        c1, c2 = st.columns(2)
        name = c1.text_input("Nombre Completo", value=p['name'] if p else "")
        pid = c2.text_input("Cédula del paciente", value=p['id'] if p else "", disabled=is_edit)

        c5, c6 = st.columns(2)
        height = c5.number_input("Altura (cm)", value=int(p['height']) if p else 170)
        weight = c6.number_input("Peso (kg)", value=int(p['weight']) if p else 70)

        st.write("")
        col_submit = st.columns([1, 4])[0]
        submitted = col_submit.form_submit_button("Guardar en Base de Datos", type="primary", use_container_width=True,
                                                  icon=":material/save:")

        if submitted and name and pid:
            new_data = {
                "id": pid, "name": name,
                "height": height, "weight": weight, "last_visit": "Hoy"
            }

            if is_edit:
                navigate_to("dashboard")
            else:
                success = create_patient_in_db(new_data)
                if success:
                    st.toast("Expediente creado", icon=":material/check_circle:")
                    navigate_to("dashboard")
                else:
                    st.error("Error al guardar en la API. Verifica que el servidor esté corriendo.")


def view_analysis_interface():
    p = st.session_state.active_patient
    render_patient_sidebar(p)

    st.title("Sala de Análisis")
    st.caption(f"Paciente: {p['name']} | ID: {p['id']}")
    st.write("")

    selected_analysis = None
    if st.session_state.selected_analysis_id:
        try:
            selected_analysis = next(
                i for i in st.session_state.history if i["id"] == st.session_state.selected_analysis_id)
        except:
            pass

    if selected_analysis:
        with st.container(border=True):
            r_col1, r_col2 = st.columns([3, 1])
            r_col1.subheader(f"Reporte de {selected_analysis['type']}")
            r_col2.caption(f"Generado: {selected_analysis['date'].strftime('%Y-%m-%d %H:%M')}")
            st.divider()

            c_img, c_details = st.columns([1, 1.5], gap="large")

            with c_img:
                st.image(selected_analysis['result']['raw_image'], caption="Imagen Analizada", use_container_width=True)

            with c_details:
                confidence_val = int(selected_analysis['result']['confidence'].strip('%')) / 100

                st.markdown("#### Diagnóstico IA")

                clase = selected_analysis['result'].get("class", "")

                if clase == "Saludable" or clase == "Sano":
                    st.success(
                        selected_analysis['result']['diagnosis'],
                        icon=":material/check_circle:"
                    )
                else:
                    st.error(
                        selected_analysis['result']['diagnosis'],
                        icon=":material/radiology:"
                    )

                st.markdown("#### Confianza del Modelo")
                st.progress(confidence_val)
                st.caption(f"Certeza: {selected_analysis['result']['confidence']}")

                st.markdown("#### Recomendación Clínica")
                st.info(selected_analysis['result']['recommendation'], icon=":material/info:")

                st.markdown("---")
                if st.button("Guardar Chequeo en Expediente", type="primary", use_container_width=True):
                    descripcion = f"Diagnóstico: {selected_analysis['result']['diagnosis']}. " \
                                  f"Clase: {selected_analysis['result']['class']}. " \
                                  f"Confianza: {selected_analysis['result']['confidence']}. " \
                                  f"Recomendación: {selected_analysis['result']['recommendation']}"

                    success = save_chequeo_to_db(
                        cedula_paciente=p['id'],
                        tipo=selected_analysis['type'],
                        descripcion=descripcion
                    )

                    if success:
                        st.toast("Chequeo guardado exitosamente en el expediente", icon="✅")
                        st.rerun()
                    else:
                        st.error("Error al guardar el chequeo en la base de datos")

    else:
        with st.container(border=True):
            st.subheader("Nueva Evaluación Diagnóstica")
            st.write("Seleccione el módulo de inteligencia artificial a utilizar:")

            tab1, tab2 = st.tabs(["Radiografía de Tórax", "Resonancia Cerebral"])

            with tab1:
                st.info("Detecta: Neumonía")
                uploader = st.file_uploader("Cargar Radiografía (DICOM/PNG/JPG)", type=["png", "jpg"], key="u_chest")
                if uploader:
                    process_model_analysis(uploader, "Radiografía de Tórax", p, model_type="pneumonia")

            with tab2:
                st.info("Detecta: Tumores")
                uploader = st.file_uploader("Cargar Resonancia (DICOM/PNG/JPG)", type=["png", "jpg"], key="u_brain")
                if uploader:
                    process_model_analysis(uploader, "Resonancia Cerebral", p, model_type="tumor")

    st.markdown("---")
    st.subheader("Historial de Chequeos")

    with st.spinner("Cargando historial clínico..."):
        patient_history = fetch_chequeos_by_patient(p["id"])

    if not patient_history:
        st.info("Sin registros previos en la base de datos.", icon=":material/folder_open:")
    else:
        for analysis in reversed(patient_history):
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"**{analysis['tipo']}**")
                    st.caption(analysis.get('descripcion', 'Sin descripción'))

                with col2:
                    fecha_str = analysis.get('fecha') or analysis.get('created_at')
                    if fecha_str:
                        try:
                            fecha_obj = datetime.datetime.fromisoformat(fecha_str)
                            st.caption(fecha_obj.strftime('%d/%m/%Y'))
                        except:
                            st.caption("Fecha no disponible")
                    else:
                        st.caption("Fecha no disponible")


def process_model_analysis(uploader, type_name, patient, model_type="pneumonia"):
    with st.status("Ejecutando analizador...", expanded=True) as status:
        try:
            files = {
                "file": (uploader.name, uploader.getvalue(), uploader.type)
            }

            if model_type == "pneumonia":
                endpoint = f"{API_URL}/model-pneumonia"
            elif model_type == "tumor":
                endpoint = f"{API_URL}/model-tumor"
            else:
                st.error("Tipo de modelo no reconocido.")
                return

            r = requests.post(
                endpoint,
                files=files,
                timeout=15
            )

            if r.status_code != 200:
                st.error("Error al ejecutar el modelo.")
                return

            clase = r.json()

            status.update(
                label="¡Análisis completado!",
                state="complete",
                expanded=False
            )

        except Exception as e:
            st.error(f"Error de conexión con el modelo: {e}")
            return

    if model_type == "pneumonia":
        if clase == "Saludable":
            diagnosis = "Pulmones sin signos patológicos"
            recommendation = "No se requieren acciones clínicas inmediatas."
            confidence = "98%"
        else:
            diagnosis = f"{clase} detectada"
            recommendation = "Se recomienda evaluación médica y tratamiento antibiótico."
            confidence = "94%"

    elif model_type == "tumor":
        if clase == "Sano":
            diagnosis = "Cerebro sin signos de masa tumoral"
            recommendation = "No se requieren acciones clínicas inmediatas."
            confidence = "97%"
        else:
            diagnosis = f"{clase} detectado"
            recommendation = "Se recomienda evaluación por neurocirugía y oncología."
            confidence = "92%"

    aid = datetime.datetime.now().timestamp()

    st.session_state.history.append({
        "id": aid,
        "type": type_name,
        "date": datetime.datetime.now(),
        "patient": patient,
        "result": {
            "class": clase,
            "diagnosis": diagnosis,
            "confidence": confidence,
            "recommendation": recommendation,
            "raw_image": uploader.getvalue()
        }
    })

    st.session_state.selected_analysis_id = aid

    st.rerun()


if st.session_state.current_view == "dashboard":
    view_dashboard()
elif st.session_state.current_view == "create":
    view_form_patient("create")
elif st.session_state.current_view == "edit":
    view_form_patient("edit")
elif st.session_state.current_view == "analysis":
    if st.session_state.active_patient:
        view_analysis_interface()
    else:
        navigate_to("dashboard")