from typing import Dict, List, Tuple
import re

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

def detect_sections(raw_text: str) -> Dict[str, bool]:
    return {sec: _has_any(raw_text, keys) for sec, keys in SECTION_HINTS.items()}

def count_metrics_mentions(raw_text: str) -> int:
    t = raw_text or ""
    patterns = [
        r"\b\d+%\b", r"\b\d+\s?(?:k|K)\b", r"\b\d+\b",
        r"\b(aument|reduc|mejor|optimiz|increment)\w*\b.*\b\d"
    ]
    score = 0
    for p in patterns:
        if re.search(p, t, flags=re.IGNORECASE):
            score += 1
    return min(score, 3)

def cv_score(parsed: Dict, target_job: Dict) -> Tuple[int, Dict]:
    raw = parsed.get("raw_text") or parsed.get("raw_text_preview") or ""
    skills = parsed.get("skills", []) or []

    sections = detect_sections(raw)
    sections_present = sum(1 for v in sections.values() if v)
    sections_total = len(sections)

    req = target_job.get("required_skills", []) or []
    nice = target_job.get("nice_to_have", []) or []

    low = raw.lower()
    missing_req = [s for s in req if s.lower() not in low]
    missing_nice = [s for s in nice if s.lower() not in low]

    metrics_level = count_metrics_mentions(raw)

    subscores = {}
    subscores["contact"] = 0
    if parsed.get("email"): subscores["contact"] += 10
    if parsed.get("phone"): subscores["contact"] += 10

    subscores["education"] = 0
    edu = parsed.get("education", [])
    if isinstance(edu, list) and len(edu) > 0:
        subscores["education"] = 10

    subscores["structure"] = int(round((sections_present / max(1, sections_total)) * 25))

    subscores["skills_strength"] = min(len(skills) * 2, 20)

    subscores["ats_keywords"] = 0
    if len(req) > 0:
        coverage = 1 - (len(missing_req) / len(req))
        subscores["ats_keywords"] = int(round(coverage * 25))
    else:
        subscores["ats_keywords"] = 10

    subscores["impact"] = [0, 5, 10, 15][metrics_level]

    total = sum(subscores.values())
    total = max(0, min(total, 100))

    breakdown = {
        "total": total,
        "subscores": subscores,
        "sections": sections,
        "missing_required_keywords": missing_req[:12],
        "missing_nice_keywords": missing_nice[:12]
    }
    return total, breakdown
