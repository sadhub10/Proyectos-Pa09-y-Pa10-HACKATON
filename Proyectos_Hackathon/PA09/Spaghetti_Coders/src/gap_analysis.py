from utils.helpers import normalize_skill_key as norm_skill

def compute_missing_skills(candidate_skills, required_skills):
    cand = {norm_skill(s) for s in (candidate_skills or [])}
    req = {norm_skill(s) for s in (required_skills or [])}

    missing_norm = req - cand

    missing = []
    for s in (required_skills or []):
        if norm_skill(s) in missing_norm:
            missing.append(s)

    return missing

def gap_summary(job_result, k: int = 5):
    missing = job_result.get("missing", []) or []
    return {
        "job_id": job_result.get("id"),
        "job_title": job_result.get("title"),
        "top_missing": missing[:k]
    }
