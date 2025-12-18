from functools import lru_cache
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

@lru_cache(maxsize=1)
def get_model(model_name: str = DEFAULT_MODEL) -> SentenceTransformer:
    return SentenceTransformer(model_name)

def embed_texts(texts: List[str], model_name: str = DEFAULT_MODEL) -> np.ndarray:
    model = get_model(model_name)
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
