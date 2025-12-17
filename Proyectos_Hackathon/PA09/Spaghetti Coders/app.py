import os
import streamlit as st

from utils.helpers import load_json
from src.resume_parser import parse_resume_es
from src.skill_matcher import rank_jobs
from src.gap_analysis import gap_summary
from src.recommender import recommend_courses
from src.scoring import employability_score

st.set_page_config(page_title="SkillBridge IA", layout="wide")

st.title("SkillBridge IA — Reinserción económica post pandemia (Demo)")
st.caption("Sube un CV (PDF con texto seleccionable o DOCX) para ver vacantes, brechas y cursos recomendados.")

# Load data
skills_data = load_json("data/skills.json")
jobs_data = load_json("data/jobs.json")
courses_data = load_json("data/courses.json")

skills_list = skills_data["skills"]
jobs = jobs_data["jobs"]
course_catalog = courses_data["courses"]

with st.sidebar:
    st.header("Configuración")
    top_n = st.slider("Top vacantes a mostrar", 3, 10, 5)
    gaps_k = st.slider("Brechas a mostrar (para la vacante top)", 3, 10, 5)
    st.markdown("---")
    st.write("Tip: DOCX suele leerse mejor que PDF. Si el PDF es escaneado, no tendrá texto.")

uploaded = st.file_uploader("Sube tu CV (.pdf o .docx)", type=["pdf", "docx"])

if uploaded:
    # Guardar archivo temporal conservando extensión
    ext = os.path.splitext(uploaded.name)[1].lower()
    tmp_path = f"data/_tmp_resume{ext}"

    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.subheader("1) Parsing del CV")
    parsed = parse_resume_es(tmp_path, skills_list=skills_list)

    if "error" in parsed:
        st.error(parsed["error"])
        st.stop()

    colA, colB = st.columns(2)
    with colA:
        st.write("**Nombre:**", parsed.get("name") or "No detectado")
        st.write("**Email:**", parsed.get("email") or "No detectado")
        st.write("**Teléfono:**", parsed.get("phone") or "No detectado")
    with colB:
        st.write("**Educación (señales):**")
        edu = parsed.get("education", [])
        if edu:
            for e in edu:
                 st.write(f"🎓 **{e.get('degree','')}**")
                 if e.get("institution"):
                     st.caption(e["institution"])
        else:
         st.write("No detectado")

    st.write("**Skills detectadas:**")
    st.write(parsed.get("skills", []) or "Ninguna detectada (revisa skills.json o el texto del CV)")

    with st.expander("Ver preview del texto extraído (debug)"):
        st.write(parsed.get("raw_text_preview", ""))

    st.subheader("2) Matching con vacantes")
    ranked = rank_jobs(parsed.get("skills", []), jobs)

    for job in ranked[:top_n]:
        score_pct = int(round(job["match_score"] * 100))
        st.markdown(f"### {job['title']} — **{score_pct}% match**")
        st.write(f"**Empresa:** {job['company']} | **Ubicación:** {job['location']}")
        st.write(job.get("description", ""))

        cols = st.columns(3)
        with cols[0]:
            st.write("**Requeridas:**")
            st.write(job.get("required_skills", []))
        with cols[1]:
            st.write("**Coinciden:**")
            st.write(job.get("overlap", []))
        with cols[2]:
            st.write("**Faltan (brechas):**")
            st.write(job.get("missing", []))

        st.markdown("---")

    st.subheader("3) Brechas + Cursos (para la vacante top)")
    top_job = ranked[0]
    summary = gap_summary(top_job, k=gaps_k)

    st.write("**Vacante objetivo:**", summary["job_title"])
    st.write("**Brechas principales:**", summary["top_missing"] or "Sin brechas (match completo)")

    recs = recommend_courses(summary["top_missing"], course_catalog, per_skill=1)
    st.write("**Cursos recomendados:**")
    if recs:
        for c in recs:
            st.markdown(
                f"- **{c['skill']}**: {c['title']} ({c['provider']}) — {c['hours']}h — {c['url']}"
            )
    else:
        st.write("No hay cursos para esas brechas todavía. Agrega más en data/courses.json")

    st.subheader("4) Puntaje de empleabilidad (demo)")
    emp = employability_score(top_job["match_score"], parsed.get("skills", []))
    st.metric("Employability Score", emp["score"])
    st.json(emp["explanation"])

else:
    st.info("Sube un CV en PDF o DOCX para iniciar la demo.")
