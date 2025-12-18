from __future__ import annotations
from pathlib import Path
import csv
from datetime import datetime
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = PROJECT_ROOT / "data" / "processed" / "session_logs.csv"

def append_log(row: Dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LOG_PATH.exists()
    fieldnames = list(row.keys())

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow(row)

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
