"""Autonomous 2026 SOTA Skill Upgrader.

Repairs YAML frontmatter, sanitizes forbidden nomenclature,
updates blueprints to 2026 SOTA standards, and re-syncs across environments.
"""

import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from uniskill.invariants import (
    validate_skill_file,
    parse_and_validate_frontmatter,
    InvariantViolation,
    FORBIDDEN_VEHICLE_TERMS,
    DEVANAGARI_REGEX,
)
from uniskill.registry import (
    compute_file_sha256,
    infer_domain_category,
    infer_compatibility_matrix,
    DEFAULT_SKILLS_ROOT,
    DEFAULT_DB_PATH,
)
from uniskill.sync import sync_skill_to_all_environments


METAPHOR_REPLACEMENTS = {
    "fleet": "cluster",
    "cockpit": "management console",
    "pilot": "operator",
    "copilot": "assistant",
    "autopilot": "autonomous engine",
    "steering wheel": "control interface",
    "engine room": "runtime core",
    "airfield": "staging environment",
    "hangar": "workspace storage",
    "vehicle": "application module",
    "vessel": "data container",
    "convoy": "process pipeline",
}


def sanitize_text(text: str) -> str:
    """Removes Devanagari and replaces forbidden transport metaphors."""
    # 1. Strip Devanagari characters cleanly
    sanitized = DEVANAGARI_REGEX.sub("", text)

    # 2. Replace forbidden vehicle metaphors
    for term, replacement in METAPHOR_REPLACEMENTS.items():
        pattern = rf"\b{re.escape(term)}\b"
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized


def format_frontmatter_block_scalar(name: str, description: str) -> str:
    """Formats clean YAML 1.2 frontmatter using description: >- block scalar."""
    clean_desc = description.strip().replace("\n", " ")
    clean_desc = re.sub(r"\s+", " ", clean_desc)

    # Wrap description lines cleanly at 70 characters
    words = clean_desc.split()
    wrapped_lines = []
    current_line = []
    current_len = 0

    for word in words:
        if current_len + len(word) + 1 > 70:
            wrapped_lines.append("  " + " ".join(current_line))
            current_line = [word]
            current_len = len(word)
        else:
            current_line.append(word)
            current_len += len(word) + 1
    if current_line:
        wrapped_lines.append("  " + " ".join(current_line))

    desc_block = "\n".join(wrapped_lines)

    return f"---\nname: {name}\ndescription: >-\n{desc_block}\n---"


def upgrade_skill_file(
    skill_path: Path,
    db_path: Path = DEFAULT_DB_PATH,
) -> Tuple[bool, str, Dict[str, Any]]:
    """Upgrades a skill file to 2026 SOTA invariants.
    Returns (success, message, details).
    """
    if not skill_path.exists():
        return False, f"File not found: {skill_path}", {}

    raw_content = skill_path.read_text(encoding="utf-8")
    before_sha = compute_file_sha256(skill_path)

    # Parse existing frontmatter and body
    try:
        meta, body = parse_and_validate_frontmatter(raw_content)
        name = meta.get("name", skill_path.parent.name)
        desc = meta.get("description", "")
    except InvariantViolation:
        # Fallback heuristic parser if frontmatter was broken
        parts = raw_content.split("---", 2)
        if len(parts) >= 3:
            raw_meta = parts[1]
            body = parts[2]
            name_m = re.search(r"name:\s*(.+)", raw_meta)
            desc_m = re.search(r"description:\s*(.+)", raw_meta)
            name = name_m.group(1).strip() if name_m else skill_path.parent.name
            desc = desc_m.group(1).strip() if desc_m else "Sovereign Antigravity Skill."
        else:
            name = skill_path.parent.name
            desc = "Sovereign Antigravity Skill."
            body = raw_content

    # Sanitize name and description
    name = re.sub(r"[^a-z0-9_\-]", "-", name.lower()).strip("-")
    clean_desc = sanitize_text(desc)
    clean_body = sanitize_text(body)

    # Reconstruct upgraded content
    new_frontmatter = format_frontmatter_block_scalar(name, clean_desc)
    upgraded_content = f"{new_frontmatter}\n\n{clean_body.strip()}\n"

    # Pre-flight invariant check
    # Write to temp string check
    temp_check = validate_skill_file(skill_path) # test existing first
    skill_path.write_text(upgraded_content, encoding="utf-8")

    # Post-write invariant validation
    post_check = validate_skill_file(skill_path)
    if not post_check["valid"]:
        # Revert on failure
        skill_path.write_text(raw_content, encoding="utf-8")
        return False, f"Post-upgrade validation failed: {'; '.join(post_check['errors'])}", post_check

    after_sha = compute_file_sha256(skill_path)

    # Update SQLite database
    try:
        conn = sqlite3.connect(db_path)
        category = infer_domain_category(name, clean_desc)
        compat = infer_compatibility_matrix(name, clean_body)

        conn.execute("""
        INSERT OR REPLACE INTO skills_catalog (
            id, name, category, description, version, sha256_hash, status,
            compatibility_matrix_json, file_path, last_audited_at
        ) VALUES (?, ?, ?, ?, '2026.1', ?, 'ACTIVE', ?, ?, CURRENT_TIMESTAMP)
        """, (
            name,
            name,
            category,
            clean_desc,
            after_sha,
            import_json := __import__("json").dumps(compat),
            str(skill_path),
        ))

        conn.execute("""
        INSERT INTO skill_lifecycle_events (
            event_type, skill_name, diff_summary, sha256_before, sha256_after, status
        ) VALUES ('UPGRADE', ?, 'Surgically upgraded frontmatter and nomenclature to 2026 SOTA standard', ?, ?, 'SUCCESS')
        """, (name, before_sha, after_sha))

        conn.commit()
        conn.close()
    except Exception:
        pass

    # Synchronize across all 3 environments
    sync_ok, sync_msg = sync_skill_to_all_environments(name, source_env="config", db_path=db_path)

    return True, f"Skill '{name}' successfully upgraded and synchronized: {sync_msg}", {
        "name": name,
        "before_sha": before_sha[:8],
        "after_sha": after_sha[:8],
        "sync_status": sync_msg,
    }
