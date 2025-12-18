import re
from typing import Dict, List

ACTION_VERBS = [
    "Lideré", "Implementé", "Optimicé", "Automaticé", "Analicé", "Diseñé",
    "Construí", "Desarrollé", "Coordiné", "Gestioné", "Mejoré", "Reduje",
    "Aumenté", "Estandaricé", "Documenté", "Monitoreé"
]

SECTION_HINTS = {
    "perfil": ["perfil", "resumen", "sobre mí", "sobre mi", "objetivo"],
    "experiencia": ["experiencia", "experiencia laboral", "historial laboral", "empleo"],
    "educacion": ["educación", "educacion", "formación", "formacion", "universidad"],
    "habilidades": ["habilidades", "skills", "competencias", "aptitudes"],
    "proyectos": ["proyectos", "portafolio", "portfolio"],
    "certificaciones": ["certificaciones", "cursos", "certificados"],
    "idiomas": ["idiomas", "lenguas", "inglés", "ingles"]
}

def _has_any(text: str, keywords: List[str]) -> bool:
    low = (text or "").lower()
    return any(k in low for k in keywords)

def detect_missing_sections(raw_text: str) -> List[str]:
    missing = []
    for section, keys in SECTION_HINTS.items():
        if not _has_any(raw_text, keys):
            missing.append(section)
    return missing

def keyword_gaps_for_target_job(raw_text: str, required_skills: List[str], nice_to_have: List[str]) -> Dict:
    low = (raw_text or "").lower()
    missing_required = [s for s in required_skills if s.lower() not in low]
    missing_nice = [s for s in nice_to_have if s.lower() not in low]
    return {"missing_required_keywords": missing_required, "missing_nice_keywords": missing_nice}

def _pick_2_relevant_skills(missing_required: List[str], required: List[str]) -> List[str]:
    base = missing_required[:]
    if len(base) < 2:
        for s in required:
            if s not in base:
                base.append(s)
            if len(base) >= 2:
                break
    return base[:2] if base else required[:2]

def concrete_edits(parsed: Dict, target_job: Dict) -> Dict:
    raw = parsed.get("raw_text") or parsed.get("raw_text_preview") or ""
    skills = parsed.get("skills", []) or []

    required = target_job.get("required_skills", []) or []
    nice = target_job.get("nice_to_have", []) or []
    gaps = keyword_gaps_for_target_job(raw, required, nice)

    missing_sections = detect_missing_sections(raw)

    edits = []

    if not parsed.get("email"):
        edits.append({
            "title": "Agregar correo profesional",
            "why": "El reclutador/ATS necesita un contacto directo.",
            "do": "Incluye un correo tipo nombre.apellido@... en el encabezado."
        })

    if not parsed.get("phone"):
        edits.append({
            "title": "Agregar teléfono en formato Panamá",
            "why": "Facilita contacto inmediato.",
            "do": "Añade +507 ####-#### (ej.: +507 6332-4725) en el encabezado."
        })

    if "perfil" in missing_sections:
        s1, s2 = _pick_2_relevant_skills(gaps["missing_required_keywords"], required)
        edits.append({
            "title": "Añadir Perfil profesional (3–4 líneas)",
            "why": "Mejora el primer impacto y alinea tu CV con la vacante.",
            "do": f"Ejemplo: 'Estudiante/Profesional orientado a {target_job.get('title','el puesto')}, con habilidades en {s1} y {s2}. Enfocado en resultados, aprendizaje rápido y trabajo en equipo.'"
        })

    if len(skills) < 10:
        add_list = gaps["missing_required_keywords"][:6] + gaps["missing_nice_keywords"][:4]
        add_list = [s for s in add_list if s and s not in skills][:10]
        if add_list:
            edits.append({
                "title": "Fortalecer sección de Habilidades",
                "why": "ATS y reclutadores buscan coincidencias rápidas.",
                "do": "Agrega estas habilidades (si aplican y puedes respaldarlas): " + ", ".join(add_list)
            })

    if "experiencia" in missing_sections:
        edits.append({
            "title": "Crear sección Experiencia (aunque sea académica/voluntariado)",
            "why": "Sin experiencia, el CV pierde evidencia de impacto.",
            "do": "Incluye 1–2 experiencias con 2–3 bullets cada una (acción + herramienta + resultado)."
        })

    metrics_present = bool(re.search(r"\b\d+%|\b\d+\b", raw))
    if not metrics_present:
        edits.append({
            "title": "Añadir métricas a tus bullets",
            "why": "Los CVs con números se perciben más sólidos.",
            "do": "Convierte bullets a: acción + herramienta + resultado medible (%, tiempo, volumen, calidad). Ej.: 'Reduje tiempos en 20%'"
        })

    if "proyectos" in missing_sections:
        s1, s2 = _pick_2_relevant_skills(gaps["missing_required_keywords"], required)
        edits.append({
            "title": "Añadir sección Proyectos (2 proyectos)",
            "why": "Demuestra competencias aunque no tengas empleo formal.",
            "do": f"Estructura cada proyecto: Problema → Herramientas ({s1}, {s2}) → Resultado/impacto."
        })

    if "certificaciones" in missing_sections:
        edits.append({
            "title": "Añadir Cursos/Certificaciones (aunque estén en progreso)",
            "why": "Cierra brechas y muestra iniciativa post pandemia.",
            "do": "Lista 2–4 cursos con plataforma + año/estado (En progreso/Completado)."
        })

    return {
        "missing_sections": missing_sections,
        "keyword_gaps": gaps,
        "edits": edits
    }

def bullet_suggestions_for_job(target_job: Dict, missing_required_keywords: List[str]) -> List[str]:
    title = target_job.get("title", "la vacante")
    req = target_job.get("required_skills", []) or []
    s1, s2 = _pick_2_relevant_skills(missing_required_keywords, req)

    verb1 = ACTION_VERBS[0]
    verb2 = ACTION_VERBS[5]
    verb3 = ACTION_VERBS[10]

    return [
        f"- {verb1} actividades alineadas a **{title}**, aplicando **{s1}** para generar resultados medibles (ej.: +X%, -Y min, Z reportes/semana).",
        f"- {verb2} entregables usando **{s2}** (reportes, dashboards o control de datos), asegurando calidad y consistencia.",
        f"- {verb3} procesos con enfoque en eficiencia y servicio, documentando pasos y mejorando la comunicación con el equipo."
    ]
