import json
from pathlib import Path
from typing import Any, Dict

def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def normalize_text(s: str) -> str:
    return " ".join((s or "").strip().split())

def normalize_skill(s: str) -> str:
    return normalize_text(s).lower()
