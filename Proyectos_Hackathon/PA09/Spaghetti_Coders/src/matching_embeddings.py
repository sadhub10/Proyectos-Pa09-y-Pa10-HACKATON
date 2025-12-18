import json
import os
import hashlib
from typing import Dict, List, Tuple
import numpy as np

from src.embedding import embed_texts, DEFAULT_MODEL


def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_candidate_text(parsed: Dict) -> str:
    skills = parsed.get("skills", [])
    edu = parsed.get("education", [])
    edu_txt = ""
    if isinstance(edu, list):
        parts = []
        for e in edu:
            if isinstance(e, dict):
                deg = (e.get("degree") or "").strip()
                inst = (e.get("institution") or "").strip()
                combo = " - ".join([p for p in [deg, inst] if p])
                if combo:
                    parts.append(combo)
            else:
                parts.append(str(e))
        edu_txt = " | ".join(parts)
    return f"SKILLS: {', '.join(skills)}. EDUCACION: {edu_txt}".strip()


def build_job_text(job: Dict) -> str:
    title = job.get("title", "")
    req = job.get("required_skills", [])
    nice = job.get("nice_to_have", [])
    desc = job.get("description", "")
    return f"{title}. REQUISITOS: {', '.join(req)}. DESEABLE: {', '.join(nice)}. {desc}".strip()


def _cosine_scores(cand_emb: np.ndarray, jobs_emb: np.ndarray) -> np.ndarray:
    return (cand_emb @ jobs_emb.T).flatten()


def load_or_build_job_embeddings(
    jobs: List[Dict],
    jobs_json_path: str = "data/jobs.json",
    cache_dir: str = "models",
    model_name: str = DEFAULT_MODEL
) -> Tuple[np.ndarray, List[str]]:
    os.makedirs(cache_dir, exist_ok=True)

    jobs_hash = _file_sha256(jobs_json_path)
    meta_path = os.path.join(cache_dir, "jobs_embeddings_meta.json")
    emb_path = os.path.join(cache_dir, "jobs_embeddings.npy")
    texts_path = os.path.join(cache_dir, "jobs_texts.json")

    if os.path.exists(meta_path) and os.path.exists(emb_path) and os.path.exists(texts_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if meta.get("jobs_hash") == jobs_hash and meta.get("model_name") == model_name:
                jobs_emb = np.load(emb_path)
                with open(texts_path, "r", encoding="utf-8") as f:
                    job_texts = json.load(f)
                if isinstance(job_texts, list) and len(job_texts) == len(jobs) and jobs_emb.shape[0] == len(jobs):
                    return jobs_emb, job_texts
        except Exception:
            pass

    job_texts = [build_job_text(j) for j in jobs]
    jobs_emb = embed_texts(job_texts, model_name=model_name)

    np.save(emb_path, jobs_emb)
    with open(texts_path, "w", encoding="utf-8") as f:
        json.dump(job_texts, f, ensure_ascii=False, indent=2)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"jobs_hash": jobs_hash, "model_name": model_name}, f, ensure_ascii=False, indent=2)

    return jobs_emb, job_texts


def rank_jobs_by_embeddings_cached(
    parsed: Dict,
    jobs: List[Dict],
    jobs_emb: np.ndarray,
    model_name: str = DEFAULT_MODEL
) -> List[Dict]:
    cand_text = build_candidate_text(parsed)
    cand_emb = embed_texts([cand_text], model_name=model_name)
    sims = _cosine_scores(cand_emb, jobs_emb)

    ranked = []
    for job, sim in zip(jobs, sims):
        ranked.append({**job, "match_score": float(sim)})

    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    return ranked
