from __future__ import annotations
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT_PATH = PROJECT_ROOT / "src" / "models" / "risk" / "risk_config.json"

DEFAULT_CONFIG = {
    "weights": {
        "Normal": 0.00,
        "Estrés": 0.35,
        "Ansiedad": 0.45,
        "Depresión": 0.65,
        "Ideación suicida": 1.00
    },
    "thresholds": {
        "BAJO": 0.30,
        "MEDIO": 0.55,
        "ALTO": 0.80
    }
}


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)

    print(f"Config de riesgo guardada en: {OUT_PATH}")


if __name__ == "__main__":
    main()
