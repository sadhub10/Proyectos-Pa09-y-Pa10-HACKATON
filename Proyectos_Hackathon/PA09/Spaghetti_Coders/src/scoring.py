from typing import Dict, List

def employability_score(match_score: float, candidate_skills: List[str]) -> Dict:
    # Score demo (0..100) explicable:
    # 70% depende del match, 30% depende de “variedad” de skills detectadas (capado)
    skills_component = min(len(candidate_skills) * 2, 30)  # 0..30
    total = int(round(match_score * 70 + skills_component))
    total = max(0, min(total, 100))

    return {
        "score": total,
        "explanation": {
            "match_component_0_70": round(match_score * 70, 2),
            "skills_component_0_30": skills_component
        }
    }
