from typing import Dict, List, Tuple
from utils.helpers import normalize_skill

def compute_match(candidate_skills: List[str], job_required: List[str]) -> Tuple[float, List[str], List[str]]:
    cand = {normalize_skill(s) for s in candidate_skills}
    req = {normalize_skill(s) for s in job_required}

    overlap = sorted(req.intersection(cand))
    missing = sorted(req.difference(cand))

    if len(req) == 0:
        return 0.0, overlap, missing

    score = len(overlap) / len(req)  # 0..1
    return score, overlap, missing

def rank_jobs(candidate_skills: List[str], jobs: List[Dict]) -> List[Dict]:
    ranked = []
    for job in jobs:
        score, overlap, missing = compute_match(candidate_skills, job.get("required_skills", []))
        ranked.append({
            **job,
            "match_score": score,
            "overlap": overlap,
            "missing": missing
        })
    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    return ranked
