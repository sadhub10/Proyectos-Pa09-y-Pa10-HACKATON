import json
import unicodedata
from pathlib import Path
from typing import Any, Dict

def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def normalize_text(s: str) -> str:
    return " ".join((s or "").strip().split())

def strip_accents(s: str) -> str:
    s = s or ""
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(ch)
    )

def normalize_skill_key(s: str) -> str:
    s = normalize_text(s).lower()
    s = strip_accents(s)
    return s
