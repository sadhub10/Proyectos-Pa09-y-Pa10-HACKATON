from typing import Dict, List

def recommend_courses(gaps: List[str], course_catalog: List[Dict], per_skill: int = 1) -> List[Dict]:
    recs = []
    for gap in gaps:
        matches = [c for c in course_catalog if (c.get("skill","").lower() == gap.lower())]
        for c in matches[:per_skill]:
            recs.append(c)
    return recs
