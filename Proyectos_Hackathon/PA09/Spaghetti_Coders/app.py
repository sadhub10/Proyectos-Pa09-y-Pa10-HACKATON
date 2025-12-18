import os
import streamlit as st

from utils.helpers import load_json
from src.resume_parser import parse_resume_es
from src.matching_embeddings import load_or_build_job_embeddings, rank_jobs_by_embeddings_cached
from src.gap_analysis import gap_summary, compute_missing_skills
from src.recommender import recommend_courses
from src.scoring import employability_score
from src.cv_score import cv_score
from src.cv_coach import concrete_edits, bullet_suggestions_for_job

st.set_page_config(page_title="SkillBridge IA", layout="wide")

st.title("SkillBridge IA")
st.caption("Plataforma de reinserción económica post pandemia: análisis de CV, matching inteligente, brechas, cursos, CV Score, CV Coach y Dashboard Empresa.")

skills_data = load_json("data/skills.json")
jobs_data = load_json("data/jobs.json")
courses_data = load_json("data/courses.json")

skills_list = skills_data["skills"]
jobs = jobs_data["jobs"]
course_catalog = courses_data["courses"]

DEMO_DIR = "data/demo_cvs"

if "candidates_results" not in st.session_state:
    st.session_state.candidates_results = []
if "demo_loaded" not in st.session_state:
    st.session_state.demo_loaded = False

with st.sidebar:
    st.header("Configuración")
    top_n = st.slider("Vacantes a mostrar (candidato)", 3, 15, 8)
    gaps_k = st.slider("Brechas a mostrar (vacante objetivo)", 3, 10, 5)
    st.markdown("---")
    show_debug = st.checkbox("Mostrar debug (texto)", value=False)

    st.markdown("---")
    with st.expander("¿Cómo funciona la IA?", expanded=False):
        st.markdown(
            """
**1) Lectura del CV (NLP)**  
Extraemos texto del PDF/DOCX y detectamos datos clave (nombre, contacto, educación) y habilidades usando listas + sinónimos.

**2) Matching inteligente (Embeddings)**  
Convertimos el CV y cada vacante en vectores numéricos (embeddings) para medir similitud semántica con **similitud coseno**.

**3) Brechas de habilidades (Gap Analysis)**  
Comparamos habilidades del candidato vs. habilidades requeridas por la vacante y detectamos lo que falta.

**4) Recomendación de cursos (Recommender)**  
Sugerimos cursos según las brechas detectadas para cerrar la distancia al puesto.

**5) Scores (Empleabilidad + CV Score)**  
Generamos puntajes para estimar compatibilidad con el mercado y calidad del CV para un ATS.

**Nota:** Todo corre local, sin APIs externas, usando datasets JSON.
            """
        )

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cargar CVs demo"):
            st.session_state.demo_loaded = True
    with c2:
        if st.button("Limpiar demo"):
            st.session_state.demo_loaded = False
            st.session_state.candidates_results = []

@st.cache_resource
def load_jobs_cache(jobs_list):
    return load_or_build_job_embeddings(
        jobs_list,
        jobs_json_path="data/jobs.json",
        cache_dir="models"
    )

jobs_emb, _ = load_jobs_cache(jobs)

def pct01_to_pct(score01: float) -> int:
    return int(round(max(0.0, min(float(score01), 1.0)) * 100))

def safe_list(x):
    return x if isinstance(x, list) else []

def render_education(edu):
    edu = safe_list(edu)
    if not edu:
        st.write("No detectado")
        return
    any_rendered = False
    for e in edu:
        if isinstance(e, dict):
            deg = (e.get("degree") or "").strip()
            inst = (e.get("institution") or "").strip()
            if deg:
                st.write(f"🎓 **{deg}**")
                any_rendered = True
            if inst:
                st.caption(inst)
                any_rendered = True
        else:
            st.write(str(e))
            any_rendered = True
    if not any_rendered:
        st.write("No detectado")

def job_label(j):
    return f"{j.get('title','')} · {j.get('company','')} · {pct01_to_pct(j.get('match_score',0.0))}%"

