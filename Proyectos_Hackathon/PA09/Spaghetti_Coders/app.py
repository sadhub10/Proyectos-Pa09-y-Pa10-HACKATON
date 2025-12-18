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
st.caption("Plataforma de reinserción económica post pandemia: análisis de CV, matching inteligente, brechas, cursos y mejoras del CV.")

skills_data = load_json("data/skills.json")
jobs_data = load_json("data/jobs.json")
courses_data = load_json("data/courses.json")

skills_list = skills_data["skills"]
jobs = jobs_data["jobs"]
course_catalog = courses_data["courses"]

with st.sidebar:
    st.header("Configuración")
    top_n = st.slider("Vacantes a mostrar", 3, 10, 5)
    gaps_k = st.slider("Brechas a mostrar (vacante objetivo)", 3, 10, 5)
    st.markdown("---")
    show_debug = st.checkbox("Mostrar debug", value=False)

@st.cache_resource
def load_jobs_cache(jobs_list):
    return load_or_build_job_embeddings(
        jobs_list,
        jobs_json_path="data/jobs.json",
        cache_dir="models"
    )

jobs_emb, _ = load_jobs_cache(jobs)

uploaded = st.file_uploader("Sube tu CV", type=["pdf", "docx"])

if not uploaded:
    st.info("Sube un CV en PDF o DOCX para iniciar.")
    st.stop()

ext = os.path.splitext(uploaded.name)[1].lower()
tmp_path = f"data/_tmp_resume{ext}"
with open(tmp_path, "wb") as f:
    f.write(uploaded.getbuffer())

parsed = parse_resume_es(tmp_path, skills_list=skills_list)
if "error" in parsed:
    st.error(parsed["error"])
    st.stop()

ranked = rank_jobs_by_embeddings_cached(parsed, jobs, jobs_emb)
if not ranked:
    st.error("No hay vacantes cargadas en data/jobs.json.")
    st.stop()

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

st.markdown("---")

vacancy_labels = []
for i, j in enumerate(ranked[:top_n], 1):
    vacancy_labels.append(f"{i}. {j.get('title','')} · {j.get('company','')} · {pct01_to_pct(j.get('match_score', 0.0))}%")

selected_label = st.selectbox("Selecciona la vacante objetivo", vacancy_labels, index=0)

selected_index = vacancy_labels.index(selected_label)
target_job = ranked[selected_index]

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
        info1, info2, info3 = st.columns(3)
        info1.write("**Nombre**")
        info1.write(parsed.get("name") or "No detectado")
        info2.write("**Email**")
        info2.write(parsed.get("email") or "No detectado")
        info3.write("**Teléfono**")
        info3.write(parsed.get("phone") or "No detectado")

        st.subheader("Habilidades detectadas")
        skills = safe_list(parsed.get("skills", []))
        if skills:
            st.dataframe({"skills": skills}, use_container_width=True, hide_index=True)
        else:
            st.info("No se detectaron habilidades. Revisa skills.json / skills_aliases.json o el texto del CV.")

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
            st.success("Sin brechas para la vacante objetivo ✅")

with tabs[1]:
    st.subheader("Vacantes recomendadas")
    for idx, job in enumerate(ranked[:top_n], 1):
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
            if reqs:
                st.dataframe({"skills": reqs}, use_container_width=True, hide_index=True)
            else:
                st.write("No especificadas")
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
    st.write(f"**Vacante:** {summary.get('job_title','')}")
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
            st.info("No hay cursos para esas brechas todavía. Agrega más en data/courses.json.")

with tabs[3]:
    st.subheader("CV Coach")
    st.write("Recomendaciones concretas para mejorar tu CV orientadas a la vacante objetivo.")

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
            st.success("Tu CV ya está bastante completo para esta vacante ✅")

with tabs[4]:
    st.subheader("Detalles y transparencia")
    d1, d2 = st.columns(2)

    with d1:
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
