"""Multi-Skill Intelligent Composer for UniSkill.

Combines multiple complementary skills into a single high-density prompt payload,
deduplicating dependency blocks and respecting LLM context token budgets.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from uniskill.economizer import economize_skill


def deduplicate_dependency_blocks(content: str) -> str:
    """Deduplicates common Gradle or NPM dependency lines across merged skills."""
    lines = content.splitlines()
    seen_deps = set()
    cleaned_lines = []
    in_dep_block = False

    for line in lines:
        stripped = line.strip()
        is_dep_line = any(
            stripped.startswith(prefix)
            for prefix in ("implementation(", "implementation \"", "api(", "testImplementation(", "ksp(")
        ) or any(
            kw in stripped for kw in ("= { group =", "@androidx.", "@compose.")
        )

        if is_dep_line:
            if stripped in seen_deps:
                continue
            seen_deps.add(stripped)
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def compose_skills(
    skill_names: List[str],
    max_tokens: int = 2500,
    include_invariants: bool = True,
    include_blueprints: bool = True,
) -> Dict[str, Any]:
    """Composes multiple skills into a cohesive, high-density prompt injection artifact.

    Args:
        skill_names: List of skill names to combine.
        max_tokens: Maximum estimated tokens allowed for the composed payload.
        include_invariants: Whether to merge constitutional invariants and rules.
        include_blueprints: Whether to merge code blueprints and templates.

    Returns:
        dict containing:
            - skills: list of resolved skills
            - total_original_chars
            - composed_chars
            - estimated_tokens
            - payload: merged markdown content
            - token_budget_exceeded: bool
    """
    if not skill_names:
        raise ValueError("At least one skill name must be provided for composition.")

    skills_data = []
    total_orig_chars = 0

    for name in skill_names:
        try:
            econ = economize_skill(name, blueprint_only=False, invariants_only=False)
            skills_data.append(econ)
            total_orig_chars += econ["original_chars"]
        except Exception as e:
            # Try by direct name fallback
            skills_data.append({
                "skill_name": name,
                "original_chars": 0,
                "content": f"# Skill: {name}\n(Failed to load: {e})",
            })

    sections = [f"# Sovereign Multi-Skill Blueprint Cluster ({', '.join(skill_names)})"]
    sections.append(f"> Synthesized from {len(skills_data)} skills with automated dependency deduplication.\n")

    # 1. Merge Invariants
    if include_invariants:
        sections.append("## Unified Invariants & Non-Negotiable Rules")
        for s in skills_data:
            s_name = s["skill_name"]
            try:
                inv_res = economize_skill(s_name, invariants_only=True)
                lines = [l for l in inv_res["content"].splitlines() if not l.startswith("#")]
                clean_inv = "\n".join(lines).strip()
                if clean_inv:
                    sections.append(f"### Invariants: {s_name}\n{clean_inv}")
            except Exception:
                pass

    # 2. Merge Blueprints
    if include_blueprints:
        sections.append("\n## Unified Architecture & Code Blueprints")
        for s in skills_data:
            s_name = s["skill_name"]
            try:
                bp_res = economize_skill(s_name, blueprint_only=True)
                lines = [l for l in bp_res["content"].splitlines() if not l.startswith("# Blueprints")]
                clean_bp = "\n".join(lines).strip()
                if clean_bp:
                    sections.append(f"### Blueprints: {s_name}\n{clean_bp}")
            except Exception:
                pass

    raw_composed = "\n\n".join(sections)
    deduped_composed = deduplicate_dependency_blocks(raw_composed)

    est_tokens = len(deduped_composed) // 4
    exceeded = est_tokens > max_tokens

    # If exceeded budget, truncate intelligently
    if exceeded:
        max_chars = max_tokens * 4
        deduped_composed = deduped_composed[:max_chars] + f"\n\n[... Truncated to fit token budget of {max_tokens} tokens ...]"
        est_tokens = len(deduped_composed) // 4

    return {
        "skills": skill_names,
        "total_original_chars": total_orig_chars,
        "composed_chars": len(deduped_composed),
        "estimated_tokens": est_tokens,
        "max_tokens_budget": max_tokens,
        "budget_exceeded": exceeded,
        "payload": deduped_composed,
    }