def process_candidate_from_path(path: str):
    parsed = parse_resume_es(path, skills_list=skills_list)
    if "error" in parsed:
        return None

    ranked = rank_jobs_by_embeddings_cached(parsed, jobs, jobs_emb)
    if not ranked:
        return None

    return {"file": os.path.basename(path), "parsed": parsed, "ranked": ranked}

def load_demo_candidates():
    if not os.path.isdir(DEMO_DIR):
        return []
    demo_paths = []
    for fn in os.listdir(DEMO_DIR):
        if fn.lower().endswith((".pdf", ".docx")):
            demo_paths.append(os.path.join(DEMO_DIR, fn))
    demo_paths = sorted(demo_paths)
    results = []
    for p in demo_paths:
        r = process_candidate_from_path(p)
        if r:
            results.append(r)
    return results

if st.session_state.demo_loaded and not st.session_state.candidates_results:
    st.session_state.candidates_results = load_demo_candidates()

candidate_mode = "demo" if st.session_state.demo_loaded else "single"

uploaded = None
if candidate_mode == "single":
    uploaded = st.file_uploader("Sube tu CV", type=["pdf", "docx"])
    if not uploaded:
        st.info("Sube un CV o usa 'Cargar CVs demo' en la barra lateral.")
        st.stop()

    ext = os.path.splitext(uploaded.name)[1].lower()
    tmp_path = f"data/_tmp_resume{ext}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    single = process_candidate_from_path(tmp_path)
    if not single:
        st.error("No se pudo procesar el CV. Verifica el archivo o el formato.")
        st.stop()

    parsed = single["parsed"]
    ranked = single["ranked"]
    limited_ranked = ranked[:top_n]

    vacancy_labels = [f"{i+1}. {job_label(j)}" for i, j in enumerate(limited_ranked)]
    selected_label = st.selectbox("Selecciona la vacante objetivo", vacancy_labels, index=0)
    target_job = limited_ranked[vacancy_labels.index(selected_label)]

    target_missing = compute_missing_skills(safe_list(parsed.get("skills", [])), safe_list(target_job.get("required_skills", [])))
    target_job = {**target_job, "missing": target_missing}

    summary = gap_summary(target_job, k=gaps_k)
    emp = employability_score(float(target_job.get("match_score", 0.0)), safe_list(parsed.get("skills", [])))
    cvscore, breakdown = cv_score(parsed, target_job)
    coach = concrete_edits(parsed, target_job)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("CV Score", cvscore)
    kpi2.metric("Employability", emp.get("score", 0))
    kpi3.metric("Skills detectadas", len(safe_list(parsed.get("skills", []))))
    kpi4.metric("Match vacante objetivo", f"{pct01_to_pct(target_job.get('match_score', 0.0))}%")

    tabs = st.tabs(["Resumen", "Vacantes", "Brechas + Cursos", "CV Coach", "Detalles"])

    with tabs[0]:
        left, right = st.columns([2, 1])
        with left:
            st.subheader("Perfil")
            i1, i2, i3 = st.columns(3)
            i1.write("**Nombre**")
            i1.write(parsed.get("name") or "No detectado")
            i2.write("**Email**")
            i2.write(parsed.get("email") or "No detectado")
            i3.write("**Teléfono**")
            i3.write(parsed.get("phone") or "No detectado")

            st.subheader("Habilidades detectadas")
            skills = safe_list(parsed.get("skills", []))
            if skills:
                st.dataframe({"skills": skills}, use_container_width=True, hide_index=True)
            else:
                st.info("No se detectaron habilidades.")
        with right:
            st.subheader("Educación")
            render_education(parsed.get("education", []))

            st.subheader("Vacante objetivo")
            st.write(f"**{summary.get('job_title','')}**")
            st.caption(f"{target_job.get('company','')} · {target_job.get('location','')}")
            st.progress(pct01_to_pct(target_job.get("match_score", 0.0)) / 100)

            st.subheader("Brechas clave")
            missing_list = safe_list(summary.get("top_missing", []))
            if missing_list:
                st.dataframe({"faltan": missing_list}, use_container_width=True, hide_index=True)
            else:
                st.success("Sin brechas ✅")

        if show_debug:
            with st.expander("Texto extraído (debug)"):
                st.write(parsed.get("raw_text_preview", ""))

    with tabs[1]:
        st.subheader("Vacantes recomendadas")
        for idx, job in enumerate(limited_ranked, 1):
            score_pct = pct01_to_pct(job.get("match_score", 0.0))
            missing = compute_missing_skills(safe_list(parsed.get("skills", [])), safe_list(job.get("required_skills", [])))
            reqs = safe_list(job.get("required_skills", []))

            header_cols = st.columns([3, 1, 1])
            header_cols[0].markdown(f"### {idx}. {job.get('title','')}")
            header_cols[1].markdown(f"**{score_pct}%**")
            header_cols[2].markdown(f"**Brechas:** {len(missing)}")
            st.progress(score_pct / 100)

            meta_cols = st.columns([1.5, 1.2, 1.3])
            meta_cols[0].write(f"**Empresa:** {job.get('company','')}")
            meta_cols[1].write(f"**Ubicación:** {job.get('location','')}")
            meta_cols[2].write(f"**Requeridas:** {len(reqs)}")

            cA, cB = st.columns(2)
            with cA:
                st.markdown("**Requeridas**")
                st.dataframe({"skills": reqs} if reqs else {"skills": []}, use_container_width=True, hide_index=True)
            with cB:
                st.markdown("**Te faltan**")
                if missing:
                    st.dataframe({"faltan": missing}, use_container_width=True, hide_index=True)
                else:
                    st.success("Ninguna ✅")

            with st.expander("Descripción"):
                st.write(job.get("description", "") or "Sin descripción")

            st.divider()

    with tabs[2]:
        st.subheader("Brechas + Cursos (vacante objetivo)")
        missing_top = safe_list(summary.get("top_missing", []))

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### Brechas")
            if missing_top:
                st.dataframe({"faltan": missing_top}, use_container_width=True, hide_index=True)
            else:
                st.success("Sin brechas ✅")
        with col2:
            st.markdown("### Cursos recomendados")
            recs = recommend_courses(missing_top, course_catalog, per_skill=2)
            if recs:
                rows = []
                for c in recs:
                    rows.append({
                        "skill": c.get("skill", ""),
                        "curso": c.get("title", ""),
                        "proveedor": c.get("provider", ""),
                        "horas": c.get("hours", ""),
                        "url": c.get("url", "")
                    })
                st.dataframe(rows, use_container_width=True, hide_index=True)
            else:
                st.info("No hay cursos para esas brechas todavía.")

    with tabs[3]:
        st.subheader("CV Coach")
        left, right = st.columns([2, 1])
        with right:
            st.markdown("### Bullets sugeridos")
            bullets = bullet_suggestions_for_job(target_job, safe_list(breakdown.get("missing_required_keywords", [])))
            for b in bullets:
                st.code(b, language="markdown")
        with left:
            st.markdown("### Acciones prioritarias")
            edits = coach.get("edits", [])
            if edits:
                for i, e in enumerate(edits, 1):
                    with st.expander(f"{i}. {e.get('title','')}", expanded=(i == 1)):
                        st.write("**Por qué**")
                        st.write(e.get("why", ""))
                        st.write("**Qué hacer**")
                        st.write(e.get("do", ""))
            else:
                st.success("Tu CV ya está bastante completo ✅")

    with tabs[4]:
        st.subheader("Detalles y transparencia")
        d1, d2 = st.columns(2)
        with d1:
            st.markdown("### Employability (desglose)")
            st.json(emp.get("explanation", {}))
            st.markdown("### CV Score (desglose)")
            st.json(breakdown.get("subscores", {}))
            st.markdown("### Secciones detectadas")
            st.json(breakdown.get("sections", {}))
        with d2:
            st.markdown("### Keywords faltantes (ATS)")
            st.write("**Requeridas:**")
            st.write(safe_list(breakdown.get("missing_required_keywords", [])) or "Ninguna")
            st.write("**Deseables:**")
            st.write(safe_list(breakdown.get("missing_nice_keywords", [])) or "Ninguna")
        if show_debug:
            st.markdown("### Texto extraído (debug)")
            st.text_area("Preview", parsed.get("raw_text_preview", ""), height=240)

