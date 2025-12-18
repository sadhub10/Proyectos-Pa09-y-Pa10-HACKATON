import os
import re
import json
import hashlib
from typing import Dict, List, Optional

import spacy
from pdfminer.high_level import extract_text
from docx import Document

from utils.helpers import normalize_skill_key, load_json


EMAIL_RE = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_RE_PA = r"\b(?:\+?507[-.\s]?)?(?:\(?507\)?[-.\s]?)?\d{4}[-.\s]?\d{4}\b"
PHONE_RE_GENERIC = r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}\b"


def _normalize_text(text: str) -> str:
    text = (text or "").replace("\r", "\n").replace("\t", " ")
    text = re.sub(r"[ \u00A0]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    return _normalize_text(extract_text(pdf_path) or "")


def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    parts = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
    return _normalize_text("\n".join(parts))


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    if ext == ".docx":
        return extract_text_from_docx(path)
    raise ValueError(f"Formato no soportado: {ext}. Usa .pdf o .docx")


def extract_email(text: str) -> Optional[str]:
    m = re.search(EMAIL_RE, text)
    return m.group() if m else None


def extract_phone(text: str) -> Optional[str]:
    m = re.search(PHONE_RE_PA, text)
    if m:
        return m.group().strip()
    m = re.search(PHONE_RE_GENERIC, text)
    return m.group().strip() if m else None


def _aliases_file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_skill_aliases(path: str = "data/skills_aliases.json") -> Dict[str, str]:
    try:
        data = load_json(path)
        aliases = data.get("aliases", {})
        return {normalize_skill_key(k): v for k, v in aliases.items()}
    except Exception:
        return {}


def extract_skills(text: str, skills_list: List[str], aliases_map: Dict[str, str]) -> List[str]:
    text_norm = normalize_skill_key(text)
    found = set()

    skills_norm = {normalize_skill_key(s): s for s in skills_list}

    for k_norm, canonical in skills_norm.items():
        pattern = r"(?<!\w){}(?!\w)".format(re.escape(k_norm))
        if re.search(pattern, text_norm):
            found.add(canonical)

    for alias_norm, canonical in (aliases_map or {}).items():
        pattern = r"(?<!\w){}(?!\w)".format(re.escape(alias_norm))
        if re.search(pattern, text_norm):
            found.add(canonical)

    return sorted(found, key=str.lower)


def extract_university_education_es(text: str) -> List[Dict]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    results = []

    degree_keywords = [
        "ingeniería", "ingenieria", "licenciatura", "lic.", "maestría", "maestria",
        "doctorado", "técnico", "tecnico", "tecnólogo", "tecnologo"
    ]

    institution_keywords = [
        "universidad", "utp", "up", "usma", "ulatina", "instituto", "college"
    ]

    def has_degree(line: str) -> bool:
        low = line.lower()
        return any(k in low for k in degree_keywords)

    def has_inst(line: str) -> bool:
        low = line.lower()
        return any(k in low for k in institution_keywords)

    for i, line in enumerate(lines):
        degree = None
        institution = None

        if has_degree(line) and has_inst(line):
            degree = line
            institution = line
        elif has_degree(line) and i + 1 < len(lines) and has_inst(lines[i + 1]):
            degree = line
            institution = lines[i + 1]
        elif has_inst(line) and i + 1 < len(lines) and has_degree(lines[i + 1]):
            institution = line
            degree = lines[i + 1]

        if degree or institution:
            results.append({
                "degree": degree,
                "institution": institution
            })

    unique = []
    seen = set()
    for r in results:
        key = ((r.get("degree") or "").lower(), (r.get("institution") or "").lower())
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique[:3]


def extract_name_es(text: str, nlp=None) -> Optional[str]:
    if nlp is None:
        nlp = spacy.load("es_core_news_sm")

    raw_lines = [l.strip() for l in text.splitlines() if l.strip()]
    head_lines = raw_lines[:25]

    banned_tokens = {
        "panamá", "panama", "curriculum", "currículum", "cv", "perfil",
        "correo", "email", "teléfono", "telefono", "celular",
        "linkedin", "github", "dirección", "direccion",
        "ingeniero", "ingeniera", "ing.", "lic.", "dr.", "dra."
    }

    def looks_like_name(line: str) -> bool:
        if "@" in line:
            return False
        if re.search(r"\d", line):
            return False
        low = line.lower().strip()
        words = [w for w in low.split() if w]
        if not (2 <= len(words) <= 4):
            return False
        if any(tok in low for tok in banned_tokens):
            return False
        if not re.match(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$", line):
            return False
        if low in ("ciudad de panamá", "panamá", "panama"):
            return False
        return True

    candidates = [l for l in head_lines if looks_like_name(l)]
    if candidates:
        return max(candidates, key=len)

    head_text = "\n".join(head_lines)
    doc = nlp(head_text)
    persons = [ent.text.strip() for ent in doc.ents if ent.label_ in ("PER", "PERSON")]
    if persons:
        return max(persons, key=len)

    return None


def parse_resume_es(path: str, skills_list: List[str], nlp=None) -> Dict:
    try:
        text = extract_text_from_file(path)
    except Exception as e:
        return {"error": f"No se pudo leer el archivo: {e}"}

    if not text:
        return {"error": "No se pudo extraer texto. Si es PDF escaneado, prueba con DOCX o pega el texto."}

    if nlp is None:
        nlp = spacy.load("es_core_news_sm")

    aliases_map = load_skill_aliases("data/skills_aliases.json")

    return {
        "name": extract_name_es(text, nlp=nlp),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text, skills_list, aliases_map=aliases_map),
        "education": extract_university_education_es(text),
        "raw_text": text[:20000],
        "raw_text_preview": text[:1200]
    }
