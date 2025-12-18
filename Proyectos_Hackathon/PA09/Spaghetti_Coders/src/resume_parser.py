import os
import re
from typing import Dict, List, Optional

import spacy
from pdfminer.high_level import extract_text
from docx import Document



EMAIL_RE = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

# Panamá: 4-4 con guion o espacio, con o sin +507 / 507
PHONE_RE_PA = r"\b(?:\+?507[-.\s]?)?(?:\(?507\)?[-.\s]?)?\d{4}[-.\s]?\d{4}\b"

# Fallback general (por si el CV trae otro formato):
PHONE_RE_GENERIC = r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}\b"



def _normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    text = extract_text(pdf_path) or ""
    text = text.replace("\t", " ")
    return _normalize_text(text)


def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    parts = []
    for p in doc.paragraphs:
        if p.text and p.text.strip():
            parts.append(p.text.strip())
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
    # Panamá primero
    m = re.search(PHONE_RE_PA, text)
    if m:
        return m.group().strip()

    # fallback general
    m2 = re.search(PHONE_RE_GENERIC, text)
    return m2.group().strip() if m2 else None


def extract_skills(text: str, skills_list: List[str]) -> List[str]:
    found = []
    for skill in skills_list:
        # matching seguro para skills con acentos / puntos / etc.
        pattern = r"(?i)(?<!\w){}(?!\w)".format(re.escape(skill))
        if re.search(pattern, text):
            found.append(skill)
    return sorted(set(found), key=str.lower)


def extract_university_education_es(text: str) -> List[Dict]:
    """
    Extrae educación universitaria en formato:
    - carrera
    - institución
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    results = []

    degree_keywords = [
        "ingeniería", "ingenieria", "licenciatura", "lic.", "técnico",
        "tecnico", "tecnólogo", "tecnologo", "maestría", "maestria"
    ]

    institution_keywords = [
        "universidad", "utp", "up", "usma", "ulatina",
        "instituto", "college"
    ]

    for i, line in enumerate(lines):
        low = line.lower()

        has_degree = any(k in low for k in degree_keywords)
        has_inst = any(k in low for k in institution_keywords)

        degree = None
        institution = None

        # Caso 1: todo en una misma línea
        if has_degree and has_inst:
            degree = line
            institution = line

        # Caso 2: carrera en una línea y universidad en la siguiente
        elif has_degree and i + 1 < len(lines):
            next_line = lines[i + 1].lower()
            if any(k in next_line for k in institution_keywords):
                degree = line
                institution = lines[i + 1]

        if degree or institution:
            results.append({
                "degree": degree,
                "institution": institution
            })

    # Limpiar duplicados
    unique = []
    seen = set()
    for r in results:
        key = (r["degree"], r["institution"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique[:3]  # máximo 3 estudios



def extract_name_es(text: str, nlp=None) -> Optional[str]:
    """
    Estrategia:
    1) Buscar en las primeras ~25 líneas una línea que parezca nombre (sin @, sin números, 2-4 palabras, solo letras)
    2) Si falla, usar NER (PERSON/PER) en el encabezado
    """
    if nlp is None:
        nlp = spacy.load("es_core_news_sm")

    raw_lines = [l.strip() for l in text.splitlines() if l.strip()]
    head_lines = raw_lines[:25]

    # Palabras típicas en encabezado que NO deberían ser el nombre
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

        # Si la línea es demasiado corta o demasiado larga
        words = [w for w in low.split() if w]
        if not (2 <= len(words) <= 4):
            return False

        # Si contiene tokens prohibidos
        if any(tok in low for tok in banned_tokens):
            return False

        # Solo letras y espacios (permite tildes/ñ)
        if not re.match(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$", line):
            return False

        # Evitar líneas tipo “Ciudad de Panamá” (contienen "de")
        # Nota: NO bloqueamos “de” siempre porque hay apellidos compuestos, pero sí filtramos casos claros:
        if low in ("ciudad de panamá", "panamá", "panama"):
            return False

        return True

    candidates = [l for l in head_lines if looks_like_name(l)]
    if candidates:
        return max(candidates, key=len)

    # Fallback NER
    head_text = "\n".join(head_lines)
    doc = nlp(head_text)
    persons = [ent.text.strip() for ent in doc.ents if ent.label_ in ("PER", "PERSON")]
    if persons:
        return max(persons, key=len)

    return None



def parse_resume_es(path: str, skills_list: List[str], nlp=None) -> Dict:
    """
    path: ruta a .pdf o .docx
    """
    try:
        text = extract_text_from_file(path)
    except Exception as e:
        return {"error": f"No se pudo leer el archivo: {e}"}

    if not text:
        return {"error": "No se pudo extraer texto. Si es PDF escaneado, prueba con DOCX o pega el texto."}

    if nlp is None:
        # Cargar una sola vez (más rápido)
        nlp = spacy.load("es_core_news_sm")

    return {
        "name": extract_name_es(text, nlp=nlp),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text, skills_list),
        "education": extract_university_education_es(text),
        "raw_text_preview": text[:1200]
    }

