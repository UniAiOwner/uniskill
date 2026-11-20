"""Zero-Noise Token Economizer for UniSkill.

Extracts surgical, high-density code blueprints and constitutional invariants
from large SKILL.md documents, stripping narrative fluff to economize context tokens.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from uniskill.registry import get_skill
from uniskill.invariants import parse_and_validate_frontmatter


def extract_code_blueprints(content: str) -> str:
    """Extracts only code blocks and their immediate preceding markdown headings."""
    lines = content.splitlines()
    extracted_lines = []
    
    current_heading = ""
    in_code_block = False
    current_block_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            current_heading = line
            continue
            
        if stripped.startswith("```"):
            if not in_code_block:
                # Entering code block
                in_code_block = True
                if current_heading:
                    extracted_lines.append(current_heading)
                    current_heading = ""  # Don't repeat heading
                current_block_lines = [line]
            else:
                # Exiting code block
                in_code_block = False
                current_block_lines.append(line)
                extracted_lines.extend(current_block_lines)
                extracted_lines.append("")  # Blank line separator
                current_block_lines = []
            continue
            
        if in_code_block:
            current_block_lines.append(line)
            
    return "\n".join(extracted_lines).strip()


def extract_invariants_and_rules(content: str) -> str:
    """Extracts constitutional invariants, mandatory rules, checklists, and prohibitions."""
    lines = content.splitlines()
    extracted_lines = []
    
    invariant_keywords = [
        "invariant", "rule", "law-", "mandatory", "forbidden", "prohibition",
        "zero-", "checklist", "constraint", "non-negotiable", "constitutional"
    ]
    
    in_invariant_section = False
    current_heading = ""
    
    for line in lines:
        stripped = line.strip()
        lower_stripped = stripped.lower()
        
        if stripped.startswith("#"):
            current_heading = line
            in_invariant_section = any(kw in lower_stripped for kw in invariant_keywords)
            if in_invariant_section:
                extracted_lines.append(current_heading)
            continue
            
        if in_invariant_section:
            if stripped.startswith("#"):
                in_invariant_section = False
            else:
                if stripped:
                    extracted_lines.append(line)
            continue
            
        # Single line invariant / checklist detection
        is_checklist = stripped.startswith(("- [ ]", "* [ ]", "- [x]", "* [x]"))
        has_kw = any(kw in lower_stripped for kw in ["invariant:", "law-000", "law acc-", "strictly forbidden", "mandatory:"])
        
        if is_checklist or has_kw:
            if current_heading and current_heading not in extracted_lines[-3:]:
                extracted_lines.append(current_heading)
            extracted_lines.append(line)
            
    return "\n".join(extracted_lines).strip()


def economize_skill(
    skill_name_or_path: str,
    blueprint_only: bool = False,
    invariants_only: bool = False,
) -> Dict[str, Any]:
    """Economizes a skill down to surgical, zero-noise token density.
    
    Returns:
        dict containing:
            - skill_name
            - original_chars
            - economized_chars
            - tokens_saved_estimate
            - compression_ratio
            - content
    """
    path = Path(skill_name_or_path)
    if path.is_file() and path.name.endswith(".md"):
        content = path.read_text(encoding="utf-8")
        skill_name = path.parent.name if path.name == "SKILL.md" else path.stem
    else:
        skill = get_skill(skill_name_or_path)
        skill_file = skill.get("file_path") or skill.get("path") if skill else None
        if not skill or not skill_file:
            raise FileNotFoundError(f"Skill '{skill_name_or_path}' not found in registry.")
        content = Path(skill_file).read_text(encoding="utf-8")
        skill_name = skill["name"]

    original_chars = len(content)
    frontmatter, body = parse_and_validate_frontmatter(content)
    
    if blueprint_only:
        extracted = extract_code_blueprints(body)
        header = f"# Blueprints & Code Templates: {skill_name}\n"
        final_content = header + "\n" + extracted if extracted else header + "\n(No code blocks found)"
    elif invariants_only:
        extracted = extract_invariants_and_rules(body)
        header = f"# Invariants & Constraints: {skill_name}\n"
        final_content = header + "\n" + extracted if extracted else header + "\n(No explicit invariants section found)"
    else:
        # Full high-density distillation
        blueprints = extract_code_blueprints(body)
        invariants = extract_invariants_and_rules(body)
        desc = frontmatter.get("description", "").strip() if frontmatter else ""
        
        sections = [f"# Distilled Surgical Skill: {skill_name}"]
        if desc:
            sections.append(f"> {desc}\n")
        if invariants:
            sections.append("## Invariants & Rules\n" + invariants)
        if blueprints:
            sections.append("## Blueprints & Code Templates\n" + blueprints)
        final_content = "\n\n".join(sections)

    economized_chars = len(final_content)
    # 1 token ~= 4 chars rule of thumb
    est_orig_tokens = original_chars // 4
    est_econ_tokens = economized_chars // 4
    saved_tokens = max(0, est_orig_tokens - est_econ_tokens)
    ratio = round((1 - (economized_chars / max(1, original_chars))) * 100, 1)

    return {
        "skill_name": skill_name,
        "original_chars": original_chars,
        "economized_chars": economized_chars,
        "tokens_saved_estimate": saved_tokens,
        "compression_percentage": ratio,
        "content": final_content,
    }