else:
    candidates = st.session_state.candidates_results
    if not candidates:
        st.error("No se encontraron CVs demo. Coloca archivos en data/demo_cvs/")
        st.stop()

    st.success(f"CVs demo procesados: {len(candidates)}")

    st.header("Dashboard Empresa")
    st.caption("Insights agregados a partir de CVs demo analizados y vacantes cargadas. (Demo, sin base de datos)")

    total_candidates = len(candidates)
    total_jobs = len(jobs)

    match_scores = []
    all_missing = []

    for c in candidates:
        parsed_demo = c["parsed"]
        ranked_demo = c["ranked"]
        tj = ranked_demo[0] if ranked_demo else {}
        match_scores.append(pct01_to_pct(tj.get("match_score", 0.0)))
        missing = compute_missing_skills(safe_list(parsed_demo.get("skills", [])), safe_list(tj.get("required_skills", [])))
        all_missing.extend(missing)

    avg_match = int(round(sum(match_scores) / max(1, len(match_scores))))
    avg_gap = round(len(all_missing) / max(1, total_candidates), 1)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Candidatos analizados", total_candidates)
    k2.metric("Vacantes activas", total_jobs)
    k3.metric("Match promedio (vacante top)", f"{avg_match}%")
    k4.metric("Brecha promedio (skills)", avg_gap)

    demand = {}
    for j in jobs:
        for s in safe_list(j.get("required_skills", [])):
            demand[s] = demand.get(s, 0) + 1
    demand_rows = sorted([{"skill": k, "demanda": v} for k, v in demand.items()], key=lambda x: x["demanda"], reverse=True)[:12]

    missing_freq = {}
    for s in all_missing:
        missing_freq[s] = missing_freq.get(s, 0) + 1
    missing_rows = sorted([{"skill": k, "faltante": v} for k, v in missing_freq.items()], key=lambda x: x["faltante"], reverse=True)[:12]

    left, right = st.columns(2)
    with left:
        st.markdown("### Skills más demandadas (vacantes)")
        st.dataframe(demand_rows, use_container_width=True, hide_index=True)
    with right:
        st.markdown("### Skills más faltantes (brechas)")
        if missing_rows:
            st.dataframe(missing_rows, use_container_width=True, hide_index=True)
        else:
            st.info("No se detectaron brechas.")

    st.markdown("### Vacantes con mayor brecha (según vacante top de cada candidato)")
    job_gap = {}
    job_match = {}
    job_count = {}

    for c in candidates:
        ranked_demo = c["ranked"]
        if not ranked_demo:
            continue
        tj = ranked_demo[0]
        title = tj.get("title", "Vacante")
        miss = compute_missing_skills(safe_list(c["parsed"].get("skills", [])), safe_list(tj.get("required_skills", [])))

        job_gap[title] = job_gap.get(title, 0) + len(miss)
        job_match[title] = job_match.get(title, 0) + pct01_to_pct(tj.get("match_score", 0.0))
        job_count[title] = job_count.get(title, 0) + 1

    job_rows = []
    for title in job_count:
        job_rows.append({
            "vacante": title,
            "candidatos": job_count[title],
            "match_promedio_%": int(round(job_match[title] / job_count[title])),
            "brecha_promedio": round(job_gap[title] / job_count[title], 1)
        })

    job_rows = sorted(job_rows, key=lambda x: x["brecha_promedio"], reverse=True)[:12]
    st.dataframe(job_rows, use_container_width=True, hide_index=True)

    st.markdown("### Insight automático")
    if missing_rows:
        s = missing_rows[0]["skill"]
        n = missing_rows[0]["faltante"]
        st.info(f"La skill con mayor brecha es **{s}** (faltante en **{n}** candidatos). Enfocar capacitación en esta skill puede aumentar la empleabilidad promedio.")
    else:
        st.success("No hay brechas destacables en la muestra actual.")
