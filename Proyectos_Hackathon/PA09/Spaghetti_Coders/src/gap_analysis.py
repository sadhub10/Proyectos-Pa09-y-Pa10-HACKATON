from typing import Dict, List

def top_gaps(missing_skills: List[str], k: int = 5) -> List[str]:
    return missing_skills[:k]

def gap_summary(job_result: Dict, k: int = 5) -> Dict:
    missing = job_result.get("missing", [])
    return {
        "job_id": job_result.get("id"),
        "job_title": job_result.get("title"),
        "top_missing": top_gaps(missing, k=k)
    }
