"""Intent-Driven Semantic Skill Router.

Matches a task description, user prompt, or UniGov task against all 217 skills
to find the exact surgical skills required, bypassing context budget limits.
"""

import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from uniskill.registry import list_skills, DEFAULT_DB_PATH


STOP_WORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with",
    "by", "is", "are", "was", "were", "be", "been", "have", "has", "had",
    "do", "does", "did", "can", "could", "should", "would", "will", "i",
    "you", "we", "they", "it", "this", "that", "these", "those", "of", "from"
}


def tokenize(text: str) -> List[str]:
    """Extracts alphanumeric word tokens in lowercase, including subwords split by hyphens."""
    raw_words = re.findall(r"[a-z0-9_\-]+", text.lower())
    tokens = set()
    for w in raw_words:
        if len(w) > 2 and w not in STOP_WORDS:
            tokens.add(w)
        # Add hyphen-split subwords
        if "-" in w:
            for sub in w.split("-"):
                if len(sub) > 2 and sub not in STOP_WORDS:
                    tokens.add(sub)
    return list(tokens)


def route_skills_for_task(
    task_description: str,
    top_k: int = 3,
    db_path: Path = DEFAULT_DB_PATH,
) -> List[Dict[str, Any]]:
    """Analyzes task description and returns the top_k most relevant skills.
    Each result contains:
    - skill_name
    - category
    - score (0.0 to 100.0%)
    - file_path
    - direct reading directive for Antigravity
    """
    task_tokens = set(tokenize(task_description))
    if not task_tokens:
        return []

    skills = list_skills(db_path=db_path)
    scored_skills: List[Tuple[float, Dict[str, Any]]] = []

    for s in skills:
        score = 0.0
        name = s["name"]
        desc = s["description"]
        category = s["category"]

        name_tokens = set(tokenize(name))
        desc_tokens = set(tokenize(desc))
        cat_tokens = set(tokenize(category))

        # 1. Exact Name / Slug Match (Highest weight: 50 pts)
        name_intersection = task_tokens.intersection(name_tokens)
        if name_intersection:
            score += len(name_intersection) * 25.0

        # 2. Description Match (Medium weight: 30 pts)
        desc_intersection = task_tokens.intersection(desc_tokens)
        if desc_intersection:
            score += min(len(desc_intersection) * 10.0, 30.0)

        # 3. Category Match (Contextual weight: 20 pts)
        cat_intersection = task_tokens.intersection(cat_tokens)
        if cat_intersection:
            score += 15.0

        # Check for multi-word phrase matching
        task_lower = task_description.lower()
        if name.replace("-", " ") in task_lower or name in task_lower:
            score += 40.0

        if score > 0.0:
            normalized_score = min(score, 100.0)
            scored_skills.append((normalized_score, s))

    # Sort descending by score
    scored_skills.sort(key=lambda x: x[0], reverse=True)

    results = []
    for sc, s in scored_skills[:top_k]:
        skill_path = Path(s["file_path"])
        scripts_dir = skill_path.parent / "scripts"
        available_scripts = [f.name for f in scripts_dir.iterdir() if f.is_file()] if scripts_dir.exists() else []

        results.append({
            "skill_name": s["name"],
            "category": s["category"],
            "relevance_score": round(sc, 1),
            "file_path": str(skill_path),
            "reading_directive": f"read_file Path='{skill_path}'",
            "available_scripts": available_scripts,
        })

    return results
