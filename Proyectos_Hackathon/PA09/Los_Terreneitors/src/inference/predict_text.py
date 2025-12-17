from src.inference.router import choose_text_backend

def predict_text_unified(text: str, mode: str = "baseline"):
    backend = choose_text_backend(mode)

    if backend == "baseline":
        from src.models.baseline.service import predict_with_confidence
        return predict_with_confidence(text)

    from src.models.transformers.predict_transformer import predict_transformer_with_confidence
    return predict_transformer_with_confidence(text)
