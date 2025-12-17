def choose_text_backend(mode: str) -> str:
    """
    mode: 'baseline' | 'transformer'
    Devuelve el backend a usar para predicción de texto.
    """
    mode = (mode or "baseline").strip().lower()
    if mode not in {"baseline", "transformer"}:
        return "baseline"
    return mode
